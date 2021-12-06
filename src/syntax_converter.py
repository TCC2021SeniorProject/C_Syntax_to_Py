"""
    XXX This is a module file that only does one job
          input:  ++b&&(!a)
          output: b += 1 and not a

    @TODO: 

    @AUTHOR: Marco-Backman
    @TARGET USER: Users who requires their single line of C assingment script and 
                  conditional statement script to be converted to Python code
"""

#Left - C syntax, Right - Python syntax
conditional_single_operator = { "&" : 1,
                                "|" : 1,
                                ">" : 3,
                                "<" : 3,
                                "=" : 3,
                                ">" : 3,
                                "<" : 3,
                                "!" : 4,
                                ":" : 5,
                                "+" : 5,
                                "-" : 5,
                                "*" : 6,}

conditional_operator = {"&&" : "and",
                        "||" : "or",
                        ">=" : ">=",
                        "<=" : "<=",
                        "==" : "==",
                        ">" : ">",
                        "<" : "<",
                        "!=" : "!=",
                        "=" : "=",
                        "<=" : "=",
                        ":=" : "=",
                        "//=" : "//=",
                        "//=" : "//=",
                        "+=" : "+=",
                        "-=" : "-=",
                        "/=" : "/=",
                        "*=" : "*=",
                        "%=" : "%=",
                        "&=" : "&=",
                        "|=" : "|=",
                        "^=" : "^=",}
    
left_expression = {'!' : 'not'}

right_expression = {'++' : "+= 1",
                    '--' : "-= 1"}

class Node:
    def __init__(self):
        self.parent : Node = None
        self.left = None
        self.left_expression = "" # Expresstion like !. ++. --
        self.operator = ""
        self.right = None
        self.right_expression = ""
        self.visited = False

    def get_left(self):
        return self.left

    def set_left(self, left):
        self.left = left
        self.check_left_expression()

    def get_operator(self):
        return self.operator

    def set_operator(self, operator):
        self.operator = operator

    def get_right(self):
        return self.right

    def set_right(self, right):
        self.right = right
        self.check_right_expression()

    def is_visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True

    def check_left_expression(self):
        if type(self.left) is str:
            self.left = self.left.strip()
            if (len(self.left) > 1): #check !
                if self.left[0:1] in left_expression:
                    self.left_expression = left_expression[self.left[0:1]]
                    self.left = (self.left[1:]).strip()
                    self.left = self.left_expression + " " + self.left
            if (len(self.left) > 2): #check --, ++
                if self.left[0:2] in right_expression:    #expression on the left
                    self.left_expression = right_expression[self.left[0:2]]
                    self.left = (self.left[2:]).strip()
                    self.left = self.left + " " + self.left_expression
                elif self.left[-2:] in right_expression:  #expression on the right
                    self.left_expression = right_expression[self.left[-2:]]
                    self.left = (self.left[:-2]).strip()
                    self.left = self.left + " " + self.left_expression

    def check_right_expression(self):
        if type(self.right) is str:
            self.right = self.right.strip()
            if (len(self.right) > 1): #check !
                if self.right[0:1] in left_expression:
                    self.right_expression = left_expression[self.right[0:1]]
                    self.right = (self.right[1:]).strip()
                    self.right = self.right_expression + " " + self.right
            if (len(self.right) > 2): #check --, ++
                if self.right[0:2] in right_expression:
                    self.right_expression = right_expression[self.right[0:2]]
                    self.right = (self.right[2:]).strip()
                    self.right = self.right + " " + self.right_expression
                elif self.right[-2:] in right_expression:
                    self.right_expression = right_expression[self.right[-2:]]
                    self.right = (self.right[:-2]).strip()
                    self.right = self.right + " " + self.right_expression

