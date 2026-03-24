from models.researcher_object import domain_model,object_model
from bocl.OCLWrapper import OCLWrapper

# Sort constraints by name for deterministic ordering across runs
constraints = sorted(domain_model.constraints, key=lambda c: c.name)

def test_1():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[0]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_2():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[1]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_3():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[2]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_4():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[3]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_5():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[4]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_6():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[5]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_7():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[6]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)

def test_8():
    wrapper = OCLWrapper(domain_model, object_model)
    constraint=constraints[7]
    print("Query: " + str(constraint.expression), end=": ")
    res = None
    try:
        res = wrapper.evaluate(constraint)
    except Exception as error:
            print('\x1b[0;30;41m' + 'Exception Occured! Info:' + str(error) + '\x1b[0m')
            res = None
    assert(res==True)