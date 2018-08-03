"""
NOTES: Everything in python is an object!

For the hello example:
----------------------
Even though we deleted the name hello, the name greet
still points to our original function object. It is important
to know that functions are objects that can be passed to other objects!

"""

s = 'A Global Variable'


def check_for_locals():
    """Scope Review, Part-1."""
    local_variable = "HELLO"
    print("{SECTION} Locals = {LOCALS}".format(
        LOCALS=locals(),
        SECTION='\n# SCOPE EXAMPLE #\n'))
    print("Globsls = {0}".format(globals().keys()))
    print(globals()['s'] + "\n")


def hello(name='Danny'):
    return 'Hello ' + name


def testing(name='Danny'):
    print("{SECTION}{PRINT}".format(
        PRINT='The hello() function has been executed',
        SECTION='\n# NESTED FUNCTIONS EXAMPLE #\n'))
    def greet():
        return '\t This is inside the greet() function'
    def welcome():
        return "\t This is inside the welcome() function"

    print(greet())
    print(welcome())
    print("Now we are back inside the hello() function")


def new_decorator(func):
    def wrap_func():
        print("Code would be here, before executing the func")

        # func()

        print("Code here will execute after the func()")

    return wrap_func


@new_decorator
def func_needs_decorator():
    print("This function is in need of a Decorator")



if __name__ == '__main__':
    check_for_locals(),
    hello()
    greet = hello
    print(greet)
    del hello
    print(greet())
    testing()
    print("")
    func_needs_decorator()
