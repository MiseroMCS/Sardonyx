#Sardonyx Documentation
##Basic Usage

To enter an interactive shell, just run the Sardonyx executable with no arguments.

To run a file, specify it in the first argument.

When running an interactive shell, the command "debug" will toggle debug mode. Debug mode is really messy and makes it basically impossible to get much done. It's good for two things, developing the language itself and trying to work past the obscure error messages. It just shows a list of tokens that are found by the interpreter and make Syntax Error messages in the actual execution stage more descriptive (there will be a "(HERE)" somewhere in the massive list of things next to the offending token).

You can enter debug mode when running a file by making the second argument "debug". See above text on the actual usage of this, though.

##Literals
There are only 2 literal types in Sardonyx, Numbers and Strings. Strings are as you'd expect, text in double quotes. Numbers are a plus or minus sign (not optional, you need a plus sign for positive numbers), stored as floats (so you can use ridiculously high/low numbers if you want).

##Defining Functions
Functions are defined like variables, but substituting the place where you'd put a literal with a dollar sign ("$") followed by a block of code denoted with curly braces ("{" and "}").

Example: ```var foo = ${var test = (test + +1)}```

##Expressions
Expressions can be used when defining a variable's value. Expressions are always enclosed in parentheses. Valid operators are "+", "==", "!=", ">", "<", ">=", and "<=" (all self explanatory). Here's an example expression: ```var foo = (+5 + bar)```. This expression sets the value of 'foo' to 'bar' plus 5. Booleans are literally just numbers, 1 is true and 0 is false. Expressions cannot be nested.

##Conditionals
Wow, Turing Completeness. You can do an if statement using the 'if' keyword. It's formatted like this: ```if [number variable/number literal] ![function name]```. If the number literal/variable is equal to one, it will run the specified function. Otherwise it will do nothing.

##Loops
Loops will run a function until the condition specified is no longer true. It's formatted like this: ```while [number variable/number literal] ![function name]```. If the number literal/variable is equal to one, it will run the specified function until that is no longer true (a literal will run forever). Otherwise it will do nothing. It is suggested that you include a delay in any loop that runs for a large period of time, because otherwise things might be a bit buggy and prone to freezing. This occurs mostly when doing output, but it's best practice to do it regardless. A delay function is included in 'examples/std.sdx'.

##Running Python Code
This is a good feature to fill in the gaps of my sub-par language. A python block starts with an "@" and then a block using curly braces to define it. Remember, the code is crunched down to one line so you're limited to statements seperated by semicolons (yes, python can use semicolons). If you need an if statement or anything that requires indenting, you're doing it wrong. This statement is for implementing features into libraries that can't be replicated otherwise, not for writing entire programs.

##Actually Writing A Program
In this "tutorial" I'm going to assume you're writing to a file rather than the shell. It should work mostly the same but it's so much easier to organize when it's in a file.

We're going to be writing a basic "Hello, world!" program. Sardonyx has no built in print function, so we need to use something from a library. There's a basic library ("std.sdx") in the examples/ directory, so we'll use that.
```import examples/std.sdx``` will append the contents of examples/std.sdx to the top of the file, which will include all of the functions and things included there.

Next, we'll define the string we're going to be outputting. Just do ```var string1 = "Hello, world!";```. The name 'string1' is necessary, as the print function uses a variable named 'string1' as an argument (this is really arbitrary and a result of the way I made the language).

Then we just run the print function, which is just ```!print```.

To break this down a bit more, variable definition in Sardonyx is done in this format:

```var [variable name] = [variable value];```

The style of the spaces is mandatory, again an artifact of the way this language works on the inside. Variable names consist of a letter/underscore, then any combination of letters, numbers, or underscores.

Calling a function in Sardonyx is done with an exclamation point. The style is like this:

```![function name]```
