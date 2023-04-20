import ast

# Get the code
code = ""

# Get the built-ins functions
code += open("default_values.py").read() + "\n" * 5
code += open("functions.py").read() + "\n" * 5
code += open("prog.py").read() + "\n" * 5


# Remove import
code = code.replace("from classes import *","")


# Define a transformer class to replace all built-ins classes by ExtendedClass
class IntStrTransformer(ast.NodeTransformer):
    # When it visits a number
    def visit_Num(self, node):
        return ast.Call(func=ast.Name(id="ExtendedInt", ctx=ast.Load()),
                         args=[node],
                         keywords=[],
                        )

    # When it visits a string
    def visit_Str(self, node):
        return ast.Call(func=ast.Name(id="ExtendedString", ctx=ast.Load()),
                         args=[node],
                         keywords=[],
                        )

    # When it visits a formated value
    def visit_FormattedValue(self, node):
        return ast.Call(func=ast.Name(id="ExtendedString", ctx=ast.Load()),
                         args=[node],
                         keywords=[],
                        )

    # When it visits a joinedstr
    def visit_JoinedStr(self, node):
        elts = []
        for value in node.values:
            if isinstance(value, ast.Str):
                elts.append(self.visit_Str(value))
            elif isinstance(value, ast.FormattedValue):
                elts.append(self.visit_FormattedValue(value))
            elif isinstance(value, ast.Call):
                elts.append(self.visit_Call(value))
            else:
                raise ValueError(f"Unexpected node inside JoinedStr, {value!r}")
        return ast.Call(func=ast.Name(id="ExtendedString", ctx=ast.Load()),
                         args=[ast.List(elts=elts, ctx=ast.Load())],
                         keywords=[],
                        )

    def visit_Call(self, node):
        args = [self.visit(arg) for arg in node.args]
        keywords = [self.visit(keyword) for keyword in node.keywords]
        return ast.Call(func=self.visit(node.func),
                        args=args,
                        keywords=keywords,
                        )
    
    # When it visits a list
    def visit_List(self, node):
            return ast.Call(func=ast.Name(id="ExtendedList", ctx=ast.Load()),
                            args=[node],
                            keywords=[],
                            )
    # When it visits a range => list
    def visit_Range(self, node):
        args = [node.start, node.end]
        if node.step is not None:
            args.append(node.step)
        return ast.Call(func=ast.Name(id="ExtendedList", ctx=ast.Load()),
                        args=[node],
                        keywords=[],
                        )

# Parse the code into an AST
# tree = ast.literal_eval(code)
tree = ast.parse(code)

# Use the transformer to modify the AST
transformer = IntStrTransformer()
new_tree = transformer.visit(tree)




# Write the new code to the prog.py
with open("tmp/prog.py", "wt") as file:

    intial_code = open("prog.py").read()

    default_code = f'''# !/https://github.com/aderepas

"""
=========================================
/!\ THIS CODE IS NOT WRITTEN BY A BOT /!\\
=========================================

 Some of you might think that everything
 here has been generated by an AI, or a
bot but actually, if the code works, it's
  because of a Human. Below is the code 
written by the Human and the GitHub repo
       that explains what is this.
"""

""" Initial code: {len(intial_code)} bytes
{intial_code}
"""
'''

    unparsed_code = ast.unparse(new_tree)

    file.write(default_code)
    file.write(open("classes.py").read().replace("from functions import *",""))
    file.write(unparsed_code)
