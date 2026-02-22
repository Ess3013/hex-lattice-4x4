# 6. Using the Abaqus Scripting Interface with Abaqus/CAE

This section discusses how you can use the Abaqus Scripting Interface to control Abaqus/CAE models and analysis jobs.

The following topics are covered:
* “The Abaqus object model,” Section 6.1
* “Copying, deleting, and renaming Abaqus Scripting Interface objects,” Section 6.2
* “Abaqus/CAE sequences,” Section 6.3
* “Namespace,” Section 6.4
* “Specifying what is displayed in the viewport,” Section 6.5
* “Specifying a region,” Section 6.6
* “Prompting the user for input,” Section 6.7
* “Interacting with Abaqus/Standard, Abaqus/Explicit, and Abaqus/CFD,” Section 6.8
* “Using Abaqus Scripting Interface commands in your environment file,” Section 6.9

## 6.1 The Abaqus object model
The hierarchy and the relationship between objects used by Abaqus/CAE is called the Abaqus object model. It consists of:
* **Session:** Objects not saved between sessions (e.g., viewports).
* **Mdb:** Objects saved in a model database (e.g., models, parts, materials).
* **Odb:** Objects saved in an output database (e.g., results).

![Figure 6–1: The Abaqus object model overview. Shows the root objects: session, mdb, and odb.]

### 6.1.1 An overview of the Abaqus object model
* **Containers:** Repositories or sequences that hold objects of a similar type.
* **Singular objects:** Objects that are not containers (e.g., `Session`, `Mdb`).

### 6.1.3 The Model object model
The `Mdb` object contains one or more `Model` objects. Each `Model` object contains parts, assemblies, steps, loads, and materials.

![Figure 6–4: The structure of the objects under the Model object. Hierarchical view including parts, materials, steps, etc.]

## 6.4 Namespace
Namespaces prevent conflict between variable names.
* **Script namespace (`__main__`):** Where commands from scripts and the CLI are executed.
* **Journal namespace (`journaling`):** Where commands from the GUI are recorded (in `abaqus.rpy`).

## 6.6 Specifying a region
Many commands require a region argument. Use the `findAt` method instead of integer IDs to identify geometric entities.
```python
pillarVertices = doorInstance.vertices.findAt(((-40,30,0),), ((40,0,0),) )
```

## 6.7 Prompting the user for input
* `getInput`: Single text input.
* `getInputs`: Multiple text inputs.
* `getWarningReply`: Yes/No reply to a warning.

## 6.9 Using Abaqus Scripting Interface commands in your environment file
The Abaqus environment file (`abaqus_v6.env`) is read at startup. You can use it to set default preferences.
```python
def onCaeStartup():
    session.printOptions.setValues(vpDecorations=OFF)
```
