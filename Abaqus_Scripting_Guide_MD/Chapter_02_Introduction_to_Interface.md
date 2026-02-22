# 2. Introduction to the Abaqus Scripting Interface

The following topics are covered:
* “Abaqus/CAE and the Abaqus Scripting Interface,” Section 2.1
* “How does the Abaqus Scripting Interface interact with Abaqus/CAE?,” Section 2.2

## 2.1 Abaqus/CAE and the Abaqus Scripting Interface
When you use the Abaqus/CAE graphical user interface (GUI) to create a model and to visualize the results, commands are issued internally by Abaqus/CAE after every operation. These commands reflect the geometry you created along with the options and settings you selected from each dialog box. The GUI generates commands in an object-oriented programming language called Python. The commands issued by the GUI are sent to the Abaqus/CAE kernel. The kernel interprets the commands and uses the options and settings to create an internal representation of your model. The kernel is the brains behind Abaqus/CAE. The GUI is the interface between the user and the kernel.

The Abaqus Scripting Interface allows you to bypass the Abaqus/CAE GUI and communicate directly with the kernel. A file containing Abaqus Scripting Interface commands is called a script. You can use scripts to do the following:

* **To automate repetitive tasks.** For example, you can create a script that executes when a user starts an Abaqus/CAE session. Such a script might be used to generate a library of standard materials. As a result, when the user enters the Property module, these materials will be available. Similarly, the script might be used to create remote queues for running analysis jobs, and these queues will be available in the Job module.
* **To perform a parametric study.** For example, you can create a script that incrementally modifies the geometry of a part and analyzes the resulting model. The same script can read the resulting output databases, display the results, and generate annotated hard copies from each analysis.
* **Create and modify the model databases and models** that are created interactively when you work with Abaqus/CAE. The Abaqus Scripting Interface is an application programming interface (API) to your model databases and models. For a discussion of model databases and models, see “What is an Abaqus/CAE model database?,” Section 9.1 of the Abaqus/CAE User’s Guide, and “What is an Abaqus/CAE model?,” Section 9.2 of the Abaqus/CAE User’s Guide.
* **Access the data in an output database.** For example, you may wish to do your own postprocessing of analysis results. You can write your own data to an output database and use the Visualization module of Abaqus/CAE to view its contents.

The Abaqus Scripting Interface is an extension of the popular object-oriented language called Python. Any discussion of the Abaqus Scripting Interface applies equally to Python in general, and the Abaqus Scripting Interface uses the syntax and operators required by Python.

## 2.2 How does the Abaqus Scripting Interface interact with Abaqus/CAE?
Figure 2–1 illustrates how Abaqus Scripting Interface commands interact with the Abaqus/CAE kernel.

![Figure 2–1: Abaqus Scripting Interface commands and Abaqus/CAE. The diagram shows the interaction between the GUI, CLI, and scripts through the Python interpreter to the Abaqus/CAE kernel, generating input files for analysis products like Abaqus/Standard and Abaqus/Explicit, which then produce an output database.]

Abaqus Scripting Interface commands can be issued to the Abaqus/CAE kernel from one of the following:

* **The graphical user interface (GUI).** For example, when you click OK or Apply in a dialog box, the GUI generates a command based on your options and settings in the dialog box. You can use the Macro Manager to record a sequence of the generated Abaqus Scripting Interface commands in a macro file. For more information, see “Creating and running a macro,” Section 9.5.5 of the Abaqus/CAE User’s Guide.
* **The command line interface (CLI).** Click `>>>` in the lower left corner of the main window to display the command line interface (CLI). You can type a single command or paste in a sequence of commands from another window; the command is executed when you press [Enter]. You can type any Python command into the command line; for example, you can use the command line as a simple calculator.
  * *Note:* When you are using Abaqus/CAE, errors and messages are posted into the message area. Click the icon in the lower left corner of the main window to display the message area.
* **Scripts.** If you have more than a few commands to execute or if you are repeatedly executing the same commands, it may be more convenient to store the set of statements in a file called a script. A script contains a sequence of Python statements stored in plain ASCII format. For example, you might create a script that opens an output database, displays a contour plot of a selected variable, customizes the legend of the contour plot, and prints the resulting image on a local PostScript printer. In addition, scripts are useful for starting Abaqus/CAE in a predetermined state. For example, you can define a standard configuration for printing, create remote queues, and define a set of standard materials and their properties.

### Running a script when you start Abaqus/CAE
You can run a script when you start an Abaqus/CAE session by typing the following command:
```bash
abaqus cae script=myscript.py
```
where `myscript.py` is the name of the file containing the script. The equivalent command for Abaqus/Viewer is:
```bash
abaqus viewer script=myscript.py
```
Arguments can be passed into the script by entering `--` on the command line, followed by the arguments separated by one or more spaces. These arguments will be ignored by the Abaqus/CAE execution procedure, but they will be accessible within the script.

### Running a script without the Abaqus/CAE GUI
You can run a script without the Abaqus/CAE GUI by typing the following command:
```bash
abaqus cae noGUI=myscript.py
```
where `myscript.py` is the name of the file containing the script. The equivalent command for Abaqus/Viewer is:
```bash
abaqus viewer noGUI=myscript.py
```
The Abaqus/CAE kernel is started without the GUI. Running a script without the Abaqus/CAE GUI is useful for automating pre- or postanalysis processing tasks without the added expense of running a display. When the script finishes running, the Abaqus/CAE kernel terminates.

### Running a script from the startup screen
When you start an Abaqus/CAE session, Abaqus displays the startup screen. You can run a script from the startup screen by clicking **Run Script**. Abaqus displays the Run Script dialog box, and you select the file containing the script.

### Running a script from the File menu
You can run a script by selecting **File→Run Script** from the main menu bar. Abaqus displays the Run Script dialog box, and you select the file containing the script.

### Running a script from the command line interface
You can run a script from the command line interface (CLI) by typing the following command:
```python
execfile('myscript.py')
```
where `myscript.py` is the name of the file containing the script and the file in this example is in the current directory. Figure 2–2 shows an example script being run from the command line interface.

![Figure 2–2: Scripts can be run from the command line interface. A screenshot showing the CLI with the command execfile('modelAExample.py') and the message 'The model "Model A" has been created.']
