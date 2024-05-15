from besser.BUML.notations.ocl.FactoryInstance import Factory
from besser.BUML.metamodel.ocl.rules import *
from besser.BUML.metamodel.structural.structural import Property
class Evaluator:

    def __init__(self):
        self.debug = False
        self.allObjSat = []
    def get_value(self,name, obj):
        for slot in obj.slots:
            if name == slot.attribute.name:
                if slot.attribute.type.name == 'str':
                    return '"'+ slot.value.value +'"'
                else:
                    return slot.value.value
    def checkInObj(self,obj,source):
        for s in obj.slots:
            if s.attribute.name == source.name:
                return obj
    def checkInLinkEnds(self,obj, source):
        toRet = []
        for link in obj.links:
            for connection in link.connections:
                if connection.association_end.name == source.name:
                    toRet.append(connection.object)

        return toRet
    def handleForAll(self, tree, allObjs, logicalExp):
        logicalExp[0] = logicalExp[0] +" ("
        for index in range(len(allObjs)):
            if len(tree.get_body)>0:
                self.update_logical_exp(tree.get_body[0],logicalExp,allObjs[index])
                if index < len(allObjs)-1:
                    logicalExp[0] = logicalExp[0] + " and "
        logicalExp[0] = logicalExp[0] +" )"
        pass
    def handle(self, source, obj, logicalExp,rightSide = False):
        if isinstance(source, PropertyCallExpression):
            if len(source.name.split('.'))==2:
                allObjs = self.checkInObj(obj,source)
                if allObjs is None:
                    allObjs = self.checkInLinkEnds(obj, source)
                for index in range(len(allObjs)):
                    objs = allObjs[index]
                    if len(allObjs) > 1 or rightSide:
                        logicalExp[0] = logicalExp[0] + " [ "
                    for i in range (len(objs.slots)):
                        logicalExp[0] = logicalExp[0] + "\""+str(objs.slots[i].name)+ str(objs.slots[i].value.value) + "\""
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
        logicalExp[0] = logicalExp[0] + " ("
        for index in range(len(allObjs)):
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], logicalExp, allObjs[index])
                if index < len(allObjs) - 1:
                    logicalExp[0] = logicalExp[0] + " or "
        logicalExp[0] = logicalExp[0] + " )"
    def handleCollect(self,tree,allObjs,logicalExp):
        self.allObjSat.append([])
        for obj in allObjs:
            expression = [""]
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], expression, obj)
                if eval (expression[0]) == True:
                    self.allObjSat[-1].append(obj)
    def verifyBody (self,tree, obj,logicalExp,source):
        expressionType = tree.name
        allObjs = self.checkInObj(obj,source)
        if allObjs is None:
            allObjs = self.checkInLinkEnds(obj, source)

        if expressionType == "forAll":
            self.handleForAll(tree, allObjs, logicalExp)
        elif expressionType == "exists":
            self.handleExists(tree,allObjs,logicalExp)
        elif expressionType == "collect":
            self.handleCollect(tree,allObjs,logicalExp)
        pass
    def getID(self,slots):
        for s in slots:
            if s.get_attribute.is_id:
                return s
    def add_to_exp(self,item,logicalExp):
        if logicalExp[0] == "":
            logicalExp[0] = logicalExp[0] + item
        else:
            logicalExp[0] = logicalExp[0] + " and "+item
    def handleSize(self, tree,obj,logicalExp):
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
            allObjs = self.checkInObj(obj, source)
            if allObjs is None:
                allObjs = self.checkInLinkEnds(obj, source)
            self.handleCollect(tree.source,allObjs,logicalExp)
            if len(self.allObjSat)>0:
                logicalExp[0] = logicalExp[0] +str(len(self.allObjSat))
                self.allObjSat.pop()
            for arg in tree.arguments:

                    if isinstance(arg, IntegerLiteralExpression) or isinstance(arg,
                                                                               RealLiteralExpression) or isinstance(arg,
                                                                                                                    BooleanLiteralExpression):
                            logicalExp[0] = logicalExp[0] + str(arg.value)
                    else:
                        logicalExp[0] = logicalExp[0]+str(arg)
        logicalExp[0] = logicalExp[0] + ")"

            #
            # if len(self.allObjSat)>0:
            #     logicalExp[0] = str(len(self.allObjSat))+logicalExp[0]
            #     self.allObjSat.pop()
    def handleIFExp(self,tree, obj, logicalExp):
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
        print("",end ="")

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
                       logicalExp[0] = logicalExp[0] +" " +str(arg)+ " "
                if tree.referredOperation is not None and( tree.referredOperation.get_infix_operator() == "and" or tree.referredOperation.get_infix_operator() == "or"):
                    logicalExp[0] =  " "+logicalExp[0]+" "+tree.referredOperation.get_infix_operator()  +" "
        if hasattr(tree, "source"):
            if tree.source is not None:
                self.update_logical_exp(tree.source, logicalExp, obj)
    def checkAndAdd(self, logicalExpTemplate, toAdd):
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
        idSlot = self.getID(object.slots)
        if idSlot.get_attribute.name == contextName:
            return True
        return False
    def getValidObjects(self,contextName, objs):
        toRet = []
        for obj in objs.instances:
            # if self.valid_object(contextName,obj):
            if obj.classifier.name == contextName:
                toRet.append(obj)
        return toRet

    def preprocessLogicalExp(self,exp):
        exp[0]=exp[0].replace(' = ', ' == ').replace('<>', ' != ')
        if len(exp[0])>5:
            if exp[0][-5:] == " and ":
                exp[0] = exp[0][:-5]
        if len(exp[0]) > 4:
            if exp[0][-4:] == " or ":
                exp[0] = exp[0][:-4]
    def evaluate(self, rootHandler,objectModel):
        self.om = objectModel
        self.roothandler = rootHandler

        objs = self.getValidObjects(self.roothandler.get_context_name(),self.om)
        tree = rootHandler.get_root()
        logicalExpTemplate= [""]
        for i in range(len(objs)):
            self.update_logical_exp(tree, logicalExpTemplate, objs[i])
            if len(objs)>1 and i < len(objs) -1:
                self.checkAndAdd(logicalExpTemplate," and ")
                # logicalExpTemplate[0] = logicalExpTemplate[0] +" and "

        if self.debug:
            print(logicalExpTemplate[0])
        self.preprocessLogicalExp(logicalExpTemplate)
        return eval(logicalExpTemplate[0])