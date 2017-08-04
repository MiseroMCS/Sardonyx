import sys, readline

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

def get_var_type(var_value):
    if(type(var_value) == str):
        return "STRING"
    elif(type(var_value) == float):
        return "NUMBER"
    elif(type(var_value) == Function):
        return "FUN_DEF"


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
        elif(code[pos-1] == "+"):
            token.type = "ADD"
        elif(code[pos-1] == "-"):
            token.type = "SUB"

    elif(cur_char == "v"):
        pos += 1
        if(code[pos] == "a"):
            pos += 1
            if(code[pos] == "r"):
                pos += 1
                token.type = "VAR_DEF"
                token.value = "var"
            else:
                raise SyntaxError(pos)
        else:
            raise SyntaxError(pos)
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
            raise SyntaxError(pos)
    elif(cur_char == "$"):
        pos += 1
        if(code[pos] == "{"):
            pos += 1
            token.type = "FUN_DEF"
            opened_braces = 0
            while(code[pos] != "}" or opened_braces != 0):
                if(code[pos] == "{"):
                    opened_braces += 1
                if(code[pos] == "}"):
                    opened_braces -= 1
                token.value += code[pos]
                pos += 1
            pos += 1
        else:
            raise SyntaxError(pos)
    elif(cur_char == "("):
        token.type = "BEGIN_EXPR"
        pos += 1
    elif(cur_char == ")"):
        token.type = "END_EXPR"
        pos += 1
    elif(cur_char == "*"):
        token.type = "MULTIPLY"
        pos += 1
    elif(cur_char == "/"):
        token.type = "DIVIDE"
        pos += 1
    elif(cur_char == "%"):
        token.type = "MODULO"
        pos += 1
    else:
        raise SyntaxError(pos)
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
        except SyntaxError as e:
            print("Unknown character '{}' (column {}).".format(code[e.msg],e.msg))
            print(code)
            print(" "*e.msg + "^")
            if(debug):
                raise
            sys.exit(0)
        if(response == "END"):
            break
        tokens.append(response[0])
        pos = response[1]
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
                            varname = tkns[pos-4].value
                            if(tkns[pos].type == "STRING"):
                                variables[varname] = tkns[pos].value
                                pos += 1
                            elif(tkns[pos].type == "NUMBER"):
                                variables[varname] = float(tkns[pos].value)
                                pos += 1
                            elif(tkns[pos].type == "FUN_DEF"):
                                variables[varname] = Function(tkns[pos].value)
                                pos += 1
                            elif(tkns[pos].type == "VAR"):
                                var_value = variables[tkns[pos].value]
                                variables[varname] = variables[tkns[pos].value]
                                pos += 1
                            elif(tkns[pos].type == "BEGIN_EXPR"):
                                pos += 1
                                arg1 = tkns[pos]
                                operator = tkns[pos+2]
                                arg2 = tkns[pos+4]
                                pos += 6
                                if(arg1.type == "VAR"):
                                    value = variables[arg1.value]
                                    arg1 = Token(get_var_type(value),value=value)
                                if(arg2.type == "VAR"):
                                    value = variables[arg2.value]
                                    arg2 = Token(get_var_type(value),value=value)
                                if(operator.type == "ADD"):
                                    if(arg1.type == "NUMBER"):
                                        if(arg2.type == "NUMBER"):
                                            variables[varname] = float(arg1.value) + float(arg2.value)
                                        elif(arg2.type == "STRING"):
                                            variables[varname] = arg1.value + arg2.value
                                        else:
                                            raise SyntaxError(pos)
                                    elif(arg1.type == "STRING"):
                                        if(arg2.type == "STRING"):
                                            variables[varname] = arg1.value + arg2.value
                                        elif(arg2.type == "NUMBER"):
                                            variables[varname] = arg1.value + arg2.value
                                        else:
                                            raise SyntaxError(pos)
                                    else:
                                        raise SyntaxError(pos)
                            else:
                                raise SyntaxError(pos) #no literal
                        else:
                            raise SyntaxError(pos) #no space
                    else:
                        raise SyntaxError(pos) # no equals
                else:
                    raise SyntaxError(pos) #no var name
            else:
                raise SyntaxError(pos) #no space
        else:
            raise SyntaxError(pos) #no 'var'
    elif(cur_type == "FUN_CALL"):
        pos += 1
        if(tkns[pos].type == "VAR"):
            fun_name = tkns[pos].value
            tokens = parse(variables[fun_name].code)
            variables = run_tokens(tokens,variables)
            pos += 1
        else:
            raise SyntaxError(pos)
    elif(cur_type == "SPACE"):
        pos += 1
    elif(cur_type == "SEMICOLON"):
        pos += 1
    elif(cur_type == "PY_CALL"):
        exec(tkns[pos].value)
        pos += 1
    else:
        raise SyntaxError(pos)(tkns[pos])
    return [variables, pos]

def run_tokens(tokens,variables,debug=0):
    if(debug):
        output = ""
        for x in tokens:
            output += str(x) + ", "
        print(output)
    pos = 0
    while(pos <= len(tokens)-1):
        try:
            response = run_token(tokens, variables, pos)
        except SyntaxError:
            print("Syntax error - those two things probably don't go next to each other.")
            raise
            sys.exit(0)
        except IndexError:
            print("Unexpected EOL.")
            sys.exit(0)
        except KeyError:
            print("Nonexistent variable.")
            sys.exit()
        variables = {**variables, **response[0]}
        pos = response[1]
    return variables


def run(code,debug=0):
    tokens = parse(code,debug=debug)
    variables = {}
    variables = run_tokens(tokens,variables,debug=debug)
    return variables
