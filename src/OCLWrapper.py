from src.Evaluator import  Evaluator
from besser.BUML.notations.ocl.BOCLLexer import BOCLLexer
from besser.BUML.notations.ocl.BOCLParser import BOCLParser
from besser.BUML.notations.ocl.BOCLListener import BOCLListener
from besser.BUML.notations.ocl.RootHandler import Root_Handler
from antlr4 import *

class OCLWrapper:
    def __init__(self,dm,om):
        self.dm = dm
        self.om = om


    def evaluate(self,ocl):

        # self.preprocess(ocl.expression)
        input_stream = InputStream(ocl.expression)
        rootHandler = Root_Handler(ocl,self.dm,self.om)
        lexer = BOCLLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = BOCLParser(stream)
        tree = parser.oclFile()
        listener = BOCLListener(rootHandler)
        walker = ParseTreeWalker()
        walker.walk(listener,tree)

        eval = Evaluator()

        return eval.evaluate(rootHandler, self.om)

        pass