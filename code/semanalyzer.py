from lexer import Token
from nodes import *


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.maybeElseLevels = set()
        self.variables = set()
        self.level = 0

    def checkNode(self, node: ExpressionNode) -> None:
        if type(node) != ElseNode and type(node) != BlockNode:
            self.maybeElseLevels.discard(self.level)

        if type(node) == ElseNode:
            if self.level not in self.maybeElseLevels:
                raise SyntaxError(f'unexpected \'else\'')

            self.maybeElseLevels.discard(self.level)

            for subnode in node.body:
                self.level += 1
                self.checkNode(subnode)
                self.level -= 1

        elif type(node) == BlockNode:
            self.checkNode(node.statement)

            if node.operator.value == 'if':
                self.maybeElseLevels.add(self.level)
                for subnode in node.body:
                    self.level += 1
                    self.checkNode(subnode)
                    self.level -= 1

            else:
                for subnode in node.body:
                    self.level += 1
                    self.checkNode(subnode)
                    self.level -= 1

        elif type(node) == BinOperatorNode:
            if node.operator.type == 'ASSIGN':
                self.variables.add(node.leftNode.value.value)
                self.checkNode(node.rightNode)
            else:
                self.checkNode(node.leftNode)
                self.checkNode(node.rightNode)

        elif type(node) == UnarOperatorNode:
            self.checkNode(node.operand)

        elif type(node) == ValueNode and node.value.type == 'VARIABLE' and node.value.value not in self.variables:
            raise NameError(f'name {node.value.value!r} is not defined')

    def check(self, root: StatementNode) -> None:
        for node in root.codeStrings:
            self.checkNode(node)
