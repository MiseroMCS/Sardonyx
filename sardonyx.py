#!/usr/bin/env python
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
    elif(cur_char == "i"):
        pos += 1
        if(code[pos] == "f"):
            pos += 1
            token.type = "IF"
            token.value = "if"
        else:
            raise SyntaxError(pos)
    elif(cur_char == "w"):
        pos += 1
        if(code[pos] == "h"):
            pos += 1
            if(code[pos] == "i"):
                pos += 1
                if(code[pos] == "l"):
                    pos += 1
                    if(code[pos] == "e"):
                        token.type = "WHILE"
                        token.value = "while"
                        pos += 1
                    else:
                        raise SyntaxError(pos)
                else:
                    raise SyntaxError(pos)
            else:
                raise SyntaxError(pos)
        else:
            raise SyntaxError(pos)
    elif(cur_char in ["-","+"]):
        pos += 1
        if(code[pos] in digits):
            token.type = "NUMBER"
            token.value = code[pos]
            if(code[pos-1] == "-"):
                token.value = "-" + code[pos]
            pos += 1
            used_decimal = 0
            while(code[pos] in digits + ["."]):
                if(code[pos] == "."):
                    if(used_decimal):
                        raise SytaxError(pos)
                    else:
                        used_decimal = 1
                token.value += code[pos]
                pos += 1
        elif(code[pos-1] == "+"):
            token.type = "ADD"

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
        if(code[pos] == "="):
            token.type = "EQUALITY"
            token.value = "=="
            pos += 1
    elif(cur_char == " "):
        token.type = "SPACE"
        token.value = " "
        pos += 1
    elif(cur_char == "!"):
        pos += 1
        if(code[pos] == "="):
            token.type = "INEQUALITY"
            token.value = "!="
        else:
            token.type = "FUN_CALL"
            token.value = "!"
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
    elif(cur_char == "<"):
        pos += 1
        if(code[pos] == "="):
            token.type = "LESSTHAN_EQUALTO"
            token.value = "<="
            pos += 1
        else:
            token.type = "LESSTHAN"
            token.value = "<"
    elif(cur_char == ">"):
        pos += 1
        if(code[pos] == "="):
            token.type = "GREATERTHAN_EQUALTO"
            token.value = ">="
            pos += 1
        else:
            token.type = "GREATERTHAN"
            token.value = ">"
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

