#!/usr/bin/env python3

import sys, os
import termios, tty

class Neo:
    variables = []
    functions = []
    arrays = []
    FROM_PARSE = False
    LINES_OF_SCRIPT = []
    INDEX_OF_I = 0
    TO_PARSE = ''
    true_readable = False
    else_readable = False
    entry_true_readable = False
    entry_else_readable = False
    def main(args):
        if Neo.FindUsage(args[0]):
            os.system('cls' if os.name == 'nt' else 'clear')
            Neo.IndexCommands(args[0])
        else:
            Neo.ErrorHandling.LexerError()
    def FindUsage(file_path):
        lines = open(file_path, "r").readlines()
        for l in lines:
            if 'using .sysNeo:' in l:
                print('Starting. . .')
                return True
        print('Usage not found.')
        return False
    def IndexCommands(file_path):
        Neo.LINES_OF_SCRIPT = open(file_path, 'r').readlines()
        Neo.INDEX_OF_I = 0
        while Neo.INDEX_OF_I < len(Neo.LINES_OF_SCRIPT):
            Neo.TO_PARSE = Neo.LINES_OF_SCRIPT(Neo.INDEX_OF_I)
            Neo.ParserHandling.IndentifyListing(Neo.TO_PARSE)
            Neo.INDEX_OF_I += 1
    def ParseInRelationTo(toParse, restParse, forParse, whichParse):
        if forParse == 'var':
            for entry in whichParse:
                if entry.startswith(f"{toParse}:"):
                    return entry.split(":", 1)[1]
            return None
        if forParse == 'bool':
            for entry in whichParse:
                if entry.startswith(f"{toParse}:"):
                    value = entry.split(":", 1)[1].strip()
                    if value == "true":
                        Neo.FROM_PARSE = True
                        Neo.true_readable = True
                        Neo.else_readable = False
                        return 'true'
                    else:
                        Neo.FROM_PARSE = False
                        Neo.true_readable = False
                        Neo.else_readable = True
                        return 'false'
            Neo.FROM_PARSE = False
            Neo.true_readable = False
            Neo.else_readable = True
            return 'false'

    def ParseForContinuationOfFindFunction(nameOfFunction, paramsOfFunction, forCallOrForDefinition):
        i = Neo.INDEX_OF_I + 1
        body = []
        while i < len(Neo.LINES_OF_SCRIPT):
            line = Neo.LINES_OF_SCRIPT[i]
            if 'def;' in line:
                break
            body.append(line)
            i += 1
        Neo.functions.append({"name": nameOfFunction, "params": paramsOfFunction, "body": body})
        Neo.INDEX_OF_I = i
    def ParseForContinuationWithArrayIn(nameOfArray, forCallOrForDefinition):
        i = Neo.INDEX_OF_I + 1
        body = []
        while i < len(Neo.LINES_OF_SCRIPT):
            line = Neo.LINES_OF_SCRIPT[i]
            if ']' in line:
                break
            body.append(line)
            i += 1
        Neo.arrays.append({"name": nameOfArray, "body": body})
        Neo.INDEX_OF_I = i
    def CheckForContinuationOfFind(entry):
        if '^' in entry and not Neo.entry_true_readable:
            ...
        elif '^' in entry and Neo.entry_true_readable:
            newEntry = entry.replace('^', '')
            return newEntry
        if '/' in entry and not Neo.entry_else_readable:
            ...
        elif '/' in entry and Neo.entry_else_readable:
            newEntry = entry.replace('/', '')
            return newEntry
        if '>' in entry and Neo.true_readable:
            newEntry = entry
            return newEntry
        elif '>' in entry and not Neo.true_readable:
            ...
        if '<' in entry and Neo.else_readable:
            newEntry = entry
            return newEntry
        elif '<' in entry and not Neo.else_readable:
            ...

    class ParserHandling:
        def IndentifyListing(currentLine):
            cleaned_line = currentLine.rstrip('\n')
            parts = [part.strip() for part in cleaned_line.split(',') if part.strip()]
            for entry in parts:
                if '~' in entry:
                    return
                new_entry = Neo.CheckForContinuationOfFind(entry)
                if(entry == 'push' or new_entry == 'push'):
                    msg = (parts[entry.index(entry) + 1]).replace("'", '')
                    if msg.startswith('*'):
                        type = msg.replace(':', '')
                        var_to_call = type.replace('*', '')
                        msg = Neo.ParseInRelationTo(var_to_call, msg, 'var', Neo.variables)
                        print(msg)
                    else:
                        msg = msg.replace(":", '')
                        print(msg)
                if entry == 'var' or new_entry == 'var':
                    var_name = parts[entry.index(entry) + 1].replace(',', '')
                    var_value = (parts[entry.index(entry) + 2].replace("'", '')).replace(':', '')
                    Neo.variables.append(f'{var_name}:{var_value}')
                if '>' in entry and not Neo.true_readable:                    
                    parsing = parts[entry.index(entry) + 1].replace('...', '')
                    if parsing.startswith('*'):
                        type = parsing.replace(':', '')
                        var_to_call = type.replace('*', '')
                        parsing = Neo.ParseInRelationTo(var_to_call, parsing, 'bool', Neo.variables)
                        if parsing == 'true':
                            Neo.FROM_PARSE = True
                            Neo.true_readable = True
                            Neo.else_readable = False
                            Neo.entry_true_readable = True
                            Neo.entry_else_readable = False
                        elif parsing == 'false':
                            Neo.FROM_PARSE = False
                            Neo.true_readable = False
                            Neo.else_readable = True
                            Neo.entry_true_readable = False
                            Neo.entry_else_readable = True
                if(entry == '> if' and not Neo.true_readable and Neo.FROM_PARSE):
                    Neo.true_readable = True
                    Neo.else_readable = False
                    Neo.entry_true_readable = True
                    Neo.entry_else_readable = False
                if(entry == '< else...' and Neo.else_readable and not Neo.FROM_PARSE):
                    Neo.true_readable = False
                    Neo.else_readable = True
                    Neo.entry_true_readable = False
                    Neo.entry_else_readable = True
                if(entry.replace(':', '') == 'clear') or new_entry == 'clear:':
                    os.system('cls' if os.name == 'nt' else 'clear')
                if(entry == 'input' or entry.replace(':', '') == 'input') or new_entry == 'input:':
                    if len(parts) > 1:
                        msg = (parts[entry.index(entry) + 1]).replace("'", '')
                    else:
                        msg = ''
                    if msg.startswith('*'):
                        type = msg.replace(':', '')
                        var_to_call = type.replace('*', '')
                        msg = Neo.ParseInRelationTo(var_to_call, msg, 'var', Neo.variables)
                    if msg == '':
                        inp = Neo.vim.neo_input()
                    else:
                        inp = Neo.vim.neo_input(prompt=msg)
                if(entry == 'inp' or new_entry == 'inp'):
                    var_name = parts[entry.index(entry) + 1].replace(',', '')
                    Neo.variables.append(f'{var_name}:{Neo.vim.neo_input()}')
                if(entry == 'arr'):
                    # currentLine is like: "arr, lists, ["
                    cleaned = currentLine.replace("]", "")
                    parts = [p.strip() for p in cleaned.split(',') if p.strip()]
                    # expected: ["arr","lists","["] (or something like that)
                    if len(parts) >= 2:
                        arr_name = parts[1]
                        Neo.ParseForContinuationWithArrayIn(arr_name, "def")
                    return
                if(entry == 'func'):
                    ...


    class vim:
        def neo_input(prompt=""):
            sys.stdout.write(prompt)
            sys.stdout.flush()
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            prompt_len = len(prompt)
            buf = []
            shown = 0
            try:
                tty.setraw(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if ch in ("\n", "\r"):
                        break
                    if ch in ("\x7f", "\b"):
                        if buf:
                            buf.pop()
                            shown -= 1
                            sys.stdout.write("\b \b")
                            sys.stdout.flush()
                        continue
                    if ch == "\x03":
                        raise KeyboardInterrupt
                    buf.append(ch)
                    shown += 1
                    sys.stdout.write(ch)
                    sys.stdout.flush()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            total = prompt_len + shown
            if total > 0:
                sys.stdout.write("\b" * total)
                sys.stdout.write(" " * total)
                sys.stdout.write("\b" * total)
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()
            return "".join(buf)
        def nvim(emulator, arr):
            ...



    class ErrorHandling:
        def LexerError():
            print('Lexer error occurred.')



Neo.main(sys.argv[1:])