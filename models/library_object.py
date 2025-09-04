####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata
)
from besser.BUML.metamodel.object import ObjectModel
import datetime

# Classes
Author = Class(name="Author")
Book = Class(name="Book")
Library = Class(name="Library")

# Author class attributes and methods
Author_name: Property = Property(name="name", type=StringType)
Author_email: Property = Property(name="email", type=StringType)
Author.attributes={Author_email, Author_name}

# Book class attributes and methods
Book_pages: Property = Property(name="pages", type=IntegerType)
Book_title: Property = Property(name="title", type=StringType)
Book_release: Property = Property(name="release", type=DateType)
Book.attributes={Book_pages, Book_title, Book_release}

# Library class attributes and methods
Library_name: Property = Property(name="name", type=StringType)
Library_address: Property = Property(name="address", type=StringType)
Library.attributes={Library_name, Library_address}

# Relationships
Author_Book: BinaryAssociation = BinaryAssociation(
    name="Author_Book",
    ends={
        Property(name="writtenBy", type=Author, multiplicity=Multiplicity(1, 9999)),
        Property(name="publishes", type=Book, multiplicity=Multiplicity(0, 9999))
    }
)
Library_Book: BinaryAssociation = BinaryAssociation(
    name="Library_Book",
    ends={
        Property(name="locatedIn", type=Library, multiplicity=Multiplicity(1, 1)),
        Property(name="has", type=Book, multiplicity=Multiplicity(0, 9999))
    }
)


# OCL Constraints
constraint_Library_0_1: Constraint = Constraint(
    name="constraint_Library_0_1",
    context=Library,
    expression="context Library inv inv1: self.has ->forAll(b:Book|b.pages>0)",
    language="OCL"
)
constraint_Book_1_1: Constraint = Constraint(
    name="constraint_Book_1_1",
    context=Book,
    expression="context Book inv inv2: self.pages>0",
    language="OCL"
)
constraint_Book_2_1: Constraint = Constraint(
    name="constraint_Book_2_1",
    context=Book,
    expression="context Book inv inv2: self.title= 'NI'",
    language="OCL"
)
constraint_Book_3_1: Constraint = Constraint(
    name="constraint_Book_3_1",
    context=Book,
    expression="context Book inv inv2: self.title <> 'NI'",
    language="OCL"
)
constraint_Library_4_1: Constraint = Constraint(
    name="constraint_Library_4_1",
    context=Library,
    expression="context Library inv inv3: self.has->exists( i_book : Book | i_book.pages <= 110 )",
    language="OCL"
)
constraint_Library_5_1: Constraint = Constraint(
    name="constraint_Library_5_1",
    context=Library,
    expression="context Library inv inv3: self.has->size()>1",
    language="OCL"
)
constraint_Library_7_1: Constraint = Constraint(
    name="constraint_Library_7_1",
    context=Library,
    expression="context Library inv inv3: self.has->collect(i_book : Book | i_book.pages <= 110)->size()>0",
    language="OCL"
)
constraint_Library_8_1: Constraint = Constraint(
    name="constraint_Library_8_1",
    context=Library,
    expression="context Library inv inv3: if self.name <> 'NI' then self.has->exists( i_book : Book | i_book.pages <= 110 ) else self.has->forAll(b:Book|b.pages>0) endif",
    language="OCL"
)
constraint_Library_9_1: Constraint = Constraint(
    name="constraint_Library_9_1",
    context=Library,
    expression="context Library inv inv3: if self.name = 'NI' then self.has->exists           ( i_book : Book | i_book.pages <= 110 ) else self.has->forAll(b:Book|b.pages>0)            endif",
    language="OCL"
)
constraint_Library_10_1: Constraint = Constraint(
    name="constraint_Library_10_1",
    context=Library,
    expression="context Library inv inv3: if self.name = 'NI' then self.has->exists( i_book : Book | i_book.pages <= 110 ) else self.has->forAll(b:Book|b.pages<0) endif",
    language="OCL"
)
constraint_Book_11_1: Constraint = Constraint(
    name="constraint_Book_11_1",
    context=Book,
    expression="context Book inv inv3: self.title.oclIsTypeOf(String)",
    language="OCL"
)
constraint_Book_12_1: Constraint = Constraint(
    name="constraint_Book_12_1",
    context=Book,
    expression="context Book inv inv3: self.pages.oclIsTypeOf(Integer)",
    language="OCL"
)
constraint_Book_13_1: Constraint = Constraint(
    name="constraint_Book_13_1",
    context=Book,
    expression="context Book inv inv3: self.pages.oclIsTypeOf(String)",
    language="OCL"
)
constraint_Library_14_1: Constraint = Constraint(
    name="constraint_Library_14_1",
    context=Library,
    expression="context Library inv inv3: if self.name <> 'NI' then self.has->exists( i_book : Book | i_book.pages <= 110 )->size()<3 else self.has->forAll(b:Book|b.pages>0) endif",
    language="OCL"
)
constraint_Book_15_1: Constraint = Constraint(
    name="constraint_Book_15_1",
    context=Book,
    expression="context Book inv inv3: self.release < Date::today().addDays(10)",
    language="OCL"
)
constraint_Library_16_1: Constraint = Constraint(
    name="constraint_Library_16_1",
    context=Library,
    expression="context Library inv inv3: self.has->reject(i_book : Book | i_book.pages <= 110)->size()>0",
    language="OCL"
)

# Domain Model
domain_model = DomainModel(
    name="a",
    types={Author, Book, Library},
    associations={Author_Book, Library_Book},
    constraints={constraint_Library_0_1, constraint_Book_1_1, constraint_Book_2_1,
                 # constraint_Book_3_1,
                 constraint_Library_4_1, constraint_Library_5_1,  constraint_Library_7_1, constraint_Library_8_1, constraint_Library_9_1, constraint_Library_10_1, constraint_Book_11_1, constraint_Book_12_1,
                 # constraint_Book_13_1,
                 constraint_Library_14_1, constraint_Book_15_1, constraint_Library_16_1},
    generalizations={}
)

################
# OBJECT MODEL #
################
author_1_obj = Author("author_1").attributes(name="John_Doe", email="john@doe.com").build()
book_1_obj = Book("book_1").attributes(pages=1230, title="NI", release=datetime.datetime.fromisoformat("2025-09-08")).build()
book_2_obj = Book("book_2").attributes(pages=100, title="NI", release=datetime.datetime.fromisoformat("2025-09-02")).build()
library_1_obj = Library("library_1").attributes(name="Library_test", address="street 123").build()

book_1_obj.locatedIn = library_1_obj
book_1_obj.writtenBy = author_1_obj
book_2_obj.writtenBy = author_1_obj
book_2_obj.locatedIn = library_1_obj

# Object Model instance
object_model: ObjectModel = ObjectModel(
    name="Object_Diagram",
    objects={author_1_obj, book_1_obj, book_2_obj, library_1_obj}
)

from besser.BUML.metamodel.project import Project
from besser.BUML.metamodel.structural.structural import Metadata

metadata = Metadata(description="New project")
project = Project(
    name="t",
    models=[domain_model, object_model],
    owner="User",
    metadata=metadata
)