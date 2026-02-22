# 8. Abaqus Scripting Interface examples

This chapter provides detailed example scripts that combine Abaqus Scripting Interface commands and Python statements.

## 8.1 Reproducing the cantilever beam tutorial
This example script (`beamExample.py`) reproduces the cantilever beam tutorial found in the Getting Started guide.

![Figure 8–1: A loaded cantilever beam. Diagram showing a beam of 200mm length, 25mm width, 20mm height, with a 0.5 MPa pressure applied.]

### Key Script Steps:
1. Create a model and viewport.
2. Create a sketch and extrude it to create a part.
3. Define material properties (Steel) and a solid section.
4. Instance the part in the assembly.
5. Define a static step.
6. Apply boundary conditions (Encastre at one end) and a pressure load.
7. Mesh the part instance and submit the job.
8. Open the output database and display a contour plot.

## 8.2 Generating a customized plot
Example scripts show how to open an output database, change the displayed frame, customize contour legend limits, and print the resulting plot to a `.png` file.

## 8.3 Investigating the skew sensitivity of shell elements
This example study evaluates the sensitivity of shell elements (S4 and S8R) to skew distortion. The script iterates through various skew angles (90°, 80°, 60°, 40°, 30°) and generates X-Y plots of displacement and bending moments.

![Figure 8–2: A 4x4 quadrilateral mesh of the plate. Shows the skew angle $\delta$.]

### Script Highlights (`skewExample.py`):
* Uses `findAt` to identify faces and vertices.
* Modifies an angular dimension in the sketch to skew the geometry.
* Sets up a structured mesh.
* Automates job submission and results extraction.

## 8.4 Editing display preferences and GUI settings
You can use the `caePrefsAccess` module to edit the `abaqus_2016.gpr` file, which controls default GUI behaviors like window size and location.
```python
import caePrefsAccess
sessionOptions = caePrefsAccess.openSessionOptions()
sessionOptions['session.animationController.animationOptions']['frameRate'] = 50
sessionOptions.save()
```
