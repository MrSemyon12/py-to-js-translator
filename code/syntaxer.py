from lexer import Token
from nodes import *


class SyntaxAnalyzer:
    def __init__(self, tokens: list) -> None:
        self.tokens = tokens
        self.pos = 0
        self.level = 0

    def match(self, *expected) -> Token or None:
        if self.pos < len(self.tokens):
            currentToken = self.tokens[self.pos]
            if currentToken.type in expected:
                self.pos += 1
                return currentToken
        return None

    def require(self, *expected) -> Token:
        token = self.match(*expected)
        if not token:
            raise SyntaxError(f'expected {expected[0]} on position {self.pos}')
        return token

    def parseValue(self) -> ExpressionNode:
        return ValueNode(self.require('NUMBER', 'VARIABLE', 'BOOL', 'STRING'))

    def parseFunc(self) -> ExpressionNode:
        function = self.match('FUNC')
        if function:
            self.require('LPAR')
            operand = self.parseFormula()
            self.require('RPAR')
            return UnarOperatorNode(function, operand)
        raise SyntaxError(f'expected \'FUNC\' on position {self.pos}')

    def parseLog(self) -> ExpressionNode:
        return UnarOperatorNode(self.require('LOG'), self.parseFormula())

    def parseTab(self) -> bool:
        cnt = 0
        for _ in range(self.level):
            if not self.match('TAB'):
                self.pos -= cnt
                return False
            cnt += 1
        return True

    def parseBlock(self) -> ExpressionNode:
        blockToken = self.match('BLOCK')
        if blockToken.value == 'else':
            block = ElseNode(blockToken)
        else:
            block = BlockNode(blockToken, self.parseFormula())
        self.require('COLON')
        self.require('NEWLINE')
        self.level += 1
        while self.parseTab():
            expression = self.parseExpression()
            block.addNode(expression)
            self.require('NEWLINE')

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
            else:
                self.pos -= 1
                return self.parseFormula()

        elif self.match('LOG'):
            self.pos -= 1
            return self.parseLog()

        elif self.match('FUNC'):
            self.pos -= 1
            return self.parseFunc()

        elif self.match('BLOCK'):
            self.pos -= 1
            return self.parseBlock()

        elif self.match('NUMBER', 'VARIABLE', 'BOOL', 'STRING'):
            self.pos -= 1
            return self.parseFormula()

    def parse(self) -> StatementNode:
        root = StatementNode()

        while self.pos < len(self.tokens):
            expression = self.parseExpression()
            self.require('NEWLINE')
            root.addNode(expression)

        return root

    def getTextNode(self, node: ExpressionNode) -> str:
        nodeType = type(node)

        if nodeType == ValueNode:
            return '-' * self.level + f'{node.value.type} {node.value.value}\n'
        elif nodeType == BinOperatorNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            self.level += 1
            res += f'{self.getTextNode(node.leftNode)}{self.getTextNode(node.rightNode)}'
            self.level -= 1
            return res
        elif nodeType == UnarOperatorNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            self.level += 1
            res += f'{self.getTextNode(node.operand)}'
            self.level -= 1
            return res
        elif nodeType == BlockNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            res += '-' * self.level + f'STATE\n'
            self.level += 1
            res += f'{self.getTextNode(node.statement)}'
            self.level -= 1
            res += '-' * self.level + f'BODY\n'
            self.level += 1
            for line in node.body:
                res += f'{self.getTextNode(line)}'
            self.level -= 1
            return res
        elif nodeType == ElseNode:
            res = '-' * self.level + \
                f'{node.operator.type} {node.operator.value}\n'
            res += '-' * self.level + f'BODY\n'
            self.level += 1
            for line in node.body:
                res += f'{self.getTextNode(line)}'
            self.level -= 1
            return res

    def getTextTree(self, root: StatementNode) -> str:
        textTree = ''

        for line in root.codeStrings:
            if line:
                textTree += self.getTextNode(line)

        return textTree
