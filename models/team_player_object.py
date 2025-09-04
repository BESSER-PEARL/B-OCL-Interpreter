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
Team = Class(name="Team")
Player = Class(name="Player")

# Team class attributes and methods
Team_city: Property = Property(name="city", type=StringType)
Team_name: Property = Property(name="name", type=StringType)
Team_division: Property = Property(name="division", type=StringType)
Team.attributes={Team_name, Team_city, Team_division}

# Player class attributes and methods
Player_position: Property = Property(name="position", type=StringType)
Player_age: Property = Property(name="age", type=IntegerType)
Player_name: Property = Property(name="name", type=StringType)
Player_jerseyNumber: Property = Property(name="jerseyNumber", type=IntegerType)
Player.attributes={Player_name, Player_age, Player_position, Player_jerseyNumber}

# Relationships
team_player: BinaryAssociation = BinaryAssociation(
    name="team_player",
    ends={
        Property(name="team", type=Team, multiplicity=Multiplicity(1, 1)),
        Property(name="players", type=Player, multiplicity=Multiplicity(0, 9999))
    }
)


# OCL Constraints
constraint_Team_0_1: Constraint = Constraint(
    name="constraint_Team_0_1",
    context=Team,
    expression="context Team inv inv2: self.players-> collect(p:Player| p.position = 'center')->size()<3",
    language="OCL"
)
constraint_Player_1_1: Constraint = Constraint(
    name="constraint_Player_1_1",
    context=Player,
    expression="context Player inv inv1: self.age > 10",
    language="OCL"
)
constraint_Team_2_1: Constraint = Constraint(
    name="constraint_Team_2_1",
    context=Team,
    expression="context Team inv inv0: self.players-> collect(p:Player| p.position = 'center')->size()>0",
    language="OCL"
)
constraint_Team_3_1: Constraint = Constraint(
    name="constraint_Team_3_1",
    context=Player,
    expression="context Player inv inv0: self.name.size()>1",
    language="OCL"
)

# Domain Model
domain_model = DomainModel(
    name="a",
    types={Team, Player},
    associations={team_player},
    constraints={
constraint_Team_3_1
        #constraint_Team_0_1, constraint_Player_1_1, constraint_Team_2_1
                 },
    generalizations={}
)

################
# OBJECT MODEL #
################
player_1_obj = Player("player_1").attributes(position="center", age=12, name="BESSER", jerseyNumber=10).build()
team_1_obj = Team("team_1").attributes(city="Luxembourg", name="Besser", division="BESSER").build()

team_1_obj.players = player_1_obj

# Object Model instance
object_model: ObjectModel = ObjectModel(
    name="Object_Diagram",
    objects={player_1_obj, team_1_obj}
)
