# 4. Introduction to Python

This section provides a basic introduction to the Python programming language. You are encouraged to try the examples and to experiment with Python statements. The Python language is used throughout Abaqus, not only in the Abaqus Scripting Interface.

The following topics are covered:
* “Python and Abaqus,” Section 4.1
* “Python resources,” Section 4.2
* “Using the Python interpreter,” Section 4.3
* “Object-oriented basics,” Section 4.4
* “The basics of Python,” Section 4.5
* “Programming techniques,” Section 4.6
* “Further reading,” Section 4.7

## 4.1 Python and Abaqus
Python is the standard programming language for Abaqus products and is used in several ways:
* The Abaqus environment file uses Python statements.
* The parameter definitions on the data lines of the `*PARAMETER` option in the Abaqus input file are Python statements.
* The parametric study capability of Abaqus requires the user to write and to execute a Python scripting (`.psf`) file.
* Abaqus/CAE records its commands as a Python script in the replay (`.rpy`) file.
* You can execute Abaqus/CAE tasks directly using a Python script.
* You can access the output database (`.odb`) using a Python script.

## 4.2 Python resources
The official Python web site ([www.python.org](http://www.python.org)) contains a wealth of information, including tutorials and reference libraries. Many books are also available, such as *Python Essential Reference* and *Learning Python*.

## 4.3 Using the Python interpreter
Python is an interpreted language. You can run the Python interpreter in several ways:
* Type `abaqus python` at the system prompt.
* Use the command line interface (CLI) provided by Abaqus/CAE at the bottom of the window.

## 4.4 Object-oriented basics
Python is an object-oriented programming language. An object encapsulates some data (members) and functions (methods) that manipulate those data. Classes define the structure of objects, and an object is an instance of a class.

## 4.5 The basics of Python

### 4.5.1 Variable names and assignment
```python
>>> myName = 'Einstein'
>>> myName
'Einstein'
>>> 3.0 / 4.0
0.75
```
Variable names must start with a letter or underscore and can contain numbers. They are case-sensitive.

### 4.5.2 Python data types
* **Integer:** `i = 20`
* **Long Integer:** `nodes = 2000000L`
* **Float:** `pi = 3.14159`
* **Complex:** `a = 2 + 4j`

### 4.5.3 Determining the type of a variable
Use the `type()` function:
```python
>>> a = 2.375
>>> type(a)
<type 'float'>
```

### 4.5.4 Sequences
| Type | Mutable | Homogeneous | Methods | Syntax |
| :--- | :--- | :--- | :--- | :--- |
| list | Yes | No | Yes | `[9.0, 'b']` |
| tuple | No | No | No | `('a', 45)` |
| string| No | Yes | Yes | `'stress'` |
| array | Yes | Yes | Yes | `array((1.2, 2.3), (2.5, 5.8))` |

### 4.5.5 Sequence operations
* **Slicing:** `myList[1:4]`
* **Repeat:** `x * 2`
* **Length:** `len(myString)`
* **Concatenation:** `a + b`
* **Range:** `range(2, 8)`

### 4.5.6 Python None
The `None` object represents an empty value.

### 4.5.7 Continuation lines and comments
Use `` for line continuation if not inside delimiters `()`, `{}`, `[]`. Comments start with `#`.

### 4.5.8 Printing variables using formatted output
```python
>>> print 'Vibration frequency = %6.2f' % freq
```

### 4.5.9 Control blocks
Python uses indentation to define blocks.
* **if, elif, else**
* **while**
* **for**

## 4.6 Programming techniques

### 4.6.1 Creating functions
```python
def distance(x, y):
    a = x**2 + y**2
    return a ** 0.5
```

### 4.6.2 Using dictionaries
Dictionaries map keys to values.
```python
>>> myPart = {'size': 3.0, 'material': 'Steel'}
```

### 4.6.3 Reading and writing from files
```python
>>> inputFile = open('foam.txt', 'r')
>>> lines = inputFile.readlines()
>>> inputFile.close()
```

### 4.6.4 Error handling
```python
try:
    outputFile = open('foam.txt')
except IOError, error:
    print 'Exception trapped: ', error
```

### 4.6.5 Functions and modules
Modules group functionality. Use `import math` or `from math import *`.

### 4.6.6 Writing your own modules
Save functions in a `.py` file and import it using the filename (without extension).
