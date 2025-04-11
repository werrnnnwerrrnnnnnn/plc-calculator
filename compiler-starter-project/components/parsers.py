from components.lexica import MyLexer
from components.memory import Memory
from sly import Parser

class PrefixParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", MINUS),
        ('left', TIMES, DIVIDE, MOD),
    )

    def __init__(self, output_widget=None):
        self.memory = Memory()
        self.infix_stack = []  # stack to build infix expr

    def get_infix(self):
        return self.infix_stack[0] if self.infix_stack else ""

    @_('NAME ASSIGN expr')
    def statement(self, p):
        var_name = p.NAME
        value = p.expr
        self.memory.set(variable_name=var_name, value=value, data_type=type(value))
        self.infix_stack = [f"{var_name} = {self.infix_stack[0]}"]  # Update infix with assignment
    
    # S -> E
    @_('expr')
    def statement(self, p) -> int:
        result = p.expr
        return result

    # E -> + E E
    @_('"+" expr expr')
    def expr(self, p):
        print("PLUS+++++", p)
        result = p.expr0 + p.expr1
        # Pop two infix sub-expressions and combine them
        right = self.infix_stack.pop()
        left = self.infix_stack.pop()

        self.infix_stack.append(f"({left} + {right})")
        return result

    # E -> * E E
    @_('TIMES expr expr')
    def expr(self, p):
        print("TIMES*****", p)
        result = p.expr0 * p.expr1

        right = self.infix_stack.pop()
        left = self.infix_stack.pop()

        self.infix_stack.append(f"({left} * {right})")
        return result
    
    # E -> % E E
    @_('MOD expr expr')
    def expr(self, p):
        print("MOD%%%%%%", p)
        result = p.expr0 % p.expr1

        right = self.infix_stack.pop()
        left = self.infix_stack.pop()

        self.infix_stack.append(f"({left} % {right})")
        return result

    # E -> number
    @_('NUMBER')
    def expr(self, p):
        print("NUMBER====", p)
        num = int(p.NUMBER)
        self.infix_stack.append(str(num))
        return num

    def parse(self, tokens):
        self.infix_stack = []  # reset
        return super().parse(tokens)

from components.ast.statement import Expression, Expression_math, Expression_number, Operations
class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", MINUS),
        # ('left', TIMES, DIVIDE),
        # ('right', UMINUS),
        )

    @_('expr')
    def statement(self, p) -> int:
        p.expr.run()
        return p.expr.value

    @_('expr "+" expr')
    def expr(self, p) -> Expression:
        parameter1 = p.expr0
        parameter2 = p.expr1
        expr = Expression_math(operation=Operations.PLUS, parameter1=parameter1, parameter2=parameter2)
        return expr
    
    @_('expr MINUS expr')
    def expr(self, p) -> Expression:
        parameter1 = p.expr0
        parameter2 = p.expr1
        expr = Expression_math(operation=Operations.MINUS, parameter1=parameter1, parameter2=parameter2)
        return expr

    @_('NUMBER')
    def expr(self, p) -> Expression:
        return Expression_number(number=p.NUMBER)
        
if __name__ == "__main__":
    lexer = MyLexer()
    # parser = MyParser()
    text = "9 + 2 + 3"
    memory = Memory()
    parser = ASTParser()
    # text = "1 + 2 + 3"
    result = parser.parse(lexer.tokenize(text))
    print(result)
    # print(memory)