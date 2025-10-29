





def log(func):
    print("Original writes once: Calling:", func.__name__)
    def wrapper(*args, **kwargs):
        print("Writing this because this print is in decorator: Calling:", func.__name__)
        return func(*args, **kwargs)  # if u comment this part then it will not print hello
    return wrapper   # since f = decorator(f) so greet = log(greet), where greet = wrapper which execute print and then calls greet function object

@log
def greet():            # calls log(greet)   # it auto appends (greet) to whatever is written after @ and executes
    print("Hello")

greet()   # Prints "Calling: greet" then "Hello" # greet = log(greet) = wrapper
greet()   # does not call the print in parent function cause decorators are run only when the function gets defined

# @decorator
# def f(): pass
#
# f = decorator(f)
