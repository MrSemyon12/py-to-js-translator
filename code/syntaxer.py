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

    def parseValue(self) -> ExpressionNode:
        value = self.match('NUMBER', 'VARIABLE', 'BOOL', 'STRING')
        if value:
            return ValueNode(value)
        raise RuntimeError(f'unexpected token on position {self.pos}')

    def parseFunc(self) -> ExpressionNode:
        function = self.match('FUNC')
        if function and self.match('LPAR'):
            operand = self.parseFormula()
            self.require('RPAR')
            return UnarOperatorNode(function, operand)
        raise RuntimeError(f'unexpected token on position {self.pos}')

    def parseLog(self) -> ExpressionNode:
        operator = self.match('LOG')
        if operator:
            return UnarOperatorNode(operator, self.parseFormula())
        raise RuntimeError(f'unexpected token on position {self.pos}')

    def parseBlock(self) -> ExpressionNode:
        block = BlockNode(self.match('BLOCK'), self.parseFormula())
        self.require('COLON')
        self.require('NEWLINE')
        self.level += 1
        while self.match('TAB'):
            expression = self.parseExpression()
            self.require('NEWLINE')
            block.addNode(expression)

        self.level -= 1
        self.pos -= 1
        return block

    def parseParenthesis(self) -> ExpressionNode:
        if self.match('FUNC'):
            self.pos -= 1
            return self.parseFunc()

        if self.match('LPAR'):
            formulaNode = self.parseFormula()
            self.require('RPAR')
            return formulaNode

        return self.parseValue()

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
            variableNode = self.parseValue()
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

        elif self.match('BLOCK'):
            self.pos -= 1
            return self.parseBlock()

        elif self.level >= 2:
            for _ in range(self.level - 1):
                self.require('TAB')
            return self.parseExpression()

    def parse(self) -> StatementNode:
        root = StatementNode()

        while self.pos < len(self.tokens):
            expression = self.parseExpression()
            self.require('NEWLINE')
            root.addNode(expression)

        return root

    def getNode(self, node: ExpressionNode) -> str:
        nodeType = type(node)

        if nodeType == ValueNode:
            return '-' * self.level + f'{node.value.type} {node.value.value}\n'
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
        elif nodeType == BlockNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            res += '-' * self.level + f'STATE\n'
            self.level += 1
            res += f'{self.getNode(node.statement)}'
            self.level -= 1
            res += '-' * self.level + f'BODY\n'
            self.level += 1
            for line in node.body:
                res += f'{self.getNode(line)}'
            self.level -= 1
            return res

    def getTree(self, root: StatementNode) -> str:
        textTree = ''

        for line in root.codeStrings:
            if line:
                textTree += self.getNode(line)

        return textTree
