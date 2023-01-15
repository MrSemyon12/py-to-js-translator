from lexer import Token
from nodes import *


class CodeGenerator:
    def __init__(self) -> None:
        self.level = 0
        self.output = ''

    def genJavaScriptNode(self, node: ExpressionNode) -> None:
        pass

    def genJavaScript(self, root: StatementNode) -> str:
        for node in root.codeStrings:
            pass
