"""Evaluator for OCL constraints using the new visitor-based AST."""
# import sys
# sys.path.append("D:\\Github\\B-OCL-Interpreter\\BESSER\\BESSER\\besser")
from besser.BUML.metamodel.ocl.ocl import (
    OperationCallExpression, LoopExp, IfExp, VariableExp,
    IntegerLiteralExpression, RealLiteralExpression,
    BooleanLiteralExpression, StringLiteralExpression,
    DateLiteralExpression, InfixOperator, TypeExp,
)
from besser.BUML.metamodel.structural.structural import Property
import re
from datetime import datetime, timedelta


class Evaluator:
    """Evaluates OCL constraints against an object model.

    The evaluator builds a Python expression string from the AST
    and uses eval() to compute the result. This preserves the
    original evaluation strategy while supporting the new AST
    structure produced by the visitor.
    """

    def __init__(self):
        self.debug = False
        self.all_obj_sat = []
        self.om = None
        self.context_name = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def evaluate(self, ast_root, object_model, context_name):
        """Evaluate a constraint AST against the object model.

        Args:
            ast_root: Root AST node from the visitor.
            object_model: BUML ObjectModel instance.
            context_name: Name of the context class (e.g. 'Library').

        Returns:
            Boolean result of the constraint evaluation.
        """
        self.om = object_model
        self.context_name = context_name

        objs = self.get_valid_objects(context_name, self.om)
        logical_exp = [""]
        for i, obj in enumerate(objs):
            self.update_logical_exp(ast_root, logical_exp, obj)
            if i < len(objs) - 1:
                self._safe_add(logical_exp, " and ")

        if self.debug:
            print("Logical Expression:", logical_exp[0])

        self._preprocess(logical_exp)
        return eval(logical_exp[0])

    # ------------------------------------------------------------------
    # Value retrieval from objects
    # ------------------------------------------------------------------
    def get_value(self, name, obj):
        for slot in obj.slots:
            if name == slot.attribute.name:
                if slot.attribute.type.name == 'str':
                    return '"' + slot.value.value + '"'
                if slot.attribute.type.name == 'date':
                    d = slot.value.value
                    return int(str(d.year) + str(d.month) + str(d.day))
                return slot.value.value
        return None

    def check_in_obj(self, obj, source):
        for s in obj.slots:
            if s.attribute.name == source.name:
                return obj
        return None

    def check_in_link_ends(self, obj, source):
        to_ret = []
        for link in obj.links:
            for connection in link.connections:
                if connection.association_end.name == source.name:
                    to_ret.append(connection.object)
        return to_ret

    def get_valid_objects(self, context_name, objs):
        return [obj for obj in objs.instances if obj.classifier.name == context_name]

    def _resolve_source_objects(self, source, obj):
        """Resolve a source expression to a list of objects."""
        if isinstance(source, Property):
            result = self.check_in_obj(obj, source)
            if result is None:
                result = self.check_in_link_ends(obj, source)
            if isinstance(result, list):
                return result
            return [result] if result is not None else []

        if isinstance(source, OperationCallExpression):
            if source.name == "ALLInstances":
                class_name = source.source.name
                return self.get_valid_objects(class_name, self.om)

        return []

    # ------------------------------------------------------------------
    # Main AST traversal
    # ------------------------------------------------------------------
    def update_logical_exp(self, tree, logical_exp, obj):
        if tree is None:
            return

        # --- LoopExp: forAll, exists, select, reject, collect ---
        if isinstance(tree, LoopExp):
            source = tree.source
            if obj.classifier.name == self.context_name:
                self._handle_loop(tree, obj, logical_exp, source)
            return

        # --- IfExp ---
        if isinstance(tree, IfExp):
            self._handle_if(tree, obj, logical_exp)
            return

        # --- OperationCallExpression ---
        if isinstance(tree, OperationCallExpression):
            name = tree.name

            # Binary logical operations (new AST nodes from visitor)
            if name == "AND_BINARY":
                logical_exp[0] += "("
                self.update_logical_exp(tree.arguments[0], logical_exp, obj)
                logical_exp[0] += " and "
                self.update_logical_exp(tree.arguments[1], logical_exp, obj)
                logical_exp[0] += ")"
                return

            if name == "OR_BINARY":
                logical_exp[0] += "("
                self.update_logical_exp(tree.arguments[0], logical_exp, obj)
                logical_exp[0] += " or "
                self.update_logical_exp(tree.arguments[1], logical_exp, obj)
                logical_exp[0] += ")"
                return

            if name == "XOR_BINARY":
                logical_exp[0] += "("
                self.update_logical_exp(tree.arguments[0], logical_exp, obj)
                logical_exp[0] += " ^ "
                self.update_logical_exp(tree.arguments[1], logical_exp, obj)
                logical_exp[0] += ")"
                return

            if name == "IMPLIES_BINARY":
                logical_exp[0] += "(not("
                self.update_logical_exp(tree.arguments[0], logical_exp, obj)
                logical_exp[0] += ") or ("
                self.update_logical_exp(tree.arguments[1], logical_exp, obj)
                logical_exp[0] += "))"
                return

            # Comparison / arithmetic operations
            if name == "Operation":
                self._handle_operation(tree, obj, logical_exp)
                return

            # Unary operations
            if name.startswith("unary_"):
                op = tree.operation
                logical_exp[0] += f" {op} "
                self.update_logical_exp(tree.arguments[0], logical_exp, obj)
                return

            # Size
            if name == "Size":
                self._handle_size(tree, obj, logical_exp)
                return

            # Includes / Excludes
            if name == "INCLUDES":
                self._handle_includes(tree, obj, logical_exp)
                return
            if name == "EXCLUDES":
                self._handle_excludes(tree, obj, logical_exp)
                return

            # OCL type checks
            if name == "OCLISTYPEOF":
                self._handle_ocl_is_type_of(tree, logical_exp)
                return

            # ALLInstances (handled when encountered as source)
            if name == "ALLInstances":
                return

            # Generic method call / dot method
            args = tree.arguments
            for arg in args:
                self._emit_value(arg, obj, logical_exp)
            return

        # --- Property (from structural metamodel) ---
        if isinstance(tree, Property):
            value = self.get_value(tree.name, obj)
            if value is not None:
                logical_exp[0] += str(value)
            return

        # --- Literal expressions ---
        if isinstance(tree, IntegerLiteralExpression):
            logical_exp[0] += str(tree.value)
            return
        if isinstance(tree, RealLiteralExpression):
            logical_exp[0] += str(tree.value)
            return
        if isinstance(tree, BooleanLiteralExpression):
            logical_exp[0] += str(tree.value)
            return
        if isinstance(tree, StringLiteralExpression):
            logical_exp[0] += '"' + str(tree.value) + '"'
            return
        if isinstance(tree, DateLiteralExpression):
            logical_exp[0] += self._handle_date_literal(tree)
            return

        # --- VariableExp ---
        if isinstance(tree, VariableExp):
            return

    # ------------------------------------------------------------------
    # Handlers for specific AST node types
    # ------------------------------------------------------------------
    def _handle_operation(self, tree, obj, logical_exp):
        """Handle comparison and arithmetic operations."""
        args = tree.arguments
        for arg in args:
            if isinstance(arg, InfixOperator):
                logical_exp[0] += " " + str(arg) + " "
            elif isinstance(arg, OperationCallExpression):
                self.update_logical_exp(arg, logical_exp, obj)
            elif isinstance(arg, LoopExp):
                self.update_logical_exp(arg, logical_exp, obj)
            elif isinstance(arg, Property):
                value = self.get_value(arg.name, obj)
                if value is not None:
                    logical_exp[0] += str(value)
            elif isinstance(arg, IntegerLiteralExpression):
                logical_exp[0] += str(arg.value)
            elif isinstance(arg, RealLiteralExpression):
                logical_exp[0] += str(arg.value)
            elif isinstance(arg, BooleanLiteralExpression):
                logical_exp[0] += str(arg.value)
            elif isinstance(arg, StringLiteralExpression):
                logical_exp[0] += '"' + str(arg.value) + '"'
            elif isinstance(arg, DateLiteralExpression):
                logical_exp[0] += self._handle_date_literal(arg)
            else:
                self._emit_value(arg, obj, logical_exp)

    def _handle_size(self, tree, obj, logical_exp):
        """Handle size() operations."""
        source = tree.source
        if isinstance(source, Property):
            result = self.check_in_obj(obj, source)
            if result is None:
                result = self.check_in_link_ends(obj, source)
            if isinstance(result, list):
                logical_exp[0] += str(len(result))
            elif result is not None:
                value = self.get_value(source.name, result)
                logical_exp[0] += str(len(value))
            else:
                logical_exp[0] += "0"
        elif isinstance(source, LoopExp):
            loop_source = source.source
            if loop_source is not None and isinstance(loop_source, OperationCallExpression) and loop_source.name == "ALLInstances":
                class_name = loop_source.source.name
                all_objs = self.get_valid_objects(class_name, self.om)
            elif loop_source is not None:
                all_objs = self.check_in_obj(obj, loop_source)
                if all_objs is None:
                    all_objs = self.check_in_link_ends(obj, loop_source)
            else:
                all_objs = []
            # When size() is applied to any loop, count matching objects
            if source.name in ("collect", "select", "exists", "forAll", "reject"):
                self._handle_filter_loop(source, all_objs)
            if len(self.all_obj_sat) > 0:
                logical_exp[0] += str(len(self.all_obj_sat[-1]))
                self.all_obj_sat.pop()
            else:
                logical_exp[0] += "0"
        elif isinstance(source, OperationCallExpression):
            # Size on nested expression result
            self.update_logical_exp(source, logical_exp, obj)
        else:
            logical_exp[0] += "0"

    def _handle_filter_loop(self, tree, all_objs):
        """Handle collect/select/reject for size() counting."""
        self.all_obj_sat.append([])
        for o in all_objs:
            expression = [""]
            if len(tree.get_body) > 0:
                self.update_logical_exp(tree.get_body[0], expression, o)
                self._preprocess(expression)
                result = eval(expression[0])
                if tree.name == "reject":
                    if result is False:
                        self.all_obj_sat[-1].append(o)
                else:
                    if result is True:
                        self.all_obj_sat[-1].append(o)

    def _handle_includes(self, tree, obj, logical_exp):
        args = tree.arguments
        self._safe_add(logical_exp, " and ")
        logical_exp[0] += " [ "
        self._handle_property_set(tree.source, obj, logical_exp)
        logical_exp[0] += " ] in "
        if len(args) >= 1:
            logical_exp[0] += " [ "
            self._handle_property_set(args[0], obj, logical_exp, right_side=True)
            logical_exp[0] += " ]"

    def _handle_excludes(self, tree, obj, logical_exp):
        args = tree.arguments
        self._safe_add(logical_exp, " and ")
        logical_exp[0] += " [ "
        self._handle_property_set(tree.source, obj, logical_exp)
        logical_exp[0] += " ] not in "
        if len(args) >= 1:
            logical_exp[0] += " [ "
            self._handle_property_set(args[0], obj, logical_exp, right_side=True)
            logical_exp[0] += " ]"

    def _handle_property_set(self, source, obj, logical_exp, right_side=False):
        """Build a set representation for includes/excludes."""
        if isinstance(source, Property):
            all_objs = self.check_in_obj(obj, source)
            if all_objs is None:
                all_objs = self.check_in_link_ends(obj, source)
            if not isinstance(all_objs, list):
                all_objs = [all_objs] if all_objs is not None else []
            for index, o in enumerate(all_objs):
                if len(all_objs) > 1 or right_side:
                    logical_exp[0] += " [ "
                for i, slot in enumerate(o.slots):
                    logical_exp[0] += '"' + str(slot.attribute.name) + str(slot.value.value) + '"'
                    if i < len(o.slots) - 1:
                        logical_exp[0] += ","
                if not right_side:
                    if len(all_objs) > 1 and index < len(all_objs) - 1:
                        logical_exp[0] += " ], "
                else:
                    logical_exp[0] += " ] "
                    if len(all_objs) > 1 and index < len(all_objs) - 1:
                        logical_exp[0] += " , "

    def _handle_if(self, tree, obj, logical_exp):
        temp_exp = [""]
        self.update_logical_exp(tree.ifCondition, temp_exp, obj)
        self._preprocess(temp_exp)
        self._safe_add(logical_exp, " and ")
        if eval(temp_exp[0]) is True:
            self.update_logical_exp(tree.thenExpression, logical_exp, obj)
        else:
            self.update_logical_exp(tree.elseCondition, logical_exp, obj)

    def _handle_loop(self, tree, obj, logical_exp, source):
        """Handle loop expressions (forAll, exists, select, reject, collect)."""
        all_objs = self._resolve_source_objects(source, obj)
        expression_type = tree.name

        if expression_type == "forAll":
            logical_exp[0] += " ("
            for i, o in enumerate(all_objs):
                if len(tree.get_body) > 0:
                    self.update_logical_exp(tree.get_body[0], logical_exp, o)
                    if i < len(all_objs) - 1:
                        logical_exp[0] += " and "
            logical_exp[0] += " )"
        elif expression_type == "exists":
            logical_exp[0] += " ( "
            temp = logical_exp[0]
            for i, o in enumerate(all_objs):
                if len(tree.get_body) > 0:
                    self.update_logical_exp(tree.get_body[0], logical_exp, o)
                    if i < len(all_objs) - 1:
                        logical_exp[0] += " or "
            if temp == logical_exp[0]:
                logical_exp[0] += " False "
            logical_exp[0] += " )"
        elif expression_type in ("collect", "select", "reject"):
            self._handle_filter_loop(tree, all_objs)

    def _handle_ocl_is_type_of(self, tree, logical_exp):
        if isinstance(tree.source, Property):
            source_type = tree.source.type.name
            self._safe_add(logical_exp, " and ")
            for i, arg in enumerate(tree.arguments):
                arg_name = arg.name
                type_map = {
                    "String": "str", "Integer": "int",
                    "Boolean": "bool", "Real": "float",
                }
                mapped = type_map.get(arg_name, arg_name)
                logical_exp[0] += f'"{source_type}" == "{mapped}"'
                if 0 < i < len(tree.arguments) - 1:
                    self._safe_add(logical_exp, " and ")

    def _handle_date_literal(self, date_expr):
        now = datetime.now()
        date_str = str(date_expr)
        if "addDays" in date_str:
            days = date_str.split("addDays")[1].replace(")", "").replace("(", "")
            now = now + timedelta(days=int(days))
        if "today" in date_str:
            return str(int(now.strftime("%Y%m%d")))
        return str(int(now.strftime("%Y%m%d")))

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def _emit_value(self, arg, obj, logical_exp):
        """Emit a value into the logical expression."""
        if isinstance(arg, InfixOperator):
            logical_exp[0] += " " + str(arg) + " "
        elif isinstance(arg, Property):
            value = self.get_value(arg.name, obj)
            if value is not None:
                logical_exp[0] += str(value)
        elif isinstance(arg, (IntegerLiteralExpression, RealLiteralExpression, BooleanLiteralExpression)):
            logical_exp[0] += str(arg.value)
        elif isinstance(arg, StringLiteralExpression):
            logical_exp[0] += '"' + str(arg.value) + '"'
        elif isinstance(arg, DateLiteralExpression):
            logical_exp[0] += self._handle_date_literal(arg)
        elif isinstance(arg, (OperationCallExpression, LoopExp, IfExp)):
            self.update_logical_exp(arg, logical_exp, obj)
        else:
            logical_exp[0] += str(arg)

    def _safe_add(self, logical_exp, connector):
        """Add a connector (and/or) only if not already present."""
        s = logical_exp[0]
        if connector == " and ":
            if len(s) > 0 and not s.rstrip().endswith("and") and not s.rstrip().endswith("("):
                logical_exp[0] += connector
        elif connector == " or ":
            if len(s) > 0 and not s.rstrip().endswith("or") and not s.rstrip().endswith("("):
                logical_exp[0] += connector

    def _preprocess(self, exp):
        """Preprocess the logical expression before eval."""
        exp[0] = re.sub(r'(?<![<>=!])\s*=\s*(?![<>=])', ' == ', exp[0]).replace('<>', ' != ')
        # Trim trailing connectors
        s = exp[0].rstrip()
        if s.endswith(" and"):
            exp[0] = s[:-4]
        elif s.endswith(" or"):
            exp[0] = s[:-3]
