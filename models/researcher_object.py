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
Paper = Class(name="Paper")
Researcher = Class(name="Researcher")

# Paper class attributes and methods
Paper_title: Property = Property(name="title", type=StringType)
Paper_wordCount: Property = Property(name="wordCount", type=IntegerType)
Paper_studentPaper: Property = Property(name="studentPaper", type=BooleanType)
Paper.attributes={Paper_title, Paper_studentPaper, Paper_wordCount}

# Researcher class attributes and methods
Researcher_name: Property = Property(name="name", type=StringType)
Researcher_isStudent: Property = Property(name="isStudent", type=BooleanType)
Researcher.attributes={Researcher_isStudent, Researcher_name}

# Relationships
writes: BinaryAssociation = BinaryAssociation(
    name="writes",
    ends={
        Property(name="manuscript", type=Paper, multiplicity=Multiplicity(1, 9999)),
        Property(name="author", type=Researcher, multiplicity=Multiplicity(1, 1))
    }
)
reviews: BinaryAssociation = BinaryAssociation(
    name="reviews",
    ends={
        Property(name="referee", type=Researcher, multiplicity=Multiplicity(1, 9999)),
        Property(name="submission", type=Paper, multiplicity=Multiplicity(0, 9999))
    }
)


# OCL Constraints
constraint_Researcher_0_1: Constraint = Constraint(
    name="constraint_Researcher_0_1",
    context=Researcher,
    expression="context Researcher inv NoSelfReviews: self.submission->excludes(self.manuscript)",
    language="OCL"
)
constraint_Paper_1_1: Constraint = Constraint(
    name="constraint_Paper_1_1",
    context=Paper,
    expression="context Paper inv :self.wordCount < 10000",
    language="OCL"
)
constraint_Paper_2_1: Constraint = Constraint(
    name="constraint_Paper_2_1",
    context=Paper,
    expression="context Paper inv AuthorsOfStudentPaper: self.author->exists(x:Researcher | x.isStudent =True)",
    language="OCL"
)
constraint_Paper_3_1: Constraint = Constraint(
    name="constraint_Paper_3_1",
    context=Paper,
    expression="context Paper inv NoStudentReviewers:self.referee->forAll(r:Researcher | r.isStudent =False)",
    language="OCL"
)
constraint_Paper_4_1: Constraint = Constraint(
    name="constraint_Paper_4_1",
    context=Paper,
    expression="context Paper inv LimitsOnStudentPapers: Paper::allInstances()->exists(p:Paper | p.studentPaper = True) and Paper::allInstances()->select(p:Paper | p.studentPaper=True) ->size() < 5",
    language="OCL"
)
constraint_Paper_5_1: Constraint = Constraint(
    name="constraint_Paper_5_1",
    context=Paper,
    expression="context Paper inv title: self.title<> 'test'",
    language="OCL"
)
constraint_Researcher_6_1: Constraint = Constraint(
    name="constraint_Researcher_6_1",
    context=Researcher,
    expression="context Researcher inv name: self.name<> 'test'",
    language="OCL"
)
constraint_Paper_7_1: Constraint = Constraint(
    name="constraint_Paper_7_1",
    context=Paper,
    expression="context Paper inv :self.wordCount > 1000",
    language="OCL"
)

# Domain Model
domain_model = DomainModel(
    name="",
    types={Paper, Researcher},
    associations={writes, reviews},
    constraints={constraint_Researcher_0_1, constraint_Paper_1_1, constraint_Paper_2_1, constraint_Paper_3_1, constraint_Paper_4_1, constraint_Paper_5_1, constraint_Researcher_6_1, constraint_Paper_7_1},
    generalizations={}
)

################
# OBJECT MODEL #
################
paper_1_obj = Paper("paper_1").attributes(title="Hello_world", wordCount=1234, studentPaper=True).build()
researcher_1_obj = Researcher("researcher_1").attributes(name="Test", isStudent=True).build()
researcher_2_obj = Researcher("researcher_2").attributes(name="Test_2", isStudent=False).build()

researcher_1_obj.manuscript = paper_1_obj
researcher_2_obj.submission = paper_1_obj

# Object Model instance
object_model: ObjectModel = ObjectModel(
    name="",
    objects={paper_1_obj, researcher_1_obj, researcher_2_obj}
)


######################
# PROJECT DEFINITION #
######################

from besser.BUML.metamodel.project import Project
from besser.BUML.metamodel.structural.structural import Metadata

metadata = Metadata(description="New project")
project = Project(
    name="t",
    models=[domain_model, object_model],
    owner="User",
    metadata=metadata
)
