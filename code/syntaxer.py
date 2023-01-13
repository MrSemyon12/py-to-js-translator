from lexer import Token
from nodes import *


class SyntaxAnalyser:
    def __init__(self, tokens: list) -> None:
        self.tokens = tokens
        self.pos = 0
        self.level = 0

    def match(self, *expected) -> Token | None:
        if self.pos < len(self.tokens):
            currentToken = self.tokens[self.pos]
            if currentToken.type in expected:
                self.pos += 1
                return currentToken
        return None

    def require(self, *expected) -> Token:
        token = self.match(*expected)
        if not token:
            raise RuntimeError(f'unexpected token on position {self.pos}')
        return token

    def parseVariableOrNumber(self) -> ExpressionNode:
        number = self.match('NUMBER')
        if number:
            return NumberNode(number)
        variable = self.match('VARIABLE')
        if variable:
            return VariableNode(variable)
        raise RuntimeError(f'unexpected token on position {self.pos}')

    def parseFunc(self):
        function = self.match('FUNC')
        if function and self.match('LPAR'):
            operand = self.parseFormula()
            self.require('RPAR')
            return UnarOperatorNode(function, operand)
        raise RuntimeError(f'unexpected token on position {self.pos}')

    def parseLog(self):
        operator = self.match('LOG')
        if operator:
            return UnarOperatorNode(operator, self.parseFormula())
        raise RuntimeError(f'unexpected token on position {self.pos}')

    def parseBlock(self):
        pass

    def parseParenthesis(self) -> ExpressionNode:
        if self.match('FUNC'):
            self.pos -= 1
            return self.parseFunc()

        if self.match('LPAR'):
            formulaNode = self.parseFormula()
            self.require('RPAR')
            return formulaNode

        return self.parseVariableOrNumber()

    def parseFormula(self) -> ExpressionNode:
        leftNode = self.parseParenthesis()
        operator = self.match('OPERATOR')
        while operator:
            rightNode = self.parseParenthesis()
            leftNode = BinOperatorNode(operator, leftNode, rightNode)
            operator = self.match('OPERATOR')
        return leftNode

    def parseExpression(self) -> ExpressionNode:
        if self.match('VARIABLE'):
            self.pos -= 1
            variableNode = self.parseVariableOrNumber()
            assignOperator = self.match('ASSIGN')
            if assignOperator:
                formulaNode = self.parseFormula()
                binaryNode = BinOperatorNode(
                    assignOperator, variableNode, formulaNode)
                return binaryNode
            raise RuntimeError(f'unexpected token on position {self.pos}')

        elif self.match('LOG'):
            self.pos -= 1
            return self.parseLog()

        elif self.match('FUNC'):
            self.pos -= 1
            return self.parseFunc()

        # elif match('BLOCK'):
        #     return parseBlock()

        # elif match('NEWLINE'):
        #     pass

    def parse(self) -> StatementNode:
        root = StatementNode()

        while self.pos < len(self.tokens):
            codeStringNode = self.parseExpression()
            self.require('NEWLINE')
            root.addNode(codeStringNode)

        return root

    def getNode(self, node: ExpressionNode) -> str:
        nodeType = type(node)

        if nodeType == VariableNode:
            return '-' * self.level + f'{node.variable.type} {node.variable.value}\n'
        elif nodeType == NumberNode:
            return '-' * self.level + f'{node.number.type} {node.number.value}\n'
        elif nodeType == BinOperatorNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            self.level += 1
            res += f'{self.getNode(node.leftNode)}{self.getNode(node.rightNode)}'
            self.level -= 1
            return res
        elif nodeType == UnarOperatorNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            self.level += 1
            res += f'{self.getNode(node.operand)}'
            self.level -= 1
            return res

    def getTree(self, root: StatementNode) -> str:
        textTree = ''

        for line in root.codeStrings:
            if line:
                textTree += self.getNode(line)

        return textTree
