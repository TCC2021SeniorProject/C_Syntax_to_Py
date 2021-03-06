# Module: C syntax to python converter
A module for translator that converts non-Python language's operational or conditional commands to Python scripts.

- Can handle assignment, conditional statements.
  - However, inputs must not include any keyword like "if", "else if", "else".
- Reforms Syntax
- Balances the parsing tree for correct brackets postioning

Used data structure: [website](https://cap.ecn.purdue.edu/compilers/project/step1/)

[<img src="https://cap.ecn.purdue.edu/compilers/project/step1/parsetree.png">](https://cap.ecn.purdue.edu)

## Usage Restriction
Program does not handle invalid statements. Please make sure that the compiler accepts the syntax before the use.
- Statement must be valid(Must be valid syntax)
- Additional brackets are accepted, but whenever the brackets are opened, it must be closed.
- Only translates supported operators

Supported operators(leftside is C-syntax and rightside is Python-syntax):
```py
  "&&" : "and",
  "||" : "or",
  ">=" : ">=",
  "<=" : "<=",
  "==" : "==",
  ">" : ">",
  "<" : "<",
  "!=" : "!=",
  "=" : "=",
  "<=" : "=",
  ":=" : "=",
  "//=" : "//=",
  "//=" : "//=",
  "+=" : "+=",
  "-=" : "-=",
  "/=" : "/=",
  "*=" : "*=",
  "%=" : "%=",
  "&=" : "&=",
  "|=" : "|=",
  "^=" : "^=",
 ```

Supported expression:
```py
  '(' : '(',
  '!' : 'not'
  '++' : "+= 1"
  '--' : "-= 1"
```

## Test cases:
1. a>= 2&&!b !=true
2. a>=2&&!(b!=false)
3. (a>=2)&&!(b!=false)
4. ((a>=2))&&!(b!=4)
5. (e&&(a>=2))&&!(b!=4)
6. (!a)&&b--
7. ++b&&(!a)
8. a := b++

## Actual outputs
1. a >= 2 and not b  != True
2. a >= 2 and not (b != False)
3. (a >= 2) and not (b != False)
4. ((a >= 2)) and not (b != 4)
5. (e and (a >= 2)) and not (b != 4)
6. (not a) and b -= 1
7. b += 1 and (not a)
8. a  = b += 1
