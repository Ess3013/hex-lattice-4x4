# 9. Using the Abaqus Scripting Interface to access an output database

This section describes the architecture of an output database (.odb) and how to use Python to access and manipulate its data.

## 9.3 Object model for the output database
The ODB object model hierarchy is essential for accessing results.

![Figure 9–1: The output database object model. Hierarchical structure starting from the Odb object to parts, sections, materials, and steps.]

### 9.3.1 Model data
* **Parts:** Collection of nodes, elements, surfaces, and sets.
* **Root Assembly:** Collection of positioned part instances.
* **Materials and Sections:** Definitions copied from the model database.

### 9.3.2 Results data
* **Steps:** Sequence of one or more analysis procedures.
* **Frames:** Increments of analysis (e.g., time increments, eigenmodes).
* **Field Output:** Data for a large portion of the model (e.g., stress tensors).
* **History Output:** Data for a single point or region (e.g., energy, displacement at a node).

## 9.5 Reading from an output database
```python
from odbAccess import *
odb = openOdb(path='viewer_tutorial.odb')
lastFrame = odb.steps['Step-1'].frames[-1]
displacement = lastFrame.fieldOutputs['U']
```

## 9.6 Writing to an output database
You can create a new ODB and add model and results data.
```python
odb = Odb(name='myData', path='testWrite.odb')
part1 = odb.Part(name='part-1', embeddedSpace=THREE_D, type=DEFORMABLE_BODY)
# Add nodes, elements, steps, and frames...
odb.save()
```

## 9.8 Computations with Abaqus results
Mathematical operations are supported for `FieldOutput`, `FieldValue`, and `HistoryOutput` objects.
```python
deltaDisp = field2 - field1
```

## 9.10 Example scripts
Detailed scripts are provided for tasks such as:
* Finding the maximum von Mises stress.
* Creating an ODB from scratch.
* Computing stress ranges over multiple load cases.
* Transforming field results to different coordinate systems.
* Viewing acoustic far-field analysis results.
