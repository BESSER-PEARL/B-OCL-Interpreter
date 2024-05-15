from models.library_object import library_model,object_model
from src.OCLWrapper import OCLWrapper
if __name__ == '__main__':

    wrapper = OCLWrapper(library_model,object_model)

    for constraint in library_model.constraints:
        print("Query: " + str(constraint.expression),end = ": ")
        res = None
        try:
            res = wrapper.evaluate(constraint)
        except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' +str(error)  + '\x1b[0m')
            res = None
        if res:
            print('\x1b[6;30;42m' + 'True' + '\x1b[0m')
        elif res == False:
            print('\x1b[0;30;41m' + 'False' + '\x1b[0m')