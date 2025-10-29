def counter():
    count = 0
    def increment():
        nonlocal count # it can read outer functions variables but not modify them
        count += 1
        return count
    return increment


c = counter() # save state function which is in the memory of the interpreter
print(c())
print(c())

def outer():
    a = 10
    def inner():
        print(a)
    return inner


f = outer() # save state function that has saved in the memory access to a
f()