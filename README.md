## Overview
An Interpreter for `plox`, a dynamically-typed language. This is a Python implementation of Part II of Bob Nystrom's [Crafting Interpreters](http://www.craftinginterpreters.com/).

## Tutorial
- comments
```sh
`this is a comment
`this is another comment
```

- statements
```sh
var a; `this is a statement. statements are delimited by ;
a = 1 + 10; `this is another statement
```

- variables
```sh
var count;
count = 1;
var name = "joe";
print count;
print name;

```
- arithmetic operations
```sh
`supported operators: +, -, /, *, % (for modulo/remainder), &, |, etc
var a = 10;
var b = 2;
var sum = a + b;
print sum;
```

- loops
```sh
var max_num = 10
var num = 0;
while (n < max_num) {
    print "num is " + num;
    num = num + 1;
}

` for loops are syntactic sugars for while loops
for (var num = 0; num < max_num; num = num + 1) {
    print "num is " + num;
}
```

- functions
```sh
`print fizzbuzz for numbers up to n.
fun fizzbuzz(n) {
    var fizz = "fizz";
    var buzz = "buzz";
    if (n < 1) print "n is " + n + ". pick a value greater than 0.";

    for (var i = 1; i <= n; i = i + 1) {
        var div_by_three = i % 3 == 0;
        var div_by_five = i % 5 == 0;
        
        if (div_by_three and div_by_five) {
            print fizz + buzz;
        } else if (div_by_three) {
            print fizz;
        } else if (div_by_five) {
            print buzz;
        } else {
            print i + " ";
        }            
    }
}

fizzbuzz(21);
```

- closures (and currying)
```sh
fun print_one() {
    var one = 1;
    var two = 2;

    fun print_one_plus_two() {
        print one + two;
    }

    return print_one_plus_two;
}

print_one()();
```

Plox code can be run in a REPL (for interactive programming) or in batch mode (by passing a file containing plox code)
```sh
python plox.py -- for REPL. inside the REPL you can type and run any valid plox code.
python plox.py -s plox_file.plox -- for batch mode.
```

## Implementation
Given a string representing valid plox code, we:
1. Tokenize the string
2. Generate ASTs from the tokenized string
3. Interpret the ASTs

All three a performed via `Scanner`, `Parser`, and `Interpreter` respectively.

## Grammar
```txt
program -> declaration* EOF ;
declaration -> variable_declaration | function_declaration | statement ;
variable_declaration -> "var" IDENTIFIER ( "=" expression )? ";"
function_declaration -> "fun" function ;
function -> IDENTIFIER "(" parameters? ")" block ;
parameters -> IDENTIFIER ( "," IDENTIFIER )* ;
statement -> for_statement | while_statement | if_statement | print_statement | return_statement | break_statement | block | expression_statement ;
for_statement -> "for" "(" ( variable_declaration | expression | ";" ) expression? ";" expression? ")" statement ;
while_statement -> "while" "(" expression ")" statement ;
if_statement -> "if" "(" expression ")" statement ( "else" statement )? ;
print_statement -> "print" expression ";" ;
return_statement -> "return" expression? ";" ;
break_statement -> "break" ";" ;
block_statement -> "{" declaration* "}" ;
expression_statement -> expression ";" ;
expression -> ternary ;
ternary -> assignment | ternary ;
assignment -> logical_or ( "=" ternary )* ;
logical_or -> logical_and ( "or" logical_and )* ;
logical_and -> bitwise_or ( "|" bitwise_or )* ;
bitwise_or -> bitwise_and ( "&" bitwise_and )* ;
equality -> comparison ( ( "!=" | "==" ) comparison )* ;
comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term -> factor ( ( "+" | "-" ) factor )* ;
factor -> unary ( ( "/" | "*" | "%" ) unary )* ;
unary -> ( ( "!" | "-" ) unary )* | power ;
power -> call ( "^" power )* ;
call -> primary ( "(" arguments? ")" )* ;
arguments -> expression ( "," expression )* ;
primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER
```