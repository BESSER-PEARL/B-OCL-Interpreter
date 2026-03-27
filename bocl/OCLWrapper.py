"""OCL Wrapper using the new grammar, visitor, and evaluator."""
from antlr4 import InputStream, CommonTokenStream
from bocl.grammar.BOCLLexer import BOCLLexer
from bocl.grammar.BOCLParser import BOCLParser
from bocl.visitor import BOCLVisitorImpl
from bocl.evaluator import Evaluator
from bocl.error_handling import BOCLErrorListener, BOCLSyntaxError


class OCLWrapper:
    """Wrapper around the OCL evaluator.

    Args:
        dm: Domain model (BUML).
        om: Object model (BUML).
    """

    def __init__(self, dm, om):
        self.dm = dm
        self.om = om

    def evaluate(self, ocl):
        """Evaluate an OCL constraint.

        Args:
            ocl: Constraint object with .expression and .context attributes.

        Returns:
            Boolean result of the constraint evaluation.

        Raises:
            BOCLSyntaxError: If the OCL expression has syntax errors.
        """
        input_stream = InputStream(ocl.expression)

        # Lexer
        lexer = BOCLLexer(input_stream)
        lexer.removeErrorListeners()
        error_listener = BOCLErrorListener()
        lexer.addErrorListener(error_listener)

        # Parser
        stream = CommonTokenStream(lexer)
        parser = BOCLParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        tree = parser.oclFile()

        if error_listener.has_errors():
            raise BOCLSyntaxError(error_listener.errors)

        # Visitor builds the AST
        visitor = BOCLVisitorImpl(self.dm, self.om, ocl.context)
        ast_root = visitor.visit(tree)

        # Evaluator processes the AST
        evaluator = Evaluator()
        context_name = visitor.context_name
        return evaluator.evaluate(ast_root, self.om, context_name)
