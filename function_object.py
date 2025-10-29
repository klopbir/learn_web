a = 1
b = 2

def example(a = 10):
    print("Hello World")

def multiply(x):
    def multBy(y):
        return x * y
    return multBy

print(example.__code__) # local variables are stored in the code segment
print(example.__defaults__)
print(example.__globals__)
x2 = multiply(2) # this makes closure segment to store integer 2 as its closure variable from outer scope
print(x2.__closure__[0].cell_contents)

def greet():pass

greet.bob = "Bob"
greet.description = "Greet the user"
print(greet.description)
print(greet.bob)

# │       Function  Object(heap)               │
# │  __name__   → 'greet'                      │
# │  __code__   → Code  Object(bytecode)       │
# │  __globals__→ Global dict reference        │
# │  __defaults__→ None                        │
# │  __closure__ → None( if no closure)        │