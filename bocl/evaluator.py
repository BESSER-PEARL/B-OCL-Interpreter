"""Importing OCL from main BESSER repository"""
from besser.BUML.metamodel.ocl.ocl import *
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
        self.all_obj_sat = []
        self.om = None
        self.root_handler = None

    def get_value(self, name, obj):
        """The get_value function to retrieve value of attribute from class_object.

            Args:
                        name: name of the attribute
                        obj: Object from object model
            """
        for slot in obj.slots:
            if name == slot.attribute.name:
                if slot.attribute.type.name == 'str':
                    return '"' + slot.value.value + '"'
                if slot.attribute.type.name == 'date':
                    return int(str(slot.value.value.year)+ str(slot.value.value.month) + str(slot.value.value.day))
                return slot.value.value
        return None

    def check_in_obj(self, obj, source):
        """The check_in_obj function identifies the class_object that contains the source in slots.

        Args:
            obj: Object from object model
            source: source of the current object in the CSTree
        """
        for s in obj.slots:
            if s.attribute.name == source.name:
                return obj
        return None

    def check_in_link_ends(self, obj, source):
        """The check_in_link_ends function identifies the source in the linkend of the object.

        Args:
            obj: Object from object model
            source: source of the current object in the CSTree
        """
        to_ret = []
        for link in obj.links:
            for connection in link.connections:
                if connection.association_end.name == source.name:
                    to_ret.append(connection.object)

        return to_ret

    def handle_for_all(self, tree, all_objs, logical_exp):
        """The handle_for_all function handles forAll expression from OCL MM.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    all_objs: all objects from object model
                    logical_exp: Expression to evaluate at the end to get the result
        """
        logical_exp[0] = logical_exp[0] + " ("
        for index in range(len(all_objs)):
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], logical_exp, all_objs[index])
                if index < len(all_objs) - 1:
                    logical_exp[0] = logical_exp[0] + " and "
        logical_exp[0] = logical_exp[0] + " )"

    def handle(self, source, obj, logical_exp, right_side=False):
        """The handle function handles Property Call expression from OCL MM.

        Args:
                    source: one child in OCL CST
                    obj: one object from object model
                    logical_exp: Expression to evaluate at the end to get the result
                    right_side: to identify the side of logical expression
        """

        if isinstance(source, (PropertyCallExpression,Property)):
            # if len(source.name.split('.'))==2:
            all_objs = self.check_in_obj(obj, source)
            if all_objs is None:
                all_objs = self.check_in_link_ends(obj, source)
            for index in range(len(all_objs)):
                objs = all_objs[index]
                if len(all_objs) > 1 or right_side:
                    logical_exp[0] = logical_exp[0] + " [ "
                for i in range(len(objs.slots)):
                    logical_exp[0] = logical_exp[0] + "\"" + str(objs.slots[i].attribute.name) + str(
                        objs.slots[i].value.value) + "\""
                    if i < len(objs.slots) - 1:
                        logical_exp[0] = logical_exp[0] + ","
                if not right_side:
                    if len(all_objs) > 1 and index < len(all_objs) - 1:
                        logical_exp[0] = logical_exp[0] + " ], "
                else:
                    logical_exp[0] = logical_exp[0] + " ] "
                    if len(all_objs) > 1 and index < len(all_objs) - 1:
                        logical_exp[0] = logical_exp[0] + " , "




    def handle_excludes(self, tree, obj, logical_exp):
        """The handle_excludes function handles excludes construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logical_exp: Expression to evaluate at the end to get the result
        """
        # tempLogicalExp =[""]
        args = tree.arguments
        self.check_and_add(logical_exp, " and ")
        logical_exp[0] = logical_exp[0] + " [ "
        self.handle(tree.source, obj, logical_exp)
        logical_exp[0] = logical_exp[0] + " ] not in "
        if len(args) == 1:  # Property
            logical_exp[0] = logical_exp[0] + " [ "
            self.handle(args[0], obj, logical_exp, True)
            logical_exp[0] = logical_exp[0] + " ]"


    def handle_includes(self, tree, obj, logical_exp):
        """The handle_includes function handles includes construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logical_exp: Expression to evaluate at the end to get the result
        """

        # tempLogicalExp =[""]
        args = tree.arguments
        self.check_and_add(logical_exp, " and ")
        logical_exp[0] = logical_exp[0] + " [ "
        self.handle(tree.source, obj, logical_exp)
        logical_exp[0] = logical_exp[0] + " ] in "
        if len(args) == 1:  # Property
            logical_exp[0] = logical_exp[0] + " [ "
            self.handle(args[0], obj, logical_exp, True)
            logical_exp[0] = logical_exp[0] + " ]"


    def handle_exists(self, tree, all_objs, logical_exp):
        """The handle_exists function handles exists construct.

        Args:
            tree: Tree that is constructed using OCL Parser
            all_objs: all objects from object model
            logical_exp: Expression to evaluate at the end to get the result
        """
        logical_exp[0] = logical_exp[0] + " ( "
        temp = logical_exp[0]
        for index in range(len(all_objs)):
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], logical_exp, all_objs[index])
                if index < len(all_objs) - 1:
                    logical_exp[0] = logical_exp[0] + " or "
        if temp == logical_exp[0]:
            logical_exp[0] = logical_exp[0] + " False "

        logical_exp[0] = logical_exp[0] + " )"

    def handle_select(self, tree, all_objs):
        """The handle_select function handles select construct.

        Args:
               tree: Tree that is constructed using OCL Parser
               all_objs: all objects from object model
        """
        self.all_obj_sat.append([])
        for obj in all_objs:
            expression = [""]
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], expression, obj)
                self.preprocess_logical_exp(expression)
                if eval(expression[0]) is True:
                    self.all_obj_sat[-1].append(obj)
    def handle_reject(self, tree, all_objs):
        """The handle_reject function handles reject construct.

        Args:
               tree: Tree that is constructed using OCL Parser
               all_objs: all objects from object model
        """
        self.all_obj_sat.append([])
        for obj in all_objs:
            expression = [""]
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], expression, obj)
                self.preprocess_logical_exp(expression)
                if eval(expression[0]) is False:
                    self.all_obj_sat[-1].append(obj)


    def handle_collect(self, tree, all_objs):
        """The handle_collect function handles collect construct.

        Args:
               tree: Tree that is constructed using OCL Parser
               all_objs: all objects from object model
        """
        self.all_obj_sat.append([])
        for obj in all_objs:
            expression = [""]
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], expression, obj)
                self.preprocess_logical_exp(expression)
                if eval(expression[0]) is True:
                    self.all_obj_sat[-1].append(obj)

    def verify_body(self, tree, obj, logical_exp, source, all_objs = None):
        """The verify_body function verifies the body of different
         constructs (e.g., forAll, exists).

        Args:
            tree: Tree that is constructed using OCL Parser
            obj: one object from object model
            logical_exp: Expression to evaluate at the end to get the result
            source: source of the obj in CSTree
        """
        expression_type = tree.name
        if all_objs is None:
            all_objs = self.check_in_obj(obj, source)
            if all_objs is None:
                all_objs = self.check_in_link_ends(obj, source)
        if source.name == "ALLInstances":
            class_name = source.source.name
            all_objs = self.get_valid_objects(class_name, self.om)

        if expression_type == "forAll":
            self.handle_for_all(tree, all_objs, logical_exp)
        elif expression_type == "exists":
            self.handle_exists(tree, all_objs, logical_exp)
        elif expression_type == "collect":
            self.handle_collect(tree, all_objs)
        elif expression_type == "select":
            self.handle_select(tree, all_objs)
        elif expression_type == "reject":
            self.handle_reject(tree, all_objs)



    def get_id(self, slots):
        """The get_id function gets the ID attribute from the Object.

        Args:
                    slots: slots of the object
        """
        for s in slots:
            if s.get_attribute.is_id:
                return s
        return None

    def add_to_exp(self, item, logical_exp):
        """The add_to_exp function adds the item to logicalExpression.

        Args:
              item: item to add in Logical Expression
              logical_exp: logical Expression
        """
        if logical_exp[0] == "":
            logical_exp[0] = logical_exp[0] + item
        else:
            logical_exp[0] = logical_exp[0] + " and " + item

    def handle_size(self, tree, obj, logical_exp):
        """The handle_size function handles the size construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logical_exp: Expression to evaluate at the end to get the result
        """
        self.check_and_add(logical_exp, " and ")
        logical_exp[0] = logical_exp[0] + "("
        if isinstance(tree.source, Property):
            all_objs = self.check_in_obj(obj, tree.source)
            if all_objs is None:
                all_objs = self.check_in_link_ends(obj, tree.source)
            logical_exp[0] = logical_exp[0] + str(len(all_objs))
            for arg in tree.arguments:
                if isinstance(arg, (IntegerLiteralExpression, RealLiteralExpression, BooleanLiteralExpression)):
                    logical_exp[0] = logical_exp[0] + str(arg.value)
                else:
                    logical_exp[0] = logical_exp[0] + str(arg)
        elif isinstance(tree.source, LoopExp):
            source = None
            if tree.source.source is not None:
                source = tree.source.source
            if source is not None and source.name == "ALLInstances":
                class_name = source.source.name
                all_objs = self.get_valid_objects(class_name, self.om)
            else:
                all_objs = self.check_in_obj(obj, source)
                if all_objs is None:
                    all_objs = self.check_in_link_ends(obj, source)
            self.handle_collect(tree.source, all_objs)
            if len(self.all_obj_sat) > 0:
                logical_exp[0] = logical_exp[0] + str(len(self.all_obj_sat[-1]))
                self.all_obj_sat.pop()
            for arg in tree.arguments:

                if isinstance(arg, (IntegerLiteralExpression,RealLiteralExpression,BooleanLiteralExpression)):
                    logical_exp[0] = logical_exp[0] + str(arg.value)
                else:
                    logical_exp[0] = logical_exp[0] + str(arg)
        logical_exp[0] = logical_exp[0] + ")"

    def handle_if_exp(self, tree, obj, logical_exp):
        """The handle_if_exp function handles the If construct.

        Args:
                    tree: Tree that is constructed using OCL Parser
                    obj: one object from object model
                    logical_exp: Expression to evaluate at the end to get the result
        """

        temp_exp = [""]
        self.update_logical_exp(tree.ifCondition, temp_exp, obj)
        self.preprocess_logical_exp(temp_exp)
        self.check_and_add(logical_exp, " and ")
        if eval(temp_exp[0]) is True:
            self.update_logical_exp(tree.thenExpression, logical_exp, obj)
        else:
            self.update_logical_exp(tree.elseCondition, logical_exp, obj)



    def handle_ocl_is_type_of(self, tree,  logical_exp):
        """The handle_ocl_is_type_of function handles the OCLIsTypeOf construct.

        Args:
                tree: Tree that is constructed using OCL Parser
                obj: one object from object model
                logical_exp: Expression to evaluate at the end to get the result
        """
        if isinstance(tree.source, Property):
            source_type = tree.source.type.name
            self.check_and_add(logical_exp, " and ")
            for index in range(len(tree.arguments)):
                arg = tree.arguments[index].name
                if arg == "String":
                    logical_exp[0] = logical_exp[0] + '\"' + source_type + '\"' + " =  \"str\""
                elif arg == "Integer":
                    logical_exp[0] = logical_exp[0] + '\"' + source_type + '\"' + " =  \"int\""
                elif arg == "Boolean":
                    logical_exp[0] = logical_exp[0] + '\"' + source_type + '\"' + " =  \"bool\""
                elif arg == "Real":
                    logical_exp[0] = logical_exp[0] + '\"' + source_type + '\"' + " =  \"float\""
                if index > 0 and index < len(tree.arguments) - 1:
                    self.check_and_add(logical_exp, "and")
    def handle_date_literal_expression(self,date):
        from datetime import datetime,timedelta
        now = datetime.now()
        if "addDays" in str(date):
            days = str(date).split("addDays")[1].replace(")","").replace("(","")
            now= now+timedelta(days = int(days))

        if "today" in str(date):
            date_time = int(now.strftime("%Y%m%d"))
            return str(date_time)


    def update_logical_exp(self, tree, logical_exp, obj):
        """The update_logical_exp function updates the logical expression.

        Args:
                        tree: Tree that is constructed using OCL Parser
                        obj: one object from object model
                        logical_exp: Expression to evaluate at the end to get the result
        """

        if isinstance(tree, PropertyCallExpression):
            if tree.source is None:
                pass

        if isinstance(tree, LoopExp):  # forAll, select,..etc
            source = tree.source
            if obj.classifier.name == self.root_handler.get_context_name():
                self.verify_body(tree, obj, logical_exp, source)
        if isinstance(tree, IfExp):
            self.handle_if_exp(tree, obj, logical_exp)
        if isinstance(tree, OperationCallExpression):

            if tree.name == "EXCLUDES":
                self.handle_excludes(tree, obj, logical_exp)
            elif tree.name == "INCLUDES":
                self.handle_includes(tree, obj, logical_exp)
            elif tree.name == "Size":
                self.handle_size(tree, obj, logical_exp)
                self.check_and_add(logical_exp, " and ")
            elif tree.name == "OCLISTYPEOF":
                self.handle_ocl_is_type_of(tree,  logical_exp)
            elif tree.name == "ALLInstances":
                pass  # handled elsewhere
            else:
                args = tree.arguments
                for arg in args:
                    if hasattr(arg, 'name'):
                        if isinstance(arg, (IntegerLiteralExpression, RealLiteralExpression, BooleanLiteralExpression)):
                            logical_exp[0] = logical_exp[0] + str(arg.value)
                        elif isinstance(arg, StringLiteralExpression):
                            logical_exp[0] = logical_exp[0] + '"' + str(arg.value) + '"'
                        elif isinstance(arg, DateLiteralExpression):
                            logical_exp[0] = logical_exp[0] + self.handle_date_literal_expression(arg)

                        else:
                            logical_exp[0] = logical_exp[0] + str(self.get_value(arg.name, obj))
                    else:
                        if str(arg).lower() == "and" or str(arg).lower() == 'or':
                            self.check_and_add(logical_exp[0], str(arg))
                        else:
                            logical_exp[0] = logical_exp[0] + " " + str(arg) + " "
                if tree.referredOperation is not None and (
                        tree.referredOperation.get_infix_operator() == "and" or tree.referredOperation.get_infix_operator() == "or"):
                    self.check_and_add(logical_exp[0], tree.referredOperation.get_infix_operator())
        if hasattr(tree, "source"):
            if tree.source is not None:
                self.update_logical_exp(tree.source, logical_exp, obj)

    def check_and_add(self, logical_exp_template, to_add):
        """The check_and_add function checks and updates the logical expression.

        Args:
                to_add: item to add in the logical expression
                logical_exp_template: Expression to evaluate at the end to get the result
        """
        if len(logical_exp_template[0]) > 5:
            if to_add == " and ":
                if logical_exp_template[0][-5:] != " and ":
                    logical_exp_template[0] = logical_exp_template[0] + to_add
        elif to_add == " and ":
            if len(logical_exp_template[0]) > 0 and len(logical_exp_template[0]) <= 5:
                logical_exp_template[0] = logical_exp_template[0] + to_add

        if len(logical_exp_template[0]) > 4:
            if to_add == " or ":
                if logical_exp_template[0][-4:] != " or ":
                    logical_exp_template[0] = logical_exp_template[0] + to_add

    def valid_object(self, context_name, class_object):
        """the valid_object verifies if the current object is the one constraint is applied on

        Args:
            context_name: name of the context of OCL constraint
            class_object: Object from object model to check

        """
        id_slot = self.get_id(class_object.slots)
        if id_slot.get_attribute.name == context_name:
            return True
        return False

    def get_valid_objects(self, context_name, objs):
        """the get_valid_objects returns all the objects the constraint should be applied on

        Args:
            context_name: name of the context of OCL constraint
            objs: all objects from object model

        """

        to_ret = []
        for obj in objs.instances:
            # if self.valid_object(context_name,obj):
            if obj.classifier.name == context_name:
                to_ret.append(obj)
        return to_ret

    def preprocess_logical_exp(self, exp):
        """the preprocess_logical_exp function preprocesses before evaluating to correct the syntax.

        Args:
            exp: logical expression to be evaluated

        """
        exp[0] = exp[0].replace(' = ', ' == ').replace('<>', ' != ')
        if len(exp[0]) > 5:
            if exp[0][-5:] == " and ":
                exp[0] = exp[0][:-5]
        if len(exp[0]) > 4:
            if exp[0][-4:] == " or ":
                exp[0] = exp[0][:-4]

    def evaluate(self, root_handler, object_model):
        """the evaluate function is the main function to be called for evaluating any contraint.

        Args:
            root_handler: Object of class RootHandler that handles the tree
            object_model: Object Model from BUML models
        """
        self.om = object_model
        self.root_handler = root_handler

        objs = self.get_valid_objects(self.root_handler.get_context_name(), self.om)
        tree = root_handler.get_root()
        logical_exp_template = [""]
        for i in range(len(objs)):
            self.update_logical_exp(tree, logical_exp_template, objs[i])
            if len(objs) > 1 and i < len(objs) - 1:
                self.check_and_add(logical_exp_template, " and ")

        if self.debug:
            print("Logical Expression")
            print(logical_exp_template[0])
        self.preprocess_logical_exp(logical_exp_template)
        return eval(logical_exp_template[0])
