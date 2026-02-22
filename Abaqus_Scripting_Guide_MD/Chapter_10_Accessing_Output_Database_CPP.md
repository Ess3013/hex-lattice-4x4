# 10. Using C++ to access an output database

The C++ interface is intended for users with high-performance requirements. It is closely related to the Abaqus Scripting Interface but tailored for the C++ language.

## 10.1 Overview
A working knowledge of C++ is assumed. Postprocessing programs must be compiled and linked using the `abaqus make` utility and must begin with an `ABQmain` function.

## 10.8 The Abaqus C++ API architecture
* **Class naming convention:** All class names start with `odb_` (e.g., `odb_String`, `odb_Odb`).
* **Constructors:** 
  * Standard C++ constructors for nonpersistent objects.
  * Methods on existing objects for persistent objects (e.g., `step1.Frame()`).
  * `addNodes`, `addElements`, and `addData` for objects created in large quantities.

## 10.9 Utility interface
A set of utilities is provided for common data structures:
* **Strings:** `odb_String`.
* **Sequences:** `odb_SequenceInt`, `odb_SequenceFloat`, etc.
* **Repositories:** Containers retrieved by name (e.g., `odb_PartRepository`).

## 10.10 Reading from an output database
```cpp
#include <odb_API.h>
odb_Odb& odb = openOdb("viewer_tutorial.odb");
odb_Step& step = odb.steps()["Step-1"];
odb_SequenceFrame& allFramesInStep = step.frames();
```

## 10.11 Writing to an output database
```cpp
odb_Odb& odb = Odb("myData", "derived data", "test", "testWrite.odb");
odb_Part& part1 = odb.Part("part-1", odb_Enum::THREE_D, odb_Enum::DEFORMABLE_BODY);
// Add nodes, elements...
odb.save();
```

## 10.15 Example programs
Complete C++ source code is provided for:
* Finding maximum von Mises stress (`odbMaxMises.C`).
* Creating an output database from scratch.
* Filtering an ODB to retain only specific frames.
* Computing stress ranges over multiple load cases.
* Postprocessing elbow element results (FELBOW).
