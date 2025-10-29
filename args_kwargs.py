def demo(*args,**kwargs):
    print(sum(args))
    print(args)
    print(kwargs)


demo(1,2,3,a = 4 ,b = 5)

nums = [1,2,3,4,5]

def dict_demo(**kwargs):
    print(kwargs)

dict = {"a":1,"b":2}

dict_demo(**dict) # just dict would be an error

print(*nums) # to seperate the arguments

def student(name, **info):
    print("Name:", name)
    print("Info:", info)

student("Michael",age=20,major = "CS" ,gpa="3.6")

def example(a,b,*args, c=10, **kwargs): # simple args, args(must come before keyword args), keyword arguments, and kwargs
    print(a,b,args, c , kwargs)

example(1,2,3,4, c= 20, pop=10,bob=30)