"""Regression tests for GitHub issue #9: B-OCL grammar issues.

Tests verify that all 6 issues identified in the issue are fixed:
1. Parser hangs on bad input
2. Left recursion
3. Fragmented IF-THEN-ELSE
4. Exponential parsing complexity
5. Implementation coupling (visitor pattern)
6. Grammar in correct repo
"""
import time
import pytest
from antlr4 import InputStream, CommonTokenStream
from besser.BUML.notations.ocl.BOCLLexer import BOCLLexer
from besser.BUML.notations.ocl.BOCLParser import BOCLParser
from besser.BUML.notations.ocl.error_handling import BOCLErrorListener, BOCLSyntaxError
from bocl.OCLWrapper import OCLWrapper
from models.library_object import domain_model, object_model


def _parse(text):
    """Parse OCL text and return (tree, errors, elapsed_ms)."""
    t0 = time.perf_counter()
    input_stream = InputStream(text)
    lexer = BOCLLexer(input_stream)
    lexer.removeErrorListeners()
    listener = BOCLErrorListener()
    lexer.addErrorListener(listener)
    stream = CommonTokenStream(lexer)
    parser = BOCLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    tree = parser.oclFile()
    elapsed = (time.perf_counter() - t0) * 1000
    return tree, listener, elapsed


# ---------------------------------------------------------------
# Issue #1: Parser should NOT hang on malformed input
# ---------------------------------------------------------------
class TestNoParserHangs:
    """Malformed input must produce errors quickly, not hang."""

    def test_missing_inv_and_endif(self):
        """The exact example from issue #9."""
        text = (
            "context Test\n"
            "if parent->isTypeOf(EObjectReference) then\n"
            "parent.elements->size() = 1\n"
            "else if parent->isTypeOf(VariableReference) then true else false\n"
            "endif"
        )
        _, listener, elapsed = _parse(text)
        assert listener.has_errors()
        assert elapsed < 5000  # must finish in <5s, not 60s

    def test_completely_broken_input(self):
        _, listener, elapsed = _parse("blah blah blah")
        assert listener.has_errors()
        assert elapsed < 1000

    def test_empty_input(self):
        _, listener, elapsed = _parse("")
        assert listener.has_errors()
        assert elapsed < 1000

    def test_missing_context(self):
        _, listener, elapsed = _parse("inv x: self.name = 'foo'")
        assert listener.has_errors()
        assert elapsed < 1000


# ---------------------------------------------------------------
# Issue #3: Fragmented IF-THEN-ELSE — must be atomic
# ---------------------------------------------------------------
class TestAtomicIfThenElse:
    """IF/THEN/ELSE/ENDIF must appear together as one construct."""

    def test_standalone_else_rejected(self):
        _, listener, _ = _parse("context Foo inv x: else 5")
        assert listener.has_errors()

    def test_missing_endif_rejected(self):
        _, listener, _ = _parse("context Foo inv x: if true then 1 else 2")
        assert listener.has_errors()

    def test_missing_else_rejected(self):
        _, listener, _ = _parse("context Foo inv x: if true then 1 endif")
        assert listener.has_errors()

    def test_valid_if_then_else_accepted(self):
        text = "context Foo inv x: if true then 1 else 2 endif"
        _, listener, _ = _parse(text)
        assert not listener.has_errors()

    def test_nested_if_then_else(self):
        text = "context Foo inv x: if true then if false then 1 else 2 endif else 3 endif"
        _, listener, _ = _parse(text)
        assert not listener.has_errors()


# ---------------------------------------------------------------
# Issue #4: Parsing performance — no exponential blowup
# ---------------------------------------------------------------
class TestParsingPerformance:
    """Complex expressions must parse in milliseconds, not seconds."""

    def test_chained_navigation(self):
        text = "context Foo inv x: self.a.b.c.d.e"
        _, listener, elapsed = _parse(text)
        assert not listener.has_errors()
        assert elapsed < 500

    def test_chained_arrows(self):
        text = "context Foo inv x: self.items->select(i:Item | i.price > 0)->size() > 0"
        _, listener, elapsed = _parse(text)
        assert not listener.has_errors()
        assert elapsed < 500

    def test_complex_boolean(self):
        text = "context Foo inv x: self.a > 0 and self.b < 10 or self.c = 5 implies self.d <> 3"
        _, listener, elapsed = _parse(text)
        assert not listener.has_errors()
        assert elapsed < 500

    def test_deeply_nested_parentheses(self):
        text = "context Foo inv x: ((((self.a + self.b) * 2) > 0) and true)"
        _, listener, elapsed = _parse(text)
        assert not listener.has_errors()
        assert elapsed < 500


