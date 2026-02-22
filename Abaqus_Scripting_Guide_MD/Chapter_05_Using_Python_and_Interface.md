# 5. Using Python and the Abaqus Scripting Interface

This section explains how Python and the Abaqus Scripting Interface combine to provide a powerful interface to Abaqus/CAE.

The following topics are covered:
* “Executing scripts,” Section 5.1
* “Abaqus Scripting Interface documentation style,” Section 5.2
* “Abaqus Scripting Interface data types,” Section 5.3
* “Object-oriented programming and the Abaqus Scripting Interface,” Section 5.4
* “Error handling in the Abaqus Scripting Interface,” Section 5.5
* “Extending the Abaqus Scripting Interface,” Section 5.6

## 5.1 Executing scripts
* If your script does not access Abaqus/CAE, run it via `abaqus python scriptname.py`.
* If it accesses Abaqus/CAE modules, execute it within Abaqus/CAE via **File→Run Script**.
* Scripts accessing an output database must include `from odbAccess import *`.

## 5.2 Abaqus Scripting Interface documentation style
The Abaqus Scripting Reference Guide uses a consistent style:
* **Access:** How to access an instance of the object.
* **Path:** The path to the constructor.
* **Arguments:** Required and optional arguments.
* **Return value:** The object or value returned by the command.

## 5.3 Abaqus Scripting Interface data types
Abaqus adds over 500 additional data types:
* **SymbolicConstants:** All-caps constants like `ON`, `OFF`, `ISOTROPIC`.
* **Booleans:** Python `True`/`False` or Abaqus `ON`/`OFF`.
* **Repositories:** Containers for objects of the same type (e.g., `mdb.models`, `mdb.models['Model-1'].parts`).

## 5.4 Object-oriented programming and the Abaqus Scripting Interface
* **Methods:** Commands that operate on objects (e.g., `viewport.setValues()`).
* **Constructors:** Methods that create objects (e.g., `mdb.Model()`).
* **Members:** Properties of an object (e.g., `viewport.width`). Members are generally read-only; use `setValues()` to modify them.

## 5.5 Error handling in the Abaqus Scripting Interface
Abaqus issues specific exceptions:
* `InvalidNameError`: For invalid object names.
* `RangeError`: When a numeric value is out of range.
* `AbaqusError` and `AbaqusException`: Context-dependent errors.

## 5.6 Extending the Abaqus Scripting Interface
You can store custom data in the model database using the `customKernel` module.
```python
import customKernel
mdb = Mdb()
mdb.customData.myString = 'The width is '
```
Custom data is saved with the model database and can be retrieved later. You can also create custom repositories and classes derived from `CommandRegister` or `RepositorySupport` to interact with the Abaqus/CAE GUI.
