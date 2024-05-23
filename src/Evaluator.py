from besser.BUML.notations.ocl.FactoryInstance import Factory
from besser.BUML.metamodel.ocl.rules import *
from besser.BUML.metamodel.structural.structural import Property
class Evaluator:
    """The Evaluator class evaluates the OCL constraints based on the object model.

    Args:

    Attributes:
            debug = this attribute is used for debugging purposes and with default value false
            allObjSat = list of all objects that satisfy the contraint
    """
    def __init__(self):
        self.debug = False
        self.allObjSat = []


    def get_value(self,name, obj):
        """The get_value function to retrieve value of attribute from object.

            Args:
                        name: name of the attribute
                        object: Object from object model
            """
        for slot in obj.slots:
            if name == slot.attribute.name:
                if slot.attribute.type.name == 'str':
                    return '"'+ slot.value.value +'"'
                else:
                    return slot.value.value
    def checkInObj(self,obj,source):
        """The checkInObj function identifies the object that contains the source in slots.

        Args:
            obj: Object from object model
            source: source of the current object in the CSTree
        """
        for s in obj.slots:
            if s.attribute.name == source.name:
                return obj
    def checkInLinkEnds(self,obj, source):
        """The checkInLinkEnds function identifies the source in the linkend of the object.

        Args:
            obj: Object from object model
            source: source of the current object in the CSTree
        """
        toRet = []
        for link in obj.links:
            for connection in link.connections:
                if connection.association_end.name == source.name:
                    toRet.append(connection.object)

        return toRet
    def handleForAll(self, tree, allObjs, logicalExp):
        """The handleForAll function handles forAll expression from OCL MM.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    allObjs: all objects from object model
                    logicalExp: Expression to evaluate at the end to get the result
        """
        logicalExp[0] = logicalExp[0] +" ("
        for index in range(len(allObjs)):
            if len(tree.get_body)>0:
                self.update_logical_exp(tree.get_body[0],logicalExp,allObjs[index])
                if index < len(allObjs)-1:
                    logicalExp[0] = logicalExp[0] + " and "
        logicalExp[0] = logicalExp[0] +" )"
        pass
    def handle(self, source, obj, logicalExp,rightSide = False):
        """The handle function handles Property Call expression from OCL MM.

        Args:
                    source: one child in OCL CST
                    obj: one object from object model
                    logicalExp: Expression to evaluate at the end to get the result
                    rightSide: to identify the side of logical expression
        """

        if isinstance(source, PropertyCallExpression) or isinstance(source,Property):
                # if len(source.name.split('.'))==2:
                allObjs = self.checkInObj(obj,source)
                if allObjs is None:
                    allObjs = self.checkInLinkEnds(obj, source)
                for index in range(len(allObjs)):
                    objs = allObjs[index]
                    if len(allObjs) > 1 or rightSide:
                        logicalExp[0] = logicalExp[0] + " [ "
                    for i in range (len(objs.slots)):
                        logicalExp[0] = logicalExp[0] + "\""+str(objs.slots[i].attribute.name)+ str(objs.slots[i].value.value) + "\""
                        if i < len(objs.slots)-1:
                            logicalExp[0] = logicalExp[0]+","
                    if not rightSide:
                        if len(allObjs) > 1 and index< len(allObjs)-1:
                            logicalExp[0] = logicalExp[0] + " ], "
                    else:
                        logicalExp[0] = logicalExp[0] + " ] "
                        if len(allObjs) > 1 and index< len(allObjs)-1:
                            logicalExp[0] = logicalExp[0] + " , "


                pass
        pass
    def handleExcludes(self, tree, obj, logicalExp):
        """The handleExcludes function handles excludes construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logicalExp: Expression to evaluate at the end to get the result
        """
        # tempLogicalExp =[""]
        args = tree.arguments
        self.checkAndAdd(logicalExp, " and ")
        logicalExp[0] = logicalExp[0] + " [ "
        self.handle(tree.source, obj, logicalExp)
        logicalExp[0] = logicalExp[0] + " ] not in "
        if len(args)==1: #Property
            logicalExp[0] = logicalExp[0] + " [ "
            self.handle(args[0],obj,logicalExp,True)
            logicalExp[0] = logicalExp[0] + " ]"
        pass

    def handleIncludes(self, tree, obj, logicalExp):
        """The handleIncludes function handles includes construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logicalExp: Expression to evaluate at the end to get the result
        """

        # tempLogicalExp =[""]
        args = tree.arguments
        self.checkAndAdd(logicalExp, " and ")
        logicalExp[0] = logicalExp[0] + " [ "
        self.handle(tree.source, obj, logicalExp)
        logicalExp[0] = logicalExp[0] + " ] in "
        if len(args)==1: #Property
            logicalExp[0] = logicalExp[0] + " [ "
            self.handle(args[0],obj,logicalExp,True)
            logicalExp[0] = logicalExp[0] + " ]"
        pass
    def handleExists(self,tree,allObjs,logicalExp):
        """The handleExists function handles exists construct.

        Args:
            tree: Tree that is constructed using OCL Parser
            allObjs: all objects from object model
            logicalExp: Expression to evaluate at the end to get the result
        """
        logicalExp[0] = logicalExp[0] + " ( "
        temp = logicalExp[0]
        for index in range(len(allObjs)):
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], logicalExp, allObjs[index])
                if index < len(allObjs) - 1:
                    logicalExp[0] = logicalExp[0] + " or "
        if temp == logicalExp[0]:
            logicalExp[0] = logicalExp[0] + " False "

        logicalExp[0] = logicalExp[0] + " )"
    def handleCollect(self,tree,allObjs,logicalExp):
        """The handleCollect function handles collect construct.

        Args:
               tree: Tree that is constructed using OCL Parser
               allObjs: all objects from object model
               logicalExp: Expression to evaluate at the end to get the result
        """
        self.allObjSat.append([])
        for obj in allObjs:
            expression = [""]
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], expression, obj)
                self.preprocessLogicalExp(expression)
                if eval (expression[0]) == True:
                    self.allObjSat[-1].append(obj)

    def verifyBody (self,tree, obj,logicalExp,source,allObjs= None):
        """The verifyBody function verifies the body of different constructs (e.g., forAll, exists).

        Args:
            tree: Tree that is constructed using OCL Parser
            obj: one object from object model
            logicalExp: Expression to evaluate at the end to get the result
            source: source of the obj in CSTree
        """
        expressionType = tree.name
        if allObjs is None:
            allObjs = self.checkInObj(obj,source)
            if allObjs is None:
                allObjs = self.checkInLinkEnds(obj, source)
        if source.name == "ALLInstances":
                className = source.source.name
                allObjs = self.getValidObjects(className, self.om)

        if expressionType == "forAll":
            self.handleForAll(tree, allObjs, logicalExp)
        elif expressionType == "exists":
            self.handleExists(tree,allObjs,logicalExp)
        elif expressionType == "collect":
            self.handleCollect(tree,allObjs,logicalExp)
        elif expressionType == "select":
            self.handleCollect(tree,allObjs,logicalExp)
        pass
    def getID(self,slots):
        """The getID function gets the ID attribute from the Object.

        Args:
                    slots: slots of the object
        """
        for s in slots:
            if s.get_attribute.is_id:
                return s
    def addToExp(self, item, logicalExp):
        """The addToExp function adds the item to logicalExpression.

        Args:
              item: item to add in Logical Expression
              logicalExp: logical Expression
        """
        if logicalExp[0] == "":
            logicalExp[0] = logicalExp[0] + item
        else:
            logicalExp[0] = logicalExp[0] + " and "+item
    def handleSize(self, tree,obj,logicalExp):
        """The handleSize function handles the size construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logicalExp: Expression to evaluate at the end to get the result
        """
        self.checkAndAdd(logicalExp , " and ")
        logicalExp[0] = logicalExp[0] + "("
        if isinstance(tree.source, Property):
            allObjs = self.checkInObj(obj, tree.source)
            if allObjs is None:
                allObjs = self.checkInLinkEnds(obj, tree.source)
            logicalExp[0] = logicalExp[0] + str(len(allObjs))
            for arg in tree.arguments:

                    if isinstance(arg, IntegerLiteralExpression) or isinstance(arg,
                                                                               RealLiteralExpression) or isinstance(arg,
                                                                                                                    BooleanLiteralExpression):
                            logicalExp[0] = logicalExp[0] + str(arg.value)
                    else:
                        logicalExp[0] = logicalExp[0]+str(arg)
        elif isinstance(tree.source,LoopExp):
            if tree.source.source is not None:
                source = tree.source.source
            if source.name == "ALLInstances":
                className = source.source.name
                allObjs = self.getValidObjects(className, self.om)
            else:
                allObjs = self.checkInObj(obj, source)
                if allObjs is None:
                    allObjs = self.checkInLinkEnds(obj, source)
            self.handleCollect(tree.source,allObjs,logicalExp)
            if len(self.allObjSat)>0:
                logicalExp[0] = logicalExp[0] +str(len(self.allObjSat[-1]))
                self.allObjSat.pop()
            for arg in tree.arguments:

                    if isinstance(arg, IntegerLiteralExpression) or isinstance(arg,
                                                                               RealLiteralExpression) or isinstance(arg,
                                                                                                                    BooleanLiteralExpression):
                            logicalExp[0] = logicalExp[0] + str(arg.value)
                    else:
                        logicalExp[0] = logicalExp[0]+str(arg)
        logicalExp[0] = logicalExp[0] + ")"

    def handleIFExp(self,tree, obj, logicalExp):
        """The handleIFExp function handles the If construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logicalExp: Expression to evaluate at the end to get the result
        """

        tempExp = [""]
        self.update_logical_exp(tree.ifCondition, tempExp, obj)
        self.preprocessLogicalExp(tempExp)
        self.checkAndAdd(logicalExp," and ")
        if eval(tempExp[0])==True:
            self.update_logical_exp(tree.thenExpression, logicalExp, obj)
        else:
            self.update_logical_exp(tree.elseCondition, logicalExp, obj)

        pass
    def handleOCLIsTypeOf(self, tree,obj,logicalExp):
        """The handleOCLIsTypeOf function handles the OCLIsTypeOf construct.

        Args:
                tree: Tree that is constructed using OCL Parser
                obj: one object from object model
                logicalExp: Expression to evaluate at the end to get the result
        """
        if isinstance(tree.source, Property):
            sourceType = tree.source.type.name
            self.checkAndAdd(logicalExp, " and ")
            for index in range(len(tree.arguments)):
                arg = tree.arguments[index].name
                if arg == "String":
                    logicalExp[0] = logicalExp[0] + '\"' + sourceType + '\"' + " =  \"str\""
                elif arg == "Integer":
                    logicalExp[0] = logicalExp[0] + '\"' + sourceType + '\"' + " =  \"int\""
                elif arg == "Boolean":
                    logicalExp[0] = logicalExp[0] + '\"' + sourceType + '\"' + " =  \"bool\""
                elif arg == "Real":
                    logicalExp[0] = logicalExp[0] + '\"' + sourceType + '\"' + " =  \"float\""
                if index >0 and index < len(tree.arguments)-1:
                    self.checkAndAdd(logicalExp, "and")


    def update_logical_exp(self, tree, logicalExp, obj):
        """The update_logical_exp function updates the logical expression.

        Args:
                        tree: Tree that is constructed using OCL Parser
                        obj: one object from object model
                        logicalExp: Expression to evaluate at the end to get the result
        """

        if isinstance(tree,PropertyCallExpression):
           if tree.source == None:
                pass

        if isinstance(tree, LoopExp):#forAll, select,..etc
           source = tree.source
           if obj.classifier.name == self.roothandler.get_context_name():
                self.verifyBody(tree,obj,logicalExp,source)
        if isinstance(tree, IfExp):
            self.handleIFExp(tree, obj, logicalExp)
        if isinstance(tree, OperationCallExpression):

            if tree.name == "EXCLUDES":
                self.handleExcludes(tree, obj, logicalExp)
            elif tree.name == "INCLUDES":
                self.handleIncludes(tree, obj, logicalExp)
            elif tree.name == "Size":
                self.handleSize(tree,obj,logicalExp)
                self.checkAndAdd(logicalExp, " and ")
            elif tree.name == "OCLISTYPEOF":
                self.handleOCLIsTypeOf(tree,obj,logicalExp)
            elif tree.name == "ALLInstances":
                pass #handled elsewhere
            else:
                args = tree.arguments
                for arg in args:
                   if hasattr(arg,'name'):
                       if isinstance(arg,IntegerLiteralExpression) or isinstance(arg,RealLiteralExpression) or isinstance(arg,BooleanLiteralExpression):
                           logicalExp[0] = logicalExp[0] + str(arg.value)
                       elif (isinstance(arg,StringLiteralExpression)):
                           logicalExp[0] = logicalExp[0] + '"'+str(arg.value)+'"'
                       else:
                            logicalExp[0]= logicalExp[0] + str(self.get_value(arg.name,obj))
                   else:
                       if str(arg).lower() == "and" or str(arg).lower() =='or':
                           self.checkAndAdd(logicalExp[0],str(arg))
                       else:
                           logicalExp[0] = logicalExp[0] +" " +str(arg)+ " "
                if tree.referredOperation is not None  and( tree.referredOperation.get_infix_operator() == "and" or tree.referredOperation.get_infix_operator() == "or"):
                    self.checkAndAdd(logicalExp[0],tree.referredOperation.get_infix_operator())
        if hasattr(tree, "source"):
            if tree.source is not None:
                self.update_logical_exp(tree.source, logicalExp, obj)
    def checkAndAdd(self, logicalExpTemplate, toAdd):
        """The checkAndAdd function checks and updates the logical expression.

        Args:
                toAdd: item to add in the logical expression
                logicalExpTemplate: Expression to evaluate at the end to get the result
        """
        if len(logicalExpTemplate[0])>5:
            if toAdd == " and ":
                if logicalExpTemplate[0][-5:] != " and ":
                    logicalExpTemplate[0] = logicalExpTemplate[0]+toAdd
        elif toAdd == " and ":
            if len(logicalExpTemplate[0]) > 0 and len(logicalExpTemplate[0])<=5:
                logicalExpTemplate[0] = logicalExpTemplate[0] + toAdd

        if len(logicalExpTemplate[0]) > 4:
            if toAdd == " or ":
                if logicalExpTemplate[0][-4:] != " or ":
                    logicalExpTemplate[0] = logicalExpTemplate[0] + toAdd

    def valid_object(self,contextName, object):
        """the valid_object verifies if the current object is the one constraint is applied on

        Args:
            contextName: name of the context of OCL constraint
            Object: Object from object model to check

        """
        idSlot = self.getID(object.slots)
        if idSlot.get_attribute.name == contextName:
            return True
        return False
    def getValidObjects(self,contextName, objs):
        """the getValidObjects returns all the objects the constraint should be applied on

        Args:
            contextName: name of the context of OCL constraint
            objs: all objects from object model

        """

        toRet = []
        for obj in objs.instances:
            # if self.valid_object(contextName,obj):
            if obj.classifier.name == contextName:
                toRet.append(obj)
        return toRet

    def preprocessLogicalExp(self,exp):
        """the preprocessLogicalExp function preprocesses before evaluating to correct the syntax.

        Args:
            exp: logical expression to be evaluated

        """
        exp[0]=exp[0].replace(' = ', ' == ').replace('<>', ' != ')
        if len(exp[0])>5:
            if exp[0][-5:] == " and ":
                exp[0] = exp[0][:-5]
        if len(exp[0]) > 4:
            if exp[0][-4:] == " or ":
                exp[0] = exp[0][:-4]
    def evaluate(self, rootHandler,objectModel):
        """the evaluate function is the main function to be called for evaluating any contraint.

        Args:
            rootHandler: Object of class RootHandler that handles the tree
            objectModel: Object Model from BUML models
        """
        self.om = objectModel
        self.roothandler = rootHandler

        objs = self.getValidObjects(self.roothandler.get_context_name(),self.om)
        tree = rootHandler.get_root()
        logicalExpTemplate= [""]
        for i in range(len(objs)):
            self.update_logical_exp(tree, logicalExpTemplate, objs[i])
            if len(objs)>1 and i < len(objs) -1:
                self.checkAndAdd(logicalExpTemplate," and ")


        if self.debug:
            print("Logical Expression")
            print(logicalExpTemplate[0])
        self.preprocessLogicalExp(logicalExpTemplate)
        return eval(logicalExpTemplate[0])