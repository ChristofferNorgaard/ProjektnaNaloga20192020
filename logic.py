from itertools import product
from tabulate import tabulate
symbl = {
    'NOT' : 'not',
    'AND': 'and',
    'NAND': 'nand',
    'XOR': 'xor',
    'OR': 'or',
    'NOR': 'nor'

}
con_tab = [
    [],
    [],
    [],
    [],
    [],
    [],
]
class Operation:
    levels_class = {
        'VAR' : 7,
        'VALUE' : 7,
        'NOT' : 6,
        'AND': 5,
        'NAND': 4,
        'XOR': 3,
        'OR': 2,
        'NOR': 1
    }
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def getVars(self):
        return list(dict.fromkeys(self.left.getVars() + self.right.getVars()))

    def ToText(self, symbl):
        text_left = self.left.ToText(symbl)
        text_right = self.right.ToText(symbl)
        if self.levels_class[self.__class__.__name__] > self.levels_class[self.left.__class__.__name__]:
            text_left = '(' + text_left + ')'
        if self.levels_class[self.__class__.__name__] > self.levels_class[self.right.__class__.__name__]:
            text_right = '(' + text_right + ')'
        if(self.__class__.__name__ + '-prefix' in symbl.keys()):
            return symbl[self.__class__.__name__ + '-prefix'] + ' (' + text_left + ' ' + symbl[self.__class__.__name__] + ' ' + text_right + ')'
        return text_left + ' ' + symbl[self.__class__.__name__] + ' ' + text_right
        
class AND(Operation):
    def get(self, values):
        return self.left.get(values) and self.right.get(values)
    

class OR(Operation):
    def get(self, values):
        return self.left.get(values) or self.right.get(values)

class XOR(Operation):
    def get(self, values):
        return self.left.get(values) ^ self.right.get(values)

class NOR(Operation):
    def get(self, values):
        return not (self.left.get(values) or self.right.get(values))

class NAND(Operation):
    def get(self, values):
        return not (self.left.get(values) and self.right.get(values))

class NOT:
    def __init__(self, left):
        self.left = left
    
    def get(self, values):
        return not self.left.get(values)

    def getVars(self):
        return self.left.getVars()
    
    def ToText(self, symbl):
        text = self.left.ToText(symbl)
        if self.left.__class__.__name__ == 'VAR' or self.left.__class__.__name__ == 'VALUE':
            return symbl[self.__class__.__name__]+text
        else:
            return symbl[self.__class__.__name__] + '(' + text + ')'

class VAR:
    def __init__(self, name):
        self.name = name
    
    def get(self, values):
        return values[self.name]
    
    def getVars(self):
        return [self.name]
    
    def ToText(self, symbl):
        return self.name

class VALUE:
    def __init__(self, bin):
        self.bin = bool(bin)
    
    def get(self, values):
        return self.bin
    def getVars(self):
        return []
    
    def ToText(self, symbl):
        return str(int(self.bin))

levels = {
    '(' : 7,
    "'" : 6, #not
    "*":5, #and
    "." : 4, #nand
    "^": 3, #xor
    "+" : 2, # or
    "-": 1 # nor
}
definitions = {
    "'" : NOT,
    "*": AND, #and
    "." : NAND, #nand
    "^": XOR, #xor
    "+" : OR, # or
    "-": NOR # nor
}
def Multipler(operations_list, mul_class):
    acum = []
    for i in operations_list:
        if len(acum) == 0:
            acum.append(i)
        else:
            acum.append(i)
            a, b = acum.pop(), acum.pop()
            acum.append(mul_class(a, b))
    if(len(acum) != 1):
        raise ValueError('the lenght of return in Multipler is not 0')
    return acum[0]
