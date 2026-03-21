import ast
from random import randint

def __gettype__(obj):
    if isinstance(obj, str) and obj.isdigit() and '"' not in obj:
        return int(obj), 'int'
    elif isinstance(obj, str) and '"' in obj:
        return obj.strip('"'), 'str'
    else:
        return obj, 'key'


def __assign_node__(data):
    if __gettype__(data)[1] == 'key':
        return MiniQ.VariableNode(data)
    elif __gettype__(data)[1] in ['int', 'str']:
        return MiniQ.LiteralNode(data)
    return None


class MiniQ:

    SYNTAX = {
        'string': '"',
        'operators': ['==', '!=', '>', '<', '>=', '<=', 'in'],
        'and': 'and',
        'or': 'or',
        'index': '  ',
    }

    ENVIRONMENT = {}
    WATCHERS = []
    class Import:
        def __init__(self, file):
            self.file = file + ".mq"

        def action(self):
            with open(self.file) as unread:
                contents = unread.read()

            imported = MiniQ(contents)

            for part in MiniQ.ENVIRONMENT:
                MiniQ.ENVIRONMENT[part] = MiniQ.ENVIRONMENT[part]
    class AppendNode:
        def __init__(self, path, data):
            self.path = path
            self.data = data
        def action(self):
            self.data.action()
            self.path.action()
            with open(self.path.value, 'r') as read_f:
                contents = read_f.read()
            with open(self.path.value, 'w') as raw:
                
                raw.write(contents + '\n' + str(self.data.value))


    class WriteNode:
        def __init__(self, path, data):
            self.path = path
            self.data = data
        def action(self):
            self.data.action()
            self.path.action()
            with open(self.path.value, 'w') as raw:
                
                raw.write(str(self.data.value))
            

    class ReadNode:
        def __init__(self, path, name):
            self.path = path
            self.name = name
        def action(self):
            self.path.action()
            MiniQ.ENVIRONMENT[self.name] = open(self.path.value).read()
        
    class InputNode:
        def __init__(self):
            self.value = None
        def action(self):
            self.value = input('> ')
    class Loop:
        def __init__(self, condition, block):
            
            self.query = condition
            self.code = block
        def check(self):
            expr = ''
            #self.query = self.query.split(' ')
           
            if type(self.query) != list:
                self.query = self.query.split(' ')
            for part in self.query:
                append = part
            
                if part not in MiniQ.SYNTAX['operators'] and part != MiniQ.SYNTAX['and'] and part != MiniQ.SYNTAX['or']:
                   
                    if __gettype__(append)[1] == 'key':
                        
                        node = MiniQ.VariableNode(part)
                        node.action()
                        value = str(node.value)
                        if value.isdigit():
                            expr += value + ' '
                        else:
                            expr += '"' + value + '"' + ' '
                    else:
                        expr += part + ' '
                else:
                    expr += part + ' '

            
            if eval(expr):
                
                return self.code.code

            return None
        
    class ReStrNode:
        def __init__(self, expr):
            self.expr = expr
        def action(self):
            self.expr = __assign_node__(self.expr)
            self.expr.action()
            self.value = '"' + self.expr.value + '"'
    class MathNode:
        def __init__(self, expr):
            self.expr = expr
            self.value = None

        def action(self):
            expr = self.expr
            new = ''
            expr = expr.split(' ')
            
            for part in expr:
                part = str(part)
                if part in MiniQ.ENVIRONMENT:
                    new += str(MiniQ.ENVIRONMENT[part]) + ' '
                else:
                    new += part + ' '
                
            
            expr = new
            tree = ast.parse(expr, mode="eval")
            self.value = eval(compile(tree, "", "eval"))
            

    class QueryNode:
        def __init__(self, query:str, code):
            self.query = query
            self.code = code

        def action(self):
           
            expr = ''
            if type(self.query) != list:
                self.query = self.query.split(' ')
            for part in self.query:
                append = part
            
                if part not in MiniQ.SYNTAX['operators'] and part != MiniQ.SYNTAX['and'] and part != MiniQ.SYNTAX['or']:
                   
                    if __gettype__(append)[1] == 'key':
                        node = MiniQ.VariableNode(part)
                        node.action()
                        value = str(node.value)
                        
                        if value.isdigit() or value[1:].isdigit() and value[0] == '-':
                            expr += value + ' '
                        else:
                            expr += '"' + value + '"' + ' '
                    else:
                        expr += part + ' '
                else:
                    expr += part + ' '

            
            if eval(expr):
                return self.code.code

            return None

    class BlockOfCode:
        def __init__(self, code):
            self.code = code

    class PrintNode:

        def __init__(self, node):
            self.node = node

        def action(self):

            self.node.action()
            print(self.node.value)

    class LiteralNode:

        def __init__(self, value):

            t = __gettype__(value)

            if t[1] == 'str':
                self.value = t[0]
            elif t[1] == 'int':
                self.value = t[0]

        def action(self):
            pass
    class FunctionCreationNode:
        def __init__(self, name:str, code:object):
            self.name = name
            self.code = code
        def action(self):
            MiniQ.ENVIRONMENT[self.name] = self.code
    class FunctionNode:
        def __init__(self, name:str, args:dict):
            self.name = name
            self.value = None
            self.args = args
        def action(self):
            for arg in self.args:
                value = __assign_node__(self.args[arg])
                value.action()
                MiniQ.ENVIRONMENT[arg] = value.value
    class VariableNode:

        def __init__(self, name):
            self.name = name
            self.value = None

        def action(self):

            if self.name in MiniQ.ENVIRONMENT:
                self.value = MiniQ.ENVIRONMENT[self.name]

    class AssignNode:

        def __init__(self, name, value):
            self.name = name
            self.value = value

        def action(self):
            
            self.value.action()

            MiniQ.ENVIRONMENT[self.name] = self.value.value

    def run(self, code):
        
        for part in code:
            
            if isinstance(part, MiniQ.PrintNode):
                part.action()

            elif isinstance(part, MiniQ.AssignNode):
                part.action()
                index = 0
                for watcher in MiniQ.WATCHERS:
                    
                    returned = watcher.action()
                    
                    if returned is not None:
                        del self.WATCHERS[index]
                        self.run(returned)
                    index += 1
            elif isinstance(part, MiniQ.QueryNode):

                returned_code = part.action()

                if returned_code is not None:
                    self.run(returned_code)

            elif isinstance(part, MiniQ.FunctionCreationNode):
                part.action()

            elif isinstance(part, MiniQ.FunctionNode):
                part.action()
                self.run(MiniQ.ENVIRONMENT[part.name].code)
            elif isinstance(part, MiniQ.Loop):
                while part.check() != None:
                    self.run(part.check())
            elif isinstance(part, self.WriteNode):
                part.action()
            elif isinstance(part, self.ReadNode):
                part.action()
            elif isinstance(part, MiniQ.AppendNode):
                part.action()
            elif isinstance(part, MiniQ.Import):
                part.action()

    def tokenize(self, text):

        lines = text.splitlines()
        index = 0

        def parse_block(indent=0):
            nonlocal index
            code = []

            while index < len(lines):

                raw_line = lines[index]

                if raw_line.strip() == "":
                    index += 1
                    continue

                current_indent = len(raw_line) - len(raw_line.lstrip())

                if current_indent < indent:
                    break

                line = raw_line.strip()

                # PRINT
                if line.startswith("import "):
                    code.append(MiniQ.Import(line.split(' ')[1]))
                    index += 1
                    continue
                if line.startswith("print "):

                    content = line[6:].strip()

                    if content.startswith("math(") and content.endswith(")"):
                        expr = content[5:-1].strip()
                        node = MiniQ.MathNode(expr)
                    elif "input" in content:
                        node = MiniQ.InputNode()
                    else:
                        node = __assign_node__(content)

                    code.append(
                        MiniQ.PrintNode(node)
                    )
                    
                    index += 1
                    continue

                # VARIABLE
                if line.startswith("var "):

                    name, value = line[4:].split("=", 1)
                    name = name.strip()
                    value = value.strip()
                    
                
                    if value.startswith("math(") and value.endswith(")"):
                        expr = value[5:-1].strip()
                        
                        node = MiniQ.MathNode(expr)

                    elif value.startswith("restr(") and value.endswith(")"):
                        expr = value[6:-1].strip()
                        node = MiniQ.ReStrNode(expr)
                    elif "input" in value:
                        node = MiniQ.InputNode()
                    else:
                        node = __assign_node__(value)
                    
                    code.append(
                        MiniQ.AssignNode(name, node)
                    )

                    index += 1
                    continue
                if line.startswith("read "):

                    new = line[5:].split("to", 1)
                    name = new[1].strip()
                    value = new[0].strip()
                    
                    if value.startswith("math(") and value.endswith(")"):
                        expr = value[5:-1].strip()
                        node = MiniQ.MathNode(expr)
                    elif "input" in value:
                        node = MiniQ.InputNode()
                    else:
                        node = __assign_node__(value)

                    code.append(
                        MiniQ.ReadNode(node, name)
                    )

                    index += 1
                    continue
                if line.startswith("rewrite "):
                    
                    new = line[8:].split("to")
                    
                    name = new[1].strip()
                    value = new[0].strip()
                    
                    if value.startswith("math(") and value.endswith(")"):
                        expr = value[5:-1].strip()
                        node = MiniQ.MathNode(expr)
                    elif "input" in value:
                        node = MiniQ.InputNode()
                    else:
                        node = __assign_node__(value)

                    if name.startswith("math(") and name.endswith(")"):
                        expr = value[5:-1].strip()
                        node_n = MiniQ.MathNode(expr)
                    elif "input" in name:
                        node_n = MiniQ.InputNode()
                    else:
                        node_n = __assign_node__(name)

                    code.append(
                        MiniQ.WriteNode(node, node_n)
                    )
                    
                    index += 1
                    continue
                if line.startswith("append "):
                    
                    new = line[7:].split("to", 1)
                    name = new[0].strip()
                    value = new[1].strip()
                    
                    if value.startswith("math(") and value.endswith(")"):
                        expr = value[5:-1].strip()
                        node = MiniQ.MathNode(expr)
                    elif "input" in value:
                        node = MiniQ.InputNode()
                    else:
                        node = __assign_node__(value)

                    if name.startswith("math(") and name.endswith(")"):
                        expr = value[5:-1].strip()
                        node_n = MiniQ.MathNode(expr)
                    elif "input" in name:
                        node_n = MiniQ.InputNode()
                    else:
                        node_n = __assign_node__(name)

                    code.append(
                        MiniQ.AppendNode(node, node_n)
                    )
                 
                    index += 1
                    continue

                # QUERY
                if line.startswith("query "):

                    query = line[6:].strip()
                 
                    index += 1
                    block = parse_block(current_indent + 2)

                    code.append(
                        MiniQ.QueryNode(
                            query,
                            MiniQ.BlockOfCode(block)
                        )
                    )

                    continue
                if line.startswith("watch "):

                    query = line[6:].strip()
                 
                    index += 1
                    block = parse_block(current_indent + 2)

                    MiniQ.WATCHERS.append(
                        MiniQ.QueryNode(
                            query,
                            MiniQ.BlockOfCode(block)
                        )
                    )

                    continue
                if line.startswith("loop "):

                    query = line[5:].strip()
                    
                    index += 1
                    block = parse_block(current_indent + 2)

                    code.append(
                        MiniQ.Loop(
                            query,
                            MiniQ.BlockOfCode(block)
                        )
                    )

                    continue
                if line.startswith("func "):
                    
                    name = line.split(' ')[1]
                    index += 1

                    block = parse_block(current_indent + 2)
                    code.append(
                        MiniQ.FunctionCreationNode(
                            name,
                            MiniQ.BlockOfCode(block)
                    
                        )
                    )
                    
                    continue
                if line.startswith('run '):
                    arguments = {}
                    args = line.split(' ')[2:]
                    for arg in args:
                        arguments[arg.split('=')[0]] = arg.split('=')[1]

                    code.append(
                        MiniQ.FunctionNode(
                            name=line.split(' ')[1],
                            args=arguments
                        )
                    )
                    index += 1
                    continue
                index += 1

            return code

        return parse_block(0)

    def __init__(self, code):

        parsed = self.tokenize(code)
        self.run(parsed)


