# 3. Simple examples

Programming with the Abaqus Scripting Interface is straightforward and logical. To illustrate how easy it is to write your own programs, the following sections describe two simple Abaqus Scripting Interface scripts.
* “Creating a part,” Section 3.1
* “Reading from an output database,” Section 3.2

You are not expected to understand every line of the examples; the terminology and the syntax will become clearer as you read the detailed explanations in the following chapters. “Summary,” Section 3.3, describes some of the principles behind programming with Python and the Abaqus Scripting Interface.

## 3.1 Creating a part
The first example shows how you can use an Abaqus/CAE script to replicate the functionality of Abaqus/CAE. The script does the following:
* Creates a new model in the model database.
* Creates a two-dimensional sketch.
* Creates a three-dimensional, deformable part.
* Extrudes the two-dimensional sketch to create the first geometric feature of the part.
* Creates a new viewport.
* Displays a shaded image of the new part in the new viewport.

The new viewport and the shaded part are shown in Figure 3–1.

![Figure 3-1: The example creates a new viewport and a part. A screenshot of Abaqus/CAE showing a 3D part in the shape of the letter 'A' in a viewport.]

The example scripts from this guide can be copied to the user’s working directory by using the Abaqus fetch utility:
```bash
abaqus fetch job=scriptName
```
where `scriptName.py` is the name of the script. Use the following command to retrieve the script for this example:
```bash
abaqus fetch job=modelAExample
```

### 3.1.1 The example script
```python
"""
modelAExample.py
A simple example: Creating a part.
"""
from abaqus import *
from abaqusConstants import *
backwardCompatibility.setValues(includeDeprecated=True, reportDeprecated=False)

import sketch
import part

myModel = mdb.Model(name='Model A')
mySketch = myModel.ConstrainedSketch(name='Sketch A', sheetSize=200.0)

xyCoordsInner = ((-5 , 20), (5, 20), (15, 0), (-15, 0), (-5, 20))
xyCoordsOuter = ((-10, 30), (10, 30), (40, -30), (30, -30), (20, -10), 
                 (-20, -10), (-30, -30), (-40, -30), (-10, 30))

for i in range(len(xyCoordsInner)-1):
    mySketch.Line(point1=xyCoordsInner[i], point2=xyCoordsInner[i+1])

for i in range(len(xyCoordsOuter)-1):
    mySketch.Line(point1=xyCoordsOuter[i], point2=xyCoordsOuter[i+1])

myPart = myModel.Part(name='Part A', dimensionality=THREE_D, type=DEFORMABLE_BODY)
myPart.BaseSolidExtrude(sketch=mySketch, depth=20.0)

myViewport = session.Viewport(name='Viewport for Model A', origin=(10, 10), width=150, height=100)
myViewport.setValues(displayedObject=myPart)
myViewport.partDisplay.setValues(renderStyle=SHADED)
```

### 3.1.2 How does the script work?
This section explains each portion of the example script.

#### `from abaqus import *`
This statement makes the basic Abaqus objects accessible to the script. It also provides access to a default model database using the variable named `mdb`. The statement `from abaqusConstants import *` makes the Symbolic Constants defined by the Abaqus Scripting Interface available to the script.

#### `import sketch`, `import part`
These statements provide access to the objects related to sketches and parts. `sketch` and `part` are called Python modules.

#### `myModel = mdb.Model(name='Model A')`
This statement creates a new model named 'Model A' and stores it in the model database `mdb`.

![Figure 3-2: Creating a new model. Diagram showing how mdb.Model creates a model and assigns it to a variable.]

#### `mySketch = myModel.ConstrainedSketch(name='Sketch A', sheetSize=200.0)`
This statement creates a new sketch object named 'Sketch A' in `myModel`.

#### `for i in range(len(xyCoordsInner)-1):`
This loop creates the inner profile of the letter “A” in `mySketch`. Note that Python uses only indentation to signify the start and end of a loop.

#### `myPart = myModel.Part(name='Part A', dimensionality=THREE_D, type=DEFORMABLE_BODY)`
This statement creates a three-dimensional, deformable part named 'Part A'.

#### `myPart.BaseSolidExtrude(sketch=mySketch, depth=20.0)`
This extrudes the sketch through a depth of 20.0.

#### `myViewport = session.Viewport(...)`
This creates a new viewport in the session.

## 3.2 Reading from an output database
The second example shows how you can use the Abaqus Scripting Interface to read an output database, manipulate the data, and display the results using the Visualization module in Abaqus/CAE.

![Figure 3-3: The resulting contour plot. A Mises stress contour plot showing the results of superimposing variables from different steps.]

### 3.2.1 The example script
```python
"""
odbExample.py
Script to open an output database, superimpose variables
from the last frame of different steps, and display a contour
plot of the result.
"""
from abaqus import *
from abaqusConstants import *
import visualization

myViewport = session.Viewport(name='Superposition example', origin=(10, 10), width=150, height=100)

# Open the tutorial output database.
myOdb = visualization.openOdb(path='viewer_tutorial.odb')

# Associate the output database with the viewport.
myViewport.setValues(displayedObject=myOdb)

# Create variables that refer to the first two steps.
firstStep = myOdb.steps['Step-1']
secondStep = myOdb.steps['Step-2']

# Read displacement and stress data from the last frame of the first two steps.
frame1 = firstStep.frames[-1]
frame2 = secondStep.frames[-1]

displacement1 = frame1.fieldOutputs['U']
displacement2 = frame2.fieldOutputs['U']

stress1 = frame1.fieldOutputs['S']
stress2 = frame2.fieldOutputs['S']

# Find the added displacement and stress caused by the loading in the second step.
deltaDisplacement = displacement2 - displacement1
deltaStress = stress2 - stress1

# Create a Mises stress contour plot of the result.
myViewport.odbDisplay.setDeformedVariable(deltaDisplacement)
myViewport.odbDisplay.setPrimaryVariable(field=deltaStress, 
    outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Mises'))

myViewport.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))
```

## 3.3 Summary
* You can run a script from the Abaqus/CAE startup screen, the **File→Run Script** menu, or from the CLI.
* Use the `import` statement to make the required set of commands available.
* A command that creates an object is called a constructor and starts with an uppercase character (e.g., `mdb.Model`).
* Python scripts use indentation to control loops and blocks.
* Python includes built-in functions like `len()`.
* You can use commands to replicate any operation performed interactively in Abaqus/CAE.
