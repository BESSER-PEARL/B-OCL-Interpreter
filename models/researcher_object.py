from besser.BUML.metamodel.structural import *
from besser.BUML.metamodel.object import *

#########################################
#           Structural Model            #
#########################################

# Primitive DataTypes
t_int: PrimitiveDataType = PrimitiveDataType("int")
t_str: PrimitiveDataType = PrimitiveDataType("str")
t_bool: PrimitiveDataType = PrimitiveDataType("bool")

# Paper class
tittle: Property = Property(name="tittle", type=t_str)
wordCount: Property = Property(name="wordcount", type=t_int)
studentPaper: Property = Property(name="studentPaper", type=t_bool)
paper: Class = Class(name="Paper", attributes={tittle, wordCount, studentPaper})

# Researcher class
name: Property = Property(name="name", type=t_str)
isStudent: Property = Property(name="isStudent", type=t_bool)
researcher: Class = Class(name="Researcher", attributes={name, isStudent})

# paper-researcher association
manuscript: Property = Property(name="manuscript", type=paper, multiplicity=Multiplicity(1, 1))
author: Property = Property(name="author", type=researcher, multiplicity=Multiplicity(1, 2))
writes: BinaryAssociation = BinaryAssociation(name="writes", ends={manuscript, author})

# researcher-paper association
submission: Property = Property(name="submission", type=paper, multiplicity=Multiplicity(1, 1))
referee: Property = Property(name="referee", type=researcher, multiplicity=Multiplicity(3, 3))
reviews: BinaryAssociation = BinaryAssociation(name="reviews", ends={submission, referee})

constraintResearcher: Constraint = Constraint(name="NoSelfReviews", context=researcher,
                                               expression="context Researcher inv NoSelfReviews: self.submission->excludes(self.manuscript)", language="OCL")

constraintPaper: Constraint = Constraint(name="PaperLength", context=paper,
                                               expression="context Paper inv :self.wordcount < 10000", language="OCL")

constraintAuthorsOfStudentPaper: Constraint = Constraint(name="AuthorsOfStudentPaper", context=paper,
                                               expression="context Paper inv AuthorsOfStudentPaper: self.author->exists(x:Researcher | x.isStudent =True)", language="OCL")

constraintNoStudentReviewers: Constraint = Constraint(name="NoStudentReviewers", context=paper,
                                               expression="context Paper inv NoStudentReviewers:self.referee->forAll(r:Researcher | r.isStudent =False)", language="OCL")

constraintLimitsOnStudentPapers: Constraint = Constraint(name="LimitsOnStudentPapers", context=paper,
                                               expression="context Paper inv LimitsOnStudentPapers: Paper::allInstances()->exists(p:Paper | p.studentPaper = True) and Paper::allInstances()->select(p:Paper | p.studentPaper=True) ->size() < 5", language="OCL")

constraintPaperTitle: Constraint = Constraint(name="constraintPaperTitle", context=paper,
                                               expression="context Paper inv title: self.tittle<> 'test'", language="OCL")
constraintResearcherName:Constraint = Constraint(name="consResearcherName", context=researcher,
                                               expression="context Researcher inv title: self.name<> 'test'", language="OCL")

constraintPaperWordCountgreater: Constraint = Constraint(name="PaperLength100", context=paper,
                                               expression="context Paper inv :self.wordcount > 1000", language="OCL")


# Structural model
domain_model: DomainModel = DomainModel(name="my_model", types={paper, researcher}, associations={writes, reviews}, constraints = {
                                                                                                                    constraintResearcher,
                                                                                                                    constraintPaper,
                                                                                                                    constraintAuthorsOfStudentPaper,
                                                                                                                    constraintNoStudentReviewers,
                                                                                                                    constraintLimitsOnStudentPapers,
                                                                                                                    constraintPaperTitle,
                                                                                                                    constraintResearcherName,
                                                                                                                    constraintPaperWordCountgreater
                                                                                                                                   })


###################################
#          Object model           #
###################################

# paper  object
paper_name: AttributeLink = AttributeLink(value=DataValue(value="besser lowcode platform", classifier=None), attribute=tittle)
paper_words: AttributeLink = AttributeLink(value=DataValue(value=5000, classifier=None), attribute=wordCount)
paper_student_paper: AttributeLink = AttributeLink(value=DataValue(value=True, classifier=None), attribute=studentPaper)
paper_obj: Object = Object(name="besser paper", classifier=paper, slots=[paper_name, paper_words, paper_student_paper])

# researcher 1  object
r1_name: AttributeLink = AttributeLink(value=DataValue(value="Marc", classifier=None), attribute=name)
r1_is_student: AttributeLink = AttributeLink(value=DataValue(value=True, classifier=None), attribute=isStudent)
researcher_1: Object = Object(name="Marc researcher", classifier=researcher, slots=[r1_name, r1_is_student])

# researcher 2  object
r2_name: AttributeLink = AttributeLink(value=DataValue(value="James", classifier=None), attribute=name)
r2_is_student: AttributeLink = AttributeLink(value=DataValue(value=True, classifier=None), attribute=isStudent)
researcher_2: Object = Object(name="James researcher", classifier=researcher, slots=[r2_name, r2_is_student])

# researcher 3  object
r3_name: AttributeLink = AttributeLink(value=DataValue(value="Adam", classifier=None), attribute=name)
r3_is_student: AttributeLink = AttributeLink(value=DataValue(value=False, classifier=None), attribute=isStudent)
researcher_3: Object = Object(name="Adam researcher", classifier=researcher, slots=[r3_name, r3_is_student])

# researcher 4  object
r4_name: AttributeLink = AttributeLink(value=DataValue(value="Lola", classifier=None), attribute=name)
r4_is_student: AttributeLink = AttributeLink(value=DataValue(value=False, classifier=None), attribute=isStudent)
researcher_4: Object = Object(name="Lola researcher", classifier=researcher, slots=[r4_name, r4_is_student])

# researcher 5  object
r5_name: AttributeLink = AttributeLink(value=DataValue(value="Sarah", classifier=None), attribute=name)
r5_is_student: AttributeLink = AttributeLink(value=DataValue(value=False, classifier=None), attribute=isStudent)
researcher_5: Object = Object(name="Sarah researcher", classifier=researcher, slots=[r5_name, r5_is_student])

# Links definition
writes_1: Link = Link(name="writes", association=writes, connections=[
    LinkEnd(name="manuscript", association_end=manuscript, object=paper_obj),
    LinkEnd(name="author", association_end=author, object=researcher_1)
])

writes_2: Link = Link(name="writes", association=writes, connections=[
    LinkEnd(name="researcher", association_end=manuscript, object=paper_obj),
    LinkEnd(name="author", association_end=author, object=researcher_2)
])

reviews_1: Link = Link(name="writes", association=writes, connections=[
    LinkEnd(name="submission", association_end=submission, object=paper_obj),
    LinkEnd(name="referee", association_end=referee, object=researcher_3)
])

reviews_2: Link = Link(name="writes", association=writes, connections=[
    LinkEnd(name="submission", association_end=submission, object=paper_obj),
    LinkEnd(name="referee", association_end=referee, object=researcher_4)
])

reviews_3: Link = Link(name="writes", association=writes, connections=[
    LinkEnd(name="submission", association_end=submission, object=paper_obj),
    LinkEnd(name="referee", association_end=referee, object=researcher_5)
])



#  object model
object_model: ObjectModel = ObjectModel(name="Object_model", instances={paper_obj, researcher_1, researcher_2, researcher_3, researcher_4, researcher_5},
                                        links={writes_1, writes_2, reviews_1, reviews_2, reviews_3})