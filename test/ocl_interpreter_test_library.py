from models.library_object import library_model,object_model
from bocl.ocl_wrapper import OCLWrapper

def test_1():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[0]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_2():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[1]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_3():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[2]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_4():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[3]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_5():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[4]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_6():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[5]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_7():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[6]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_8():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[7]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_9():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[8]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_10():
    wrapper = OCLWrapper(library_model, object_model)
    constraint=list(library_model.constraints)[9]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

