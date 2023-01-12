from lexer import Token


class ExpressionNode:
    pass


class StatementNode(ExpressionNode):
    def __init__(self) -> None:
        super().__init__()
        self.codeStrings = []

    def addNode(self, node: ExpressionNode):
        self.codeStrings.append(node)


class VariableNode(ExpressionNode):
    def __init__(self, variable: Token) -> None:
        super().__init__()
        self.variable: Token = variable


class NumberNode(ExpressionNode):
    def __init__(self, number: Token) -> None:
        super().__init__()
        self.number: Token = number


class BinOperatorNode(ExpressionNode):
    def __init__(self, operator: Token, leftNode: ExpressionNode, rightNode: ExpressionNode) -> None:
        super().__init__()
        self.operator: Token = operator
        self.leftNode: ExpressionNode = leftNode
        self.rightNode: ExpressionNode = rightNode


class UnarOperatorNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode) -> None:
        super().__init__()
        self.operator: Token = operator
        self.operand: ExpressionNode = operand