# ---------------------------------------------------------------
# Issue #2 & #5: Proper precedence and visitor-based evaluation
# ---------------------------------------------------------------
class TestPrecedenceAndEvaluation:
    """Grammar has correct operator precedence and visitor produces valid ASTs."""

    def test_if_then_else_evaluates_correctly(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # if self.name <> 'NI' then exists(pages<=110) else forAll(pages>0) endif
        # Library name is "Library_test" != "NI", so then-branch fires
        c = constraints_by_name["constraint_Library_8_1"]
        assert wrapper.evaluate(c) is True

    def test_if_then_else_else_branch(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # if self.name = 'NI' then ... else forAll(pages<0) endif
        # Library name is "Library_test", condition is False, else fires: forAll(pages<0) = False
        c = constraints_by_name["constraint_Library_10_1"]
        assert wrapper.evaluate(c) is False

    def test_forall_evaluates_correctly(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # self.has->forAll(b:Book|b.pages>0) — pages are 1230 and 100
        c = constraints_by_name["constraint_Library_0_1"]
        assert wrapper.evaluate(c) is True

    def test_exists_evaluates_correctly(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # self.has->exists(i_book:Book | i_book.pages <= 110) — book_2 has 100 pages
        c = constraints_by_name["constraint_Library_4_1"]
        assert wrapper.evaluate(c) is True

    def test_comparison_evaluates_correctly(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # self.has->size()>1 — library has 2 books
        c = constraints_by_name["constraint_Library_5_1"]
        assert wrapper.evaluate(c) is True

    def test_collect_size_chain(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # self.has->collect(i_book:Book | i_book.pages<=110)->size()>0
        c = constraints_by_name["constraint_Library_7_1"]
        assert wrapper.evaluate(c) is True

    def test_ocl_is_type_of(self):
        wrapper = OCLWrapper(domain_model, object_model)
        constraints_by_name = {c.name: c for c in domain_model.constraints}

        # self.title.oclIsTypeOf(String) — title is StringType
        c = constraints_by_name["constraint_Book_11_1"]
        assert wrapper.evaluate(c) is True

        # self.pages.oclIsTypeOf(Integer) — pages is IntegerType
        c = constraints_by_name["constraint_Book_12_1"]
        assert wrapper.evaluate(c) is True


# ---------------------------------------------------------------
# Issue #6: Grammar lives in this repo
# ---------------------------------------------------------------
class TestGrammarLocation:
    """BOCL.g4 and generated files must live in besser/BUML/notations/ocl/."""

    def test_grammar_imports_from_besser(self):
        """OCLWrapper must import grammar from besser, not bocl.grammar."""
        import inspect
        from bocl import OCLWrapper as module
        source = inspect.getsource(module)
        assert "besser.BUML.notations.ocl.BOCLLexer" in source
        assert "besser.BUML.notations.ocl.BOCLParser" in source


# ---------------------------------------------------------------
# Error message quality
# ---------------------------------------------------------------
class TestErrorMessages:
    """Syntax errors must produce helpful, specific messages."""

    def test_error_includes_line_number(self):
        _, listener, _ = _parse("blah")
        assert listener.has_errors()
        assert "line" in listener.errors[0]

    def test_syntax_error_exception(self):
        with pytest.raises(BOCLSyntaxError) as exc_info:
            wrapper = OCLWrapper(domain_model, object_model)
            from besser.BUML.metamodel.structural import Constraint
            bad_constraint = Constraint(
                name="bad", context=list(domain_model.types)[0],
                expression="blah blah blah", language="OCL"
            )
            wrapper.evaluate(bad_constraint)
        assert "syntax error" in str(exc_info.value).lower()