class Table:
    def __init__(self, headers, values):
        self.headers = headers
        self.values = values
    
    def __str__(self):
        return str(tabulate(self.values, headers=self.headers, tablefmt="grid"))

    def GetTable(expr, expr_str):
        elements = expr.getVars()
        elements.sort()
        values = product(*([0,1] for i in range(len(elements))))
        table = []
        hdrs = (elements + [expr_str])
        for i in values:
            vls = {}
            for j in range(len(elements)):
                vls[elements[j]] = i[j]
            table.append(list(i) + [expr.get(vls)])
        return Table(hdrs, table)
    
    def getLogic(self):
        hd = {}
        lines = []
        for i in self.headers:
            hd[i] = VAR(i)
        for line in self.values:
            vals = []
            for value_index in range(len(hd.keys())):
                if(line[-1] == 1):
                    if(line[value_index]):
                        vals.append(hd[self.headers[value_index]])
                    else:
                        vals.append(NOT(hd[self.headers[value_index]]))
            if(vals):
                lines.append(Multipler(vals, AND))
        
        return Multipler(lines, OR)

def parse(expr_str):
    expr_str = list(expr_str)
    vals = []
    operators = []
    while(len(expr_str)>0):
        #print(operators)
        char = expr_str.pop(0)
        #print(char)
        if(char == '1' or char == '0'):
            vals.append(VALUE(bool(char)))
        elif(char in levels.keys()):
            while(operators and levels[char] <= levels[operators[-1]] and operators[-1] != '('):
                op = operators.pop()
                if op == 'n':
                    a= vals.pop()
                    vals.append(NOT(a))
                    #print('appended not')
                elif op in definitions:
                    a, b = vals.pop(), vals.pop()
                    vals.append(definitions[op](a, b))
                    #print('Appended ' + str(definitions[op](a, b)))
                else:
                    raise ValueError('The value of ' + op + 'has not been expected for.')
            operators.append(char)
        elif(char == '('):
            operators.append(char)
        elif(char == ')'):
            
            while(operators[-1] != '('):
                op = operators.pop()
                if op == 'n':
                    a= vals.pop()
                    vals.append(NOT(a))
                    #print('appended not')
                elif op in definitions:
                    a, b = vals.pop(), vals.pop()
                    vals.append(definitions[op](a, b))
                    #print('Appended ' + str(definitions[op](a, b)))
                else:
                    raise ValueError('The value of ' + op + ' has not been expected for.')
            #print(operators[-1])
            if(operators[-1] == '('):
                del operators[-1]
        elif(char.isupper()):
            vals.append(VAR(char))
        elif(char == ' '):
            pass
        else:
            raise ValueError('the ' + char + ' has not been expected.')
    if(len(expr_str)==0):
        while(operators):
            op = operators.pop()
            if op == 'n':
                a= vals.pop()
                vals.append(NOT(a))
                print('Appended not')
            elif op in definitions:
                a, b = vals.pop(), vals.pop()
                vals.append(definitions[op](a, b))
                print('Appended ' + str(definitions[op](a, b)))
            elif op == ')' or op == '(' :
                pass
            else:
                raise ValueError('The value of ' + op + 'has not been expected for.')
    return vals[0]

def GeneratePython(expr):
    symbl = {
    'NOT' : 'not ',
    'AND': 'and',
    'NAND': 'and',
    'NAND-prefix' : 'not ',
    'XOR': '^',
    'OR': 'or',
    'NOR': 'or',
    'NOR-prefix' : 'not '
    }
    string = 'def function(' + ','.join(expr.getVars()) + '):\n'
    string += '\t' + 'return ' + expr.ToText(symbl)
    return string
def GenerateCPlusPlus(expr):
    symbl = {
        'NOT' : '!',
        'AND': '&&',
        'NAND': '&&',
        'NAND-prefix' : '!',
        'XOR': '^',
        'OR': '||',
        'NOR': '||',
        'NOR-prefix' : '!'
    }
    return 'bool function('+ ','.join(' bool ' + x for x in expr.getVars()) + '){ retrun(' + expr.ToText(symbl) + ')}'
