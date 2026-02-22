# 7. Using the Abaqus Python development environment

The Abaqus Python development environment (PDE) is an application in which you can create, edit, test, and debug Python scripts.

## 7.1 An overview of the Abaqus Python development environment
The Abaqus PDE is a separate application that you can access from within Abaqus/CAE or launch independently. It enables you to set breakpoints, step through code, and watch variables.

![Figure 7–1: The Abaqus PDE interface. Shows the main window with script editor, debugger controls, and CLI.]

## 7.2 Abaqus PDE basics

### 7.2.1 Starting the Abaqus Python development environment
* From Abaqus/CAE: **File→Abaqus PDE**.
* From the command prompt: `abaqus cae -pde` or `abaqus pde`.

### 7.2.2 Managing files in the Abaqus PDE
The file to be tested is designated as the **Main File**. The PDE supports `.py` and `.guiLog` files.

### 7.2.3 Editing files in the Abaqus PDE
The Edit menu includes standard tools (Undo, Redo, Copy, Paste) plus script-specific tools like **Indent Region**, **Comment Region**, etc.

### 7.2.4 Selecting the settings for use with a file
Settings allow you to control:
* **Recording Options:** For UI actions.
* **Run Script In:** Choose between GUI, Kernel, or Local processes.
* **Line Animation:** Highlight the line currently being executed.

## 7.3 Using the Abaqus PDE

### 7.3.1 Creating .guiLog files
You can record actions in the Abaqus/CAE GUI into a `.guiLog` file by clicking the **Start Recording** icon in the PDE.

### 7.3.2 Running a script
Click **Play** to run the main file. Use **Next Line**, **Stop**, **Go to Start**, and **Go to End** for granular control.

### 7.3.3 Using the debugger
The debugger includes a call stack, debug buttons, and a **Watch List** to monitor variable values as the script executes.

### 7.3.4 Using breakpoints
Add a breakpoint by clicking in the margin or pressing **[F9]**. Script execution will pause at these points.

### 7.3.5 Using the Abaqus PDE with plug-ins
Open the plug-in file in the PDE, add breakpoints, and then start the plug-in from within Abaqus/CAE to begin debugging.
