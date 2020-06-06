import fire
from logic import *
levels = {
    'NOT' : "'", #not
    'AND' : "*", #and
    'NAND': ".", #nand
    'XOR' : "^", #xor
    'OR' : "+", # or
    'NOR' : "-" # nor
}
class Program:
    def welcome(self, welcome_file):
        '''
        A short welcome to all good people
        '''
        with open(welcome_file) as f:
            welcome_string = f.read()
        print(welcome_string)
    def generateTable(self, expr_str):
        try:
            expr = parse(expr_str)
        except:
            raise ValueError('Some of the chars in expretion have not been recognized. There may be an error in parssing the expresion.')
        print(Table.GetTable(expr, expr_str))
    
    def generateLogicFromTable(self):
        print('On first line input vars. They must be only singel upercase letters. Seperate them by tabs')
        hdrs = input().split()
        print('Now enter values in 1 and 0. New line is registered by enter Split them by tab. When done, just press enter.')
        vls = []
        while(True):
            inpt = input()
            if(inpt == ''):
                break
            inp = [bool(x) for x in inpt.split()]
            vls.append(inp)
        tbl = Table(hdrs, vls)
        print(tbl.getLogic().ToText(levels))
    
    def genPyFunction(self, expr_str):
        try:
            expr = parse(expr_str)
        except:
            raise ValueError('Some of the chars in expretion have not been recognized. There may be an error in parssing the expresion.')
        print(GeneratePython(expr))

    def genCFunction(self, expr_str):
        try:
            expr = parse(expr_str)
        except:
            raise ValueError('Some of the chars in expretion have not been recognized. There may be an error in parssing the expresion.')
        print(GenerateCPlusPlus(expr))
if __name__ == "__main__":
    fire.Fire(Program)