from models.team_player_object import domain_model,object_model
from bocl.OCLWrapper import OCLWrapper

if __name__ == "__main__":
    wrapper = OCLWrapper(domain_model, object_model)
    for constraint in domain_model.constraints:
        print("Query: " + str(constraint.expression), end=": ")
        res = None
        try:
            res = wrapper.evaluate(constraint)
            print('\x1b[0;30;35m' + str(res) + '\x1b[0m')

        except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
