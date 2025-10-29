
import sys
import click
#how python looks for vars inside the function
# L	Local	Variables inside the current function
# E	Enclosing	Variables in outer (non-global) functions
# G	Global	Variables defined at the module level
# B	Built-in	Python’s built-in names (len, sum, etc.)

x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()

outer()  # prints "local"

def outer1():
    x = 10
    def inner():
        print(x)
    return inner

f = outer1()
print(f.__closure__[0].cell_contents)

def multiply(x):
    def multBy(y):
        return x * y
    return multBy

x2 = multiply(2)
print(x2(6))

if "Toghrul" in sys.argv: # added command line options in Python just from C's argv interpreter builds sys.argv
                          # have to import sys because not in my namespace
    print("Hello World")
# print(sys.modules)
click.echo(click.style('Hello, world!', fg='red'))
