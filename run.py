import sys, readline
"""
Valid Token Types:
".+" - STRING
[-]?[0-9,.]+ - NUMBER
variable style is 1 letter and then any combination of numbers/letters.
a variable assignment is done using 'var' first, a space, then the name, space, equals, space, value
a function call is ! and then a variable style name.
a function definition starts with "define" and then a valid variable name, followed by brackets containing code, C style.
"""

digits = ["0","1","2","3","4","5","6","7","8","9"]
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower() + "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alphanumeric = digits + letters

class Token(object):
    def __init__(self, token_type, value=""):
        self.type = token_type
        self.value = value
    def __str__(self):
        return "{}:'{}'".format(self.type,self.value)

class Function(object):
    def __init__(self, code):
        self.code = code

def parse_char(code, pos):
    cur_char = code[pos]
    token = Token("UNDEFINED")
    if(cur_char == '"'):
        token.type = "STRING"
        value = ""
        pos += 1
        while(code[pos] != '"'):
            token.value += code[pos]
            pos += 1
        pos += 1
    elif(cur_char in ["-","+"]):
        pos += 1
        if(code[pos] in digits):
            token.type = "NUMBER"
            token.value = code[pos]
            pos += 1
            while(code[pos] in digits):
                token.value += code[pos]
                pos += 1
    elif(cur_char == "v"):
        pos += 1
        if(code[pos] == "a"):
            pos += 1
            if(code[pos] == "r"):
                pos += 1
                token.type = "VAR_DEF"
                token.value = "var"
            else:
                raise SyntaxError
        else:
            raise SyntaxError
    elif(cur_char in letters):
        token.type = "VAR"
        token.value = code[pos]
        pos += 1
        while(code[pos] in alphanumeric):
            token.value += code[pos]
            pos += 1
    elif(cur_char == "="):
        token.type = "EQUALS"
        token.value = "="
        pos += 1
    elif(cur_char == " "):
        token.type = "SPACE"
        token.value = " "
        pos += 1
    elif(cur_char == "!"):
        token.type = "FUN_CALL"
        token.value = "!"
        pos += 1
    elif(cur_char == ";"):
        token.type = "SEMICOLON"
        token.value = ";"
        pos += 1
    elif(cur_char == "@"):
        pos += 1
        if(code[pos] == "{"):
            pos += 1
            token.type = "PY_CALL"
            while(code[pos] != "}"):
                token.value += code[pos]
                pos += 1
            pos += 1
        else:
            raise SyntaxError
    elif(cur_char == "$"):
        pos += 1
        if(code[pos] == "{"):
            pos += 1
            token.type = "FUN_DEF"
            while(code[pos] != "}"):
                token.value += code[pos]
                pos += 1
            pos += 1
        else:
            raise SyntaxError
    else:
        raise SyntaxError #this is the worst way of doing this
    return (token, pos)

def parse(code,debug=0):
    tokens = []
    pos = 0
    while(pos <= len(code)-1):
        try:
            response = parse_char(code, pos)
        except IndexError:
            if(debug):
                raise
            print("Unexpected EOL.")
            sys.exit(0)
        except SyntaxError:
            print("Unknown character.")
            if(debug):
                raise
            sys.exit(0)
        if(response == "END"):
            break
        tokens.append(response[0])
        pos = response[1]
    print("Finished parsing.")
    return tokens

def run_token(tkns, variables, pos):
    cur_type = tkns[pos].type
    if(cur_type == "VAR_DEF"):
        pos += 1
        if(tkns[pos].type == "SPACE"):
            pos += 1
            if(tkns[pos].type == "VAR"):
                pos += 1
                if(tkns[pos].type == "SPACE"):
                    pos += 1
                    if(tkns[pos].type == "EQUALS"):
                        pos += 1
                        if(tkns[pos].type == "SPACE"):
                            pos += 1
                            if(tkns[pos].type == "STRING"):
                                variables[tkns[pos-4].value] = tkns[pos].value
                                pos += 1
                            elif(tkns[pos].type == "NUMBER"):
                                variables[tkns[pos-4].value] = float(tkns[pos].value)
                                pos += 1
                            elif(tkns[pos].type == "FUN_DEF"):
                                variables[tkns[pos-4].value] = Function(tkns[pos].value)
                                pos += 1
                            else:
                                raise SyntaxError #no literal
                        else:
                            raise SyntaxError #no space
                    else:
                        raise SyntaxError # no equals
                else:
                    raise SyntaxError #no var name
            else:
                raise SyntaxError #no space
        else:
            raise SyntaxError #no 'var'
    elif(cur_type == "FUN_CALL"):
        pos += 1
        if(tkns[pos].type == "VAR"):
            fun_name = tkns[pos].value
            tokens = parse(variables[fun_name].code)
            run_tokens(tokens)
            pos += 1
        else:
            raise SyntaxError
    elif(cur_type == "SPACE"):
        pos += 1
    elif(cur_type == "SEMICOLON"):
        pos += 1
    elif(cur_type == "PY_CALL"):
        exec(tkns[pos].value)
        pos += 1
    else:
        raise SyntaxError(tkns[pos])
    return [variables, pos]

def run_tokens(tokens,debug=0):
    if(debug):
        output = ""
        for x in tokens:
            output += str(x) + ", "
        print(output)
    pos = 0
    variables = {}
    functions = {}
    while(pos <= len(tokens)-1):
        try:
            response = run_token(tokens, variables, pos)
        except SyntaxError:
            print("Syntax error - those two things probably don't go next to each other.")
            sys.exit(0)
        except IndexError:
            print("Unexpected EOL.")
            sys.exit(0)
        variables = {**variables, **response[0]}
        pos = response[1]
    if(debug):
        print(variables)


def run(code,debug=0):
    tokens = parse(code,debug=debug)
    run_tokens(tokens,debug=debug)

run(input("> "),debug=1)
