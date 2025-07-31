from discord.ext import commands

class PythonWiki(commands.Cog):
    @commands.group(name="pythonwiki")
    async def pythonwiki(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("A small Python wiki. Type the keyword/function you want info as a command. (e.g, >pythonwiki print). >execute is also a good tool for experimenting.")
    
    pythonwiki.command(name="and")
    async def and_kw(self, ctx):
        await ctx.send("""
`and` is a logical operator. It returns `True` if all conditions are `True`, otherwise `False`
Example:
```py
print(7>3 and 15+4>9)
# Output: True
```
""")
    
    @pythonwiki.command(name="as")
    async def as_kw(self, ctx):
        await ctx.send("""
`as` is used to create an alias for a module, or an exception.
Example:
```py
from time import time as t
print(t)
```""")
    
    @pythonwiki.command(name="assert")
    async def assert_kw(self, ctx):
        await ctx.send("""
`assert` is used for debugging. It checks if a condition is `True`, otherwise an `AssertionError` is raised. You can also add a message if the `AssertionError` is raised
Example:
```py
assert 5 == 5, "5 shouldn't equal to 5!" # If 5 doesn't equal to 5, it will raise an AssertionError: 5 shouldn't equal to 5!
```""")
        
    @pythonwiki.command(name="break")
    async def break_kw(self, ctx):
        await ctx.send("""
`break` is used for breaking out a `for` or a `while` loop. It immediately exits the innermost loop in which it appears.
Example:
```py
string = "Python"
for i in string:
    if i == "h":
        break
    print(i)
```""")
        
    @pythonwiki.command(name="class")
    async def class_kw(self, ctx):
        await ctx.send("""
The `class` keyword is used to define class. Think of it like a blueprint.
Example:
```py
class Person:
    name = "John"
    age = 33
    height = 170

person1 = Person()
print(person1.name)```""")
        
    @pythonwiki.command(name="continue")
    async def continue_kw(self, ctx):
        await ctx.send("""
`continue` is used to end the current iteration of a loop, and continues to the next iteration.
Example:
```py
string = "Python"
for i in string:
    if i == "o":
        continue
    print(i)
```""")
        
    @pythonwiki.command(name="def")
    async def def_kw(self, ctx):
        await ctx.send("""
`def` is used to define a function. A function is a named, reusable block of code designed to perform a specific task.
Example:
```py
    def ping():
        print("Pong!")
```""")
        
    @pythonwiki.command(name="del")
    async def del_kw(self, ctx):
        await ctx.send("""
`del` is used to delete an object. Since everything in Python is an object. It can also be used for variables, lists,...
Example:
```py
x = [1, 2, 3]
del x
print(x) # NameError: name 'x' is not defined```""")
    
    @pythonwiki.command(name="elif")
    async def elif_kw(self, ctx):
        await ctx.send("""
`elif` is used in conditional statements. 
An `if` statement is evaluated first. If its condition is true, the code block associated with the `if` statement is executed, and the rest of the `elif/else` chain is skipped. 
If the if condition is false, the program proceeds to the first `elif` statement.
The `elif` condition is then evaluated. If it is true, its corresponding code block is executed, and the rest of the chain is skipped.
This process continues for any subsequent `elif` statements.
If none of the `if` or `elif` conditions are true, the `else` block (if present) is executed.
Example:
```py
age = 15

if age >= 18:
    print("You are an adult.")
elif age >= 13:
    print("You are a teenager.")
else:
    print("You are a child.")
```""")
        
    @pythonwiki.command(name="else")
    async def else_kw(self, ctx):
        await ctx.send("""
`else` is used in conditional statements, or a `for` loop, or a `try-except-else-finally` block (what the fuck).

When there are multiple conditions to check, `elif` (short for "else if") statements can be chained after an `if` statement. 
The `else` block then executes if none of the `if` or `elif` conditions are `True`.
Example:
```py
score = 75
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```
`else` can also be used with `for` loops. 
The else block associated with a `for` loop executes only if the loop completes without encountering a `break` statement.
Example:
```py
for i in range(5):
    if i == 6:  # This condition will never be met
        print("Found 6!")
        break
else:
    print("Loop completed without finding 6")
```
           
The `else` clause in a `try-except` block executes if no exception occurs within the `try` block.
Example:
```py
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Cannot divide by zero!")
else:
    print("Division successful:", result)
```
""")
        
    @pythonwiki.command(name="except")
    async def except_kw(self, ctx):
        await ctx.send("""
`except` is used to handle errors. It's used in a `try-except` block. You can also assign different blocks for different errors.
Example:
```py
try:
    print(1/0)
except ZeroDivisionError:
    print("You cannot divide by zero!")
```""")
    
    @pythonwiki.command(name="False")
    async def false_kw(self, ctx):
        await ctx.send("""
`False` is a built-in constant representing the Boolean value of false. It is one of the two Boolean literal values, the other being `True`. These values are fundamental for logical operations, conditional statements, and controlling program flow.
`False` is an instance of the `bool` type, which is a subclass of `int`. This means `False` can be treated as `0` in numerical contexts, although its primary purpose is to represent truth values.
Example:
```py
is_active = False
if is_active:
    print("User is active")
else:
    print("User is not active")
print(int(False))
```""")
        
    @pythonwiki.command(name="finally")
    async def finally_kw(self, ctx):
        await ctx.send("""
`finally` is used with exceptions, a block of code that will be executed no matter if there is an exception or not.
Example:
```py
try:
    print(1/0)
except ZeroDivisionError:
    print("You cannot divide by zero!")
finally:
    print("This try-except block is fully executed.")
```""")
        
    @pythonwiki.command(name="for")
    async def for_kw(self, ctx):
        await ctx.send("""
`for` is used to declare a `for` loop, which iterates through an iterable object, like a list, tuple,...
Example:
```py
for i in range(9):
    print(i**2)
```
""")
    
    @pythonwiki.command(name="from")
    async def from_kw(self, ctx):
        await ctx.send("""
`from` is used to import specific parts of a module.
Example:
```py
from random import randint
print(randint(10, 20))
```""")
    
    @pythonwiki.command(name="global")
    async def global_kw(self, ctx):
        await ctx.send("""
`global` is used to declare global variables from a non-global scope such as . A global variable can be accessed anywhere.
Example:
```py
def func():
    global x
    x = 2

func()
print(x)
```""")
    
    @pythonwiki.command(name="if")
    async def if_kw(self, ctx):
        await ctx.send("""
`if` is used to declare an `if` statement. An `if` statement is a fundamental control flow construct used for conditional execution. It allows a program to make decisions and execute specific blocks of code only if a given condition evaluates to `True`.
Example:
```py
x = None
if x is None:
    print("x doesn't have any value.")
```""")
        
    @pythonwiki.command(name="import")
    async def import_kw(self, ctx):
        await ctx.send("""
`import` is used to import a module
Example:
```py
import math
print(math.cos(180))
```""")
    
    @pythonwiki.command(name="in")
    async def in_kw(self, ctx):
        await ctx.send("""
`in` is used to check if a value is present in a list, tuple, ...
Example:
```py
numbers = range(8)
print(9 in numbers)```""")

    @pythonwiki.command(name="is")
    async def is_kw(self, ctx):
        await ctx.send("""
In Python, every object resides at a specific memory location. The `is` operator compares the **memory addresses** of two objects.
The `==` operator, on the other hand, compares the **values** of two objects. Two distinct objects can have the same value, in which case `==` would return `True` but `is` would return `False`.
Example:
```py
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]

    print(a is b)  # True (a and b refer to the same list object)
    print(a is c)  # False (a and c are distinct list objects, even with same content)
    print(a == c)  # True (a and c have the same content)
```""")
        
    @pythonwiki.command(name="lambda")
    async def lambda_kw(slef, ctx):
        await ctx.send("""
A `lambda` function is an anonymous, single-expression function defined using the `lambda` keyword. Unlike standard functions defined with `def`, lambda functions do not require a name and implicitly return the result of their single expression.
Example:
```py
square = lambda x: x ** 2
print(square(6))
```""")
        
    @pythonwiki.command(name="None")
    async def none_kw(self, ctx):
        await ctx.send("""
`None` is used to represent the absence of a value. `No`ne doesn't equal to `0`, `False` or any other values. Only `None` can be `None`. `None` is a class of is own, `NoneType`.
Example:
```py
x = None
print(type(x))```""")
        
    @pythonwiki.command(name="nonlocal")
    async def nonlocal_kw(self, ctx):
        await ctx.send("""
The `nonlocal` keyword in Python is used within nested functions to explicitly declare that a variable refers to a variable in the nearest enclosing, but non-global, scope. This allows modification of variables in an outer function from within an inner function. 
Without `nonlocal`, if an inner function assigns a value to a variable with the same name as a variable in an outer scope, Python would by default create a new local variable within the inner function, effectively "shadowing" the outer variable. The `nonlocal` keyword prevents this shadowing and directs the interpreter to modify the existing variable in the enclosing scope.
Example:
```py
def outer_function():
    message = "Hello"

    def inner_function():
        nonlocal message
        message = "Hello, Python!"
        print("Inside inner:", message)

    inner_function()
    print("Inside outer:", message)

outer_function()
```""")
    
    @pythonwiki.command(name="not")
    async def not_kw(self, ctx):
        await ctx.send("""
`not` is used to invert the value of an expression, if that expression is `True`, `not` returns `False` and vice versa. If used in a Boolean context (e.g `True or `False`), `not` inverts the value. `not` can also be used with non-Boolean values. In this case, Python will consider it as `True` or `False`(called "truthy and "falsy"). Falsy values includes 0, an empty string, an empty list, an empty dictionary,...""")
        
    @pythonwiki.command(name="or")
    async def or_kw(self, ctx):
        await ctx.send("""
`or` returns `True` at least one expression is `True`, otherwise `False`. If used in a Boolean context (e.g `True or `False`), `or` returns `True` if at least one boolean is `True`. `or` can also be used with non-Boolean values. In this case, Python will consider it as `True` or `False` (called "truthy and "falsy"). Falsy values includes 0, an empty string, an empty list, an empty dictionary,...""")
    
    @pythonwiki.command("pass")
    async def pass_kw(self, ctx):
        await ctx.send("""
`pass` declares a null statement. A null statement does nothing.
Example:
```py
def useless():
    pass
```""")
        
    @pythonwiki.command(name="raise")
    async def raise_kw(self, ctx):
        await ctx.send("""
`raise` is used to raise an exception. You can define what type of error to raise, and the message to print.
Example:
```py
    pi = 3.14159
    if pi != 3.14159:
        raise Exception("No, a circle is supposed to be a circle")
```""")
        
    @pythonwiki.command(name="return")
    async def return_kw(self, ctx):
        await ctx.send("""
The `return` keyword is used to exit a function and return a value.
Example:
```py
def something():
    return "I ran out of creativity"
```""")
        
    @pythonwiki.command(name="False")
    async def true_kw(self, ctx):
        await ctx.send("""
`True` is a built-in constant representing the Boolean value of true. It is one of the two Boolean literal values, the other being `False`. These values are fundamental for logical operations, conditional statements, and controlling program flow.
`True` is an instance of the `bool` type, which is a subclass of `int`. This means `True` can be treated as `1` in numerical contexts, although its primary purpose is to represent truth values.
Example:
```py
is_active = True
if is_active:
    print("User is active")
else:
    print("User is not active")
print(int(True))
```""")
    
    @pythonwiki.command(name="try")
    async def try_kw(self, ctx):
        await ctx.send("""
The `try` statement in Python is a fundamental construct for handling exceptions, which are errors that occur during the execution of a program. It allows for graceful error handling, preventing a program from crashing and enabling it to continue execution or provide informative error messages.
Example:
```py
try:
    # Code that might raise an exception
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
```""")
    
    @pythonwiki.command(name="while")
    async def while_kw(self, ctx):
        await ctx.send("""
`while` is used to declare a `while` loop. A while loop runs until the specified condition is False:
Example:
```py
x = 0

while x <= 9:
  print(x)
  x = x + 1
```""")
        
    @pythonwiki.command(name="with")
    async def with_kw(self, ctx):
        await ctx.send("""
The `with` keyword in Python is used for resource management, primarily to ensure that resources are properly acquired and released, even in the event of errors. It works in conjunction with context managers, which are objects that implement the `__enter__()` and `__exit__()` methods.
Example:
```py
with open("example.txt", "w") as file:
    file.write("This is a test.")
# File is automatically closed here
```""")
    
    @pythonwiki.command(name="yield")
    async def yield_kw(self, ctx):
        await ctx.send("""
The `yield` keyword in Python is used to create generator functions. Unlike a `return` statement, which terminates a function and returns a single value, `yield` returns a value and pauses the function's execution, allowing it to resume from where it left off when the next value is requested.
Example:
```py
def count_up_to(max_val):
    count = 1
    while count <= max_val:
        yield count 
        count += 1

for number in count_up_to(5):
    print(number)
```""")

async def setup(bot):
    await bot.add_cog(PythonWiki(bot))