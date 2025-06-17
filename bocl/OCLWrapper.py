"""Including imports from BESSER and ANTLR4"""
from antlr4 import InputStream,CommonTokenStream,ParseTreeWalker
from besser.BUML.notations.ocl.BOCLLexer import BOCLLexer
from besser.BUML.notations.ocl.BOCLParser import BOCLParser
from besser.BUML.notations.ocl.BOCLListener import BOCLListener
from besser.BUML.notations.ocl.RootHandler import Root_Handler
from bocl.evaluator import Evaluator

class OCLWrapper:
    """The OCLWrapper class is the wrapper around the evaluator
    class to prepare the construct needed by evaluator.

    Args:
        dm: Domain model in BUML
        om: object model in BUML
    Attributes:
        dm: Domain model in BUML
        om: object model in BUML
    """
    def __init__(self,dm,om):
        self.dm = dm
        self.om = om
    def __str__(self):
        return str(self.dm)+ str(self.om)


    def evaluate(self,ocl):
        """the evaluate function takes the OCL constraint and evaluate using evaluator
        Args:
            ocl: Object of OCL class that constaints the OCL expression and context class
        """

        # self.preprocess(ocl.expression)
        input_stream = InputStream(ocl.expression)
        root_handler = Root_Handler(self.dm,self.om)
        root_handler.set_context(ocl.context)
        lexer = BOCLLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = BOCLParser(stream)
        tree = parser.oclFile()
        listener = BOCLListener(root_handler)
        walker = ParseTreeWalker()
        walker.walk(listener,tree)

        evaluator = Evaluator()

        return evaluator.evaluate(root_handler, self.om)
        # return True