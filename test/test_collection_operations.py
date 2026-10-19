"""isEmpty(), notEmpty(), sum() and loops over empty collections.

Loop variables are typed (``b: Book``) so these tests do not depend on the
BESSER version inferring the element type of an untyped variable.

Before: ->isEmpty() and ->collect(...)->sum() crashed with
"invalid syntax (<string>, line 1)", and forAll over an empty collection
returned an empty tuple instead of True.
"""

import pytest

from besser.BUML.metamodel.object import AttributeLink, DataValue, Link, LinkEnd, Object, ObjectModel
from besser.BUML.metamodel.structural import (
    BinaryAssociation, Class, Constraint, DomainModel, IntegerType, Multiplicity, Property, StringType,
)
from besser.BUML.notations.ocl.BOCLParser import BOCLParser
from bocl.OCLWrapper import OCLWrapper

NAME, PAGES = Property("name", StringType), Property("pages", IntegerType)
LIBRARY = Class("Library", attributes={NAME})
BOOK = Class("Book", attributes={PAGES})
END_LIBRARY = Property("library", LIBRARY, multiplicity=Multiplicity(1, 1))
END_BOOKS = Property("books", BOOK, multiplicity=Multiplicity(0, "*"))
LIBRARY_BOOK = BinaryAssociation("Library_Book", ends={END_LIBRARY, END_BOOKS})
MODEL = DomainModel("Libraries", types={LIBRARY, BOOK}, associations={LIBRARY_BOOK})


def _evaluate(expression, book_pages):
    lib = Object("lib", LIBRARY, slots=[
        AttributeLink(attribute=NAME, value=DataValue(classifier=StringType, value="City")),
    ])
    books = []
    for i, pages in enumerate(book_pages):
        book = Object(f"b{i}", BOOK, slots=[
            AttributeLink(attribute=PAGES, value=DataValue(classifier=IntegerType, value=pages)),
        ])
        Link(f"l{i}", LIBRARY_BOOK, [LinkEnd(f"x{i}", END_LIBRARY, lib), LinkEnd(f"y{i}", END_BOOKS, book)])
        books.append(book)
    constraint = Constraint(name="c", context=LIBRARY, expression=expression, language="OCL")
    return OCLWrapper(MODEL, ObjectModel("objs", objects={lib, *books})).evaluate(constraint)


@pytest.mark.parametrize(("expression", "book_pages", "expected"), [
    ("context Library inv: self.books->isEmpty()", [], True),
    ("context Library inv: self.books->isEmpty()", [10], False),
    ("context Library inv: not self.books->isEmpty()", [10, 20], True),
    ("context Library inv: self.books->reject(b: Book | b.pages > 0)->isEmpty()", [10, 20], True),
    ("context Library inv: self.books->reject(b: Book | b.pages > 0)->isEmpty()", [10, -1], False),
    ("context Library inv: self.books->forAll(b: Book | b.pages > 0)", [], True),
    ("context Library inv: self.books->exists(b: Book | b.pages > 0)", [], False),
    ("context Library inv: self.books->collect(b: Book | b.pages)->sum() > 25", [10, 20], True),
    ("context Library inv: self.books->collect(b: Book | b.pages)->sum() > 25", [10, 5], False),
    ("context Library inv: self.books->collect(b: Book | b.pages)->sum() = 0", [], True),
])
def test_collection_operations(expression, book_pages, expected):
    assert _evaluate(expression, book_pages) is expected


@pytest.mark.skipif(not hasattr(BOCLParser, "ArrowNotEmptyContext"),
                    reason="this BESSER version's B-OCL grammar has no notEmpty()")
@pytest.mark.parametrize(("book_pages", "expected"), [([], False), ([10], True)])
def test_not_empty(book_pages, expected):
    assert _evaluate("context Library inv: self.books->notEmpty()", book_pages) is expected