class SyntaxTree:
    def __init__(self, root):
        self.root : Node = root
        self.deepest_node : Node = None
        self.py_script : str = ""
        self.stack = []

    def to_python_keywords(self, line : str):
        line = line.replace("(", "")
        line = line.replace("true", "True")
        line = line.replace("false", "False")
        return line

    #Set string on left, operator on the middle, and empty node on the right
    def connect_node(self, walk : Node, operator : str, variable : str):
        walk.set_operator(conditional_operator[operator])
        new_node = Node()
        new_node.parent = walk
        walk.set_left(variable)
        walk.set_right(new_node)

    def translate(self, line : str, walk : Node):
        remainder = ""
        for index, char in enumerate(line):
            #Hits the last index
            if index == (len(line) - 1):
                if char == ')':
                    walk.parent.set_right(remainder)
                else:
                    walk.parent.set_right(remainder + char)
                return

            elif char == ')': #one step to the parent and set left when there is no more ')'
                if walk == self.root:
                    self.translate(remainder + line[(index + 1):].strip(), walk)
                    return
                elif remainder == "":
                    continue
                elif walk.parent == self.root:
                    new_parent_node = Node()
                    new_parent_node.set_left(walk.parent)
                    walk.parent.set_right(remainder)
                    self.root = new_parent_node
                    new_parent_node.set_right(Node())
                    self.translate(line[(index + 1):].strip(), new_parent_node)
                    return
                else:
                    new_parent_node = Node()
                    new_parent_node.parent = walk.parent.parent
                    new_parent_node.set_left(walk.parent)
                    walk.parent.parent.set_right(new_parent_node)
                    walk.parent.set_right(remainder)
                    walk.parent.parent = new_parent_node
                    new_parent_node.set_right(Node())
                    self.translate(line[(index + 1):].strip(), new_parent_node)
                    return

            #On one operator character match
            elif char in conditional_single_operator:
                singular_operator = line[index]
                two_operator = line[index] + line[index + 1]

                #Check two charactor operators first
                if two_operator in conditional_operator:
                    #Reassign operator
                    if walk.left != None and walk.right != None:
                        walk.set_operator(conditional_operator[two_operator])
                        self.translate(line[(index + 2):].strip(), walk.get_right())
                        return
                    #Assign operator
                    elif walk != None:
                        self.connect_node(walk, two_operator, remainder)
                        self.translate(line[(index + 2):].strip(), walk.get_right())
                        return
                    else:
                        print("Connection failed, empty node")  
                #Check single charactor operators                 
                elif singular_operator in conditional_operator: 
                    if walk != None:
                        self.connect_node(walk, singular_operator, remainder)
                        self.translate(line[(index + 1):].strip(), walk.get_right())
                        return
                    else:
                        print("Connection failed, empty node")
            remainder += char

    def getScript(self) -> str:
        return self.py_script

    def print_info(self, walk : Node, script : str):
        if type(walk) is Node:
            if type(walk.left) is str:
                script += walk.left
            else:
                script = self.print_info(walk.left, script + "(")
            script += " " + walk.operator + " "
            if type(walk.right) is str:
                script += walk.right
            else:
                script =  self.print_info(walk.right, script + "(")
        if walk == self.root:
            return script
        return script + ")"



string1 = "a>= 2&&!b !=true" #-> Pass: a >= (2 and (not b != True))

syntax = SyntaxTree(Node())
string1 = syntax.to_python_keywords(string1)
syntax.translate(string1, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")

string2 = "a>=2&&!(b!=false)" #-> Pass: a >= (2 and (not b != False))

syntax = SyntaxTree(Node())
string2 = syntax.to_python_keywords(string2)
syntax.translate(string2, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")

string3 = "(a>=2)&&!(b!=false)" #-> Pass : (a >= 2) and (not b != False)

syntax = SyntaxTree(Node())
string3 = syntax.to_python_keywords(string3)
syntax.translate(string3, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")


string4 = "((a>=2))&&!(b!=4)" #-> Pass - (a >= 2) and (not b != 4)

syntax = SyntaxTree(Node())
string4 = syntax.to_python_keywords(string4)
syntax.translate(string4, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")

string5 = "(e&&(a>=2))&&!(b!=4)" #-> Pass - e and ((a >= 2) and (not b != 4))

syntax = SyntaxTree(Node())
string5 = syntax.to_python_keywords(string5)
syntax.translate(string5, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")

string6 = "(!a)&&b--"

syntax = SyntaxTree(Node()) #-> Pass - not a and b -= 1
string6 = syntax.to_python_keywords(string6)
syntax.translate(string6, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")

string7 = "++b&&(!a)" #-> Pass - b += 1 and not a

syntax = SyntaxTree(Node())
string7 = syntax.to_python_keywords(string7)
syntax.translate(string7, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")

string8 = "a := b++" #-> Pass - a = b += 1

syntax = SyntaxTree(Node())
string8 = syntax.to_python_keywords(string8)
syntax.translate(string8, syntax.root)
print(syntax.print_info(syntax.root, ""))
print("-----------------------------")