def run_token(tkns, variables, pos, debug=0):
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
                                if(debug):
                                    print("Executing expression: {} {} {}".format(arg1,operator,arg2))
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
                                elif(operator.type == "EQUALITY"):
                                    if(arg1.type == "NUMBER"):
                                        arg1.value = float(arg1.value)
                                    if(arg2.type == "NUMBER"):
                                        arg2.value = float(arg2.value)
                                    if(arg1.value == arg2.value):
                                        variables[varname] = 1
                                    else:
                                        variables[varname] = 0
                                elif(operator.type == "INQUALITY"):
                                    if(arg1.type == "NUMBER"):
                                        arg1.value = float(arg1.value)
                                    if(arg2.type == "NUMBER"):
                                        arg2.value = float(arg2.value)
                                    if(arg1.value != arg2.value):
                                        variables[varname] = 1
                                    else:
                                        variables[varname] = 0
                                elif(operator.type == "LESSTHAN"):
                                    if(arg1.type != "NUMBER" or arg2.type != "NUMBER"):
                                        raise SyntaxError(pos)
                                    arg1.value = float(arg1.value)
                                    arg2.value = float(arg2.value)
                                    if(arg1.value < arg2.value):
                                        variables[varname] = 1
                                    else:
                                        variables[varname] = 0
                                elif(operator.type == "GREATERTHAN"):
                                    if(arg1.type != "NUMBER" or arg2.type != "NUMBER"):
                                        raise SyntaxError(pos)
                                    arg1.value = float(arg1.value)
                                    arg2.value = float(arg2.value)
                                    if(arg1.value > arg2.value):
                                        variables[varname] = 1
                                    else:
                                        variables[varname] = 0
                                elif(operator.type <= "LESSTHAN_EQUALTO"):
                                    if(arg1.type != "NUMBER" or arg2.type != "NUMBER"):
                                        raise SyntaxError(pos)
                                    arg1.value = float(arg1.value)
                                    arg2.value = float(arg2.value)
                                    if(arg1.value < arg2.value):
                                        variables[varname] = 1
                                    else:
                                        variables[varname] = 0
                                elif(operator.type == "GREATERTHAN_EQUALTO"):
                                    if(arg1.type != "NUMBER" or arg2.type != "NUMBER"):
                                        raise SyntaxError(pos)
                                    arg1.value = float(arg1.value)
                                    arg2.value = float(arg2.value)
                                    if(arg1.value >= arg2.value):
                                        variables[varname] = 1
                                    else:
                                        variables[varname] = 0
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
            variables = run_tokens(tokens,variables,debug=debug)
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
    elif(cur_type == "IF"):
        pos += 1
        if(tkns[pos].type == "SPACE"):
            pos += 1
            if(tkns[pos].type == "VAR"):
                pos += 1
                if(tkns[pos].type == "SPACE"):
                    pos += 1
                    if(tkns[pos].type == "FUN_CALL"):
                        pos += 1
                        if(tkns[pos].type == "VAR"):
                            if(variables[tkns[pos-3].value] == 1):
                                fun_name = tkns[pos].value
                                tokens = parse(variables[fun_name].code)
                                variables = run_tokens(tokens,variables)
                            pos += 1
                        elif(tkns[pos].type == "NUMBER"):
                            if(tkns[pos].value == 1):
                                fun_name = tkns[pos].value
                                tokens = parse(variables[fun_name].code)
                                variables = run_tokens(tokens,variables)
                            pos += 1
                        else:
                            raise SyntaxError(pos)
                    else:
                        raise SyntaxError(pos)
                else:
                    raise SyntaxError(pos)
            else:
                raise SyntaxError(pos)
        else:
            raise SyntaxError(pos)
    elif(cur_type == "WHILE"):
        pos += 1
        if(tkns[pos].type == "SPACE"):
            pos += 1
            if(tkns[pos].type == "VAR"):
                pos += 1
                if(tkns[pos].type == "SPACE"):
                    pos += 1
                    if(tkns[pos].type == "FUN_CALL"):
                        pos += 1
                        if(tkns[pos].type == "VAR"):
                            while(variables[tkns[pos-3].value] == 1):
                                fun_name = tkns[pos].value
                                tokens = parse(variables[fun_name].code)
                                variables = run_tokens(tokens,variables)
                            pos += 1
                        elif(tkns[pos].type == "NUMBER"):
                            if(tkns[pos].value == 1):
                                fun_name = tkns[pos].value
                                tokens = parse(variables[fun_name].code)
                                variables = run_tokens(tokens,variables)
                            pos += 1
                        else:
                            raise SyntaxError(pos)
                    else:
                        raise SyntaxError(pos)
                else:
                    raise SyntaxError(pos)
            else:
                raise SyntaxError(pos)
        else:
            raise SyntaxError(pos)
    else:
        raise SyntaxError(pos)
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
            response = run_token(tokens, variables, pos,debug=debug)
        except SyntaxError as e:
            print("Syntax error - those two things probably don't go next to each other.")
            if(debug):
                output = ""
                for i,x in enumerate(tokens):
                    if(i == e.msg):
                        output += "(HERE)"
                    output += str(x) + ", "
                print(output)
            sys.exit(0)
        except IndexError:
            print("Unexpected EOL.")
            sys.exit(0)
        except KeyError as e:
            print("Nonexistent variable.")
            sys.exit(0)
        variables = {**variables, **response[0]}
        pos = response[1]
    return variables


def run(code,variables={},debug=0):
    tokens = parse(code,debug=debug)
    variables = run_tokens(tokens,variables,debug=debug)
    return variables

def find_imports(contents):
    lines = contents.split("\n")
    if(lines[0].startswith("import ")):
        imports = lines[0].replace("import ","").split(", ")
        lines[0] = lines[0].replace(lines[0],"")
        for filename in imports:
            try:
                lines = find_imports(open(filename).read()).split("\n") + lines
            except FileNotFoundError:
                print("File '{}' not found. Aborting.".format(filename))
                sys.exit(0)
    for x in lines:
        if(x.startswith("//")):
            lines.remove(x)
    return '\n'.join(lines)

if(__name__ == "__main__"):
    if(len(sys.argv) >= 2):
        debug = 0
        if(len(sys.argv) >= 3):
            if(sys.argv[2] == "debug"):
                debug = 1
        filename = sys.argv[1]
        try:
            contents = open(filename).read()
        except:
            print("File does not exist.")
            sys.exit(0)
        contents = find_imports(contents)
        contents = contents.replace("\n","")
        try:
            print(run(contents,debug=debug))
        except KeyboardInterrupt:
            print("Exiting.")
            sys.exit(0)
    else:
        print("Starting shell. Type 'help' for help.")
        variables = {}
        debug = 0
        while(1):
            cmd = input(">> ")
            if(cmd == "variables"):
                print(variables)
            elif(cmd == "help"):
                print("Type in code to run it.\nType 'variables' to view all of the variables currently being used.\nType 'exit' to exit the prompt.")
            elif(cmd.startswith("import ")):
                cmd = cmd.replace("import ","")
                try:
                    contents = open(cmd).read()
                except FileNotFoundError:
                    print("File not found.")
                    continue
                contents = find_imports(contents)
                contents = contents.replace("\n","")
                variables = run(contents,variables=variables,debug=debug)
            elif(cmd == "exit"):
                print("Exiting.")
                sys.exit(0)
            elif(cmd == "debug"):
                print("Toggled debug mode.")
                debug = not(debug)
            else:
                variables = run(cmd,variables=variables,debug=debug)
