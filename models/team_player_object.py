
from besser.BUML.metamodel.structural import DomainModel, Class, Property, \
    PrimitiveDataType, Multiplicity, BinaryAssociation,Constraint
from besser.BUML.metamodel.object import *
import datetime

#############################################
#   Team Player - structural model definition   #
#############################################

# Primitive DataTypes
t_int: PrimitiveDataType = PrimitiveDataType("int")
t_str: PrimitiveDataType = PrimitiveDataType("str")
t_date: PrimitiveDataType = PrimitiveDataType("date")

# Team attributes definition
team_name: Property = Property(name="name", type=t_str)
team_city: Property = Property(name="city", type=t_str)
team_division: Property = Property(name="division", type=t_str)
# Team class definition
team: Class = Class (name="team", attributes={team_name,team_city,team_division})

# Player attributes definition
name: Property = Property(name="name", type=t_str)
age: Property = Property(name="age", type=t_int)
position: Property = Property(name="position", type=t_str)
jerseyNumber: Property = Property(name="jerseyNumber", type=t_int)

# Player class definition
player: Class = Class (name="player", attributes={name, age, position,jerseyNumber})


# team-player association definition
hasteam: Property = Property(name="many",type=team, multiplicity=Multiplicity(1, 1))
many: Property = Property(name="has", type=player, multiplicity=Multiplicity(0, "*"))
team_player_association: BinaryAssociation = BinaryAssociation(name="team_player_asso", ends={hasteam, many})


constraintPlayerAge: Constraint = Constraint(name = "playerAge",context=player,expression="context player inv inv1: self.age > 10",language="OCL")

constraintTeamCenter: Constraint = Constraint(name = "teamCenter",context=team,expression="context team inv inv2: self.many -> collect(p:player| p.position = 'center')->size()<3",language="OCL")

constraintTeamOtherPlayers: Constraint = Constraint(name = "teamCenterPlayer",context=team,expression="context team inv inv2: self.many -> select(p:player| p.position = 'center')->size()>0",language="OCL")


# Domain model definition
team_player_model : DomainModel = DomainModel(name="Team-Player model", types={team,player},
                                          associations={team_player_association },
                                          constraints={
                                          constraintPlayerAge,
                                          constraintTeamCenter,
constraintTeamOtherPlayers,
                                          }
                                          )


#########################################
#   TeamPlayer -  object model definition   #
#########################################


# Team  object attributes
teamObjectName: AttributeLink = AttributeLink(attribute=team_name, value=DataValue(classifier=t_str, value="test-3"))
teamcity: AttributeLink = AttributeLink(attribute=team_city, value=DataValue(classifier=t_str, value="not important"))
teamDivision: AttributeLink = AttributeLink(attribute=team_division, value=DataValue(classifier=t_str, value="junior"))
# Team  object
teamObject: Object = Object(name="team  object", classifier=team, slots=[teamObjectName,teamcity,teamDivision])

# player  object attributes
player1_obj_name: AttributeLink = AttributeLink(attribute=name, value=DataValue(classifier=t_str, value="test"))
player1_obj_age: AttributeLink = AttributeLink(attribute=age, value=DataValue(classifier=t_int, value=12))
player1_obj_position: AttributeLink = AttributeLink(attribute=position, value=DataValue(classifier=t_str, value="center"))
player1_obj_JN: AttributeLink = AttributeLink(attribute=jerseyNumber, value=DataValue(classifier=t_int, value=10))

# Player  object
player_1_obj: Object = Object(name="playerTest1", classifier=player, slots=[player1_obj_name, player1_obj_age,player1_obj_position,player1_obj_JN])


# player 2  object attributes
player2_obj_name: AttributeLink = AttributeLink(attribute=name, value=DataValue(classifier=t_str, value="test-2"))
player2_obj_age: AttributeLink = AttributeLink(attribute=age, value=DataValue(classifier=t_int, value=15))
player2_obj_position: AttributeLink = AttributeLink(attribute=position, value=DataValue(classifier=t_str, value="center"))
player2_obj_JN: AttributeLink = AttributeLink(attribute=jerseyNumber, value=DataValue(classifier=t_int, value=11))

# Player  object
player_2_obj: Object = Object(name="playerTest2", classifier=player, slots=[player2_obj_name, player2_obj_age,player2_obj_position,player2_obj_JN])

# player1 team  object link
player_1_link_end: LinkEnd = LinkEnd(name="many", association_end=hasteam, object=player_1_obj)
team_1_link_end: LinkEnd = LinkEnd(name="has", association_end=many, object=teamObject)
team_player_link_1: Link = Link(name="team_player_link_1", association=team_player_association, connections=[player_1_link_end,team_1_link_end])

# player2 team  object link
player_2_link_end: LinkEnd = LinkEnd(name="many", association_end=hasteam, object=player_2_obj)
team_2_link_end: LinkEnd = LinkEnd(name="has", association_end=many, object=teamObject)
team_player_link_2: Link = Link(name="team_player_link_2", association=team_player_association, connections=[player_2_link_end,team_2_link_end])

# Object model definition
object_model: ObjectModel = ObjectModel(name="Object model", instances={teamObject, player_1_obj,player_2_obj}, links={team_player_link_1,team_player_link_2})