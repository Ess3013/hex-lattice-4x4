# Abaqus 2016 Scripting User's Guide

## Legal Notices
Abaqus, the 3DS logo, and SIMULIA are commercial trademarks or registered trademarks of Dassault Systèmes or its subsidiaries in the United States and/or other countries. Use of any Dassault Systèmes or its subsidiaries trademarks is subject to their express written approval.

Abaqus and this documentation may be used or reproduced only in accordance with the terms of the software license agreement signed by the customer, or, absent such an agreement, the then current software license agreement to which the documentation relates.

This documentation and the software described in this documentation are subject to change without prior notice.

Dassault Systèmes and its subsidiaries shall not be responsible for the consequences of any errors or omissions that may appear in this documentation.

© Dassault Systèmes, 2015

Other company, product, and service names may be trademarks or service marks of their respective owners. For additional information concerning trademarks, copyrights, and licenses, see the Legal Notices in the Abaqus 2016 Installation and Licensing Guide.

## Preface
This section lists various resources that are available for help with using Abaqus Unified FEA software.

### Support
Both technical software support (for problems with creating a model or performing an analysis) and systems support (for installation, licensing, and hardware-related problems) for Abaqus are offered through a global network of support offices, as well as through our online support system. Contact information for our regional offices is accessible from SIMULIA→Locations at www.3ds.com/simulia. The online support system is accessible by selecting the SUBMIT A REQUEST link at Support - Dassault Systèmes (http://www.3ds.com/support).

### Online support
Dassault Systèmes provides a knowledge base of questions and answers, solutions to questions that we have answered, and guidelines on how to use Abaqus, Engineering Process Composer, Isight, Tosca, fe-safe, and other SIMULIA products. The knowledge base is available by using the Search our Knowledge option on www.3ds.com/support (http://www.3ds.com/support).

By using the online support system, you can also submit new requests for support. All support/service requests are tracked. If you contact us by means outside the system to discuss an existing support problem and you know the support request number, please mention it so that we can query the support system to see what the latest action has been.

### Training
All SIMULIA regional offices offer regularly scheduled public training classes. The courses are offered in a traditional classroom form and via the Web. We also provide training seminars at customer sites. All training classes and seminars include workshops to provide as much practical experience with Abaqus as possible. For a schedule and descriptions of available classes, see the Training link at www.3ds.com/products-services/simulia (www.3ds.com/products-services/simulia) or call your support office.

### Feedback
We welcome any suggestions for improvements to Abaqus software, the support tool, or documentation. We will ensure that any enhancement requests you make are considered for future releases. If you wish to make a suggestion about the service or products, refer to www.3ds.com/simulia. Complaints should be made by contacting your support office or by visiting SIMULIA→Quality Assurance at www.3ds.com/simulia (www.3ds.com/simulia).

## Contents

### PART I: AN INTRODUCTION TO THE Abaqus Scripting Interface
1. An overview of the Abaqus Scripting User’s Guide
2. Introduction to the Abaqus Scripting Interface
   - Abaqus/CAE and the Abaqus Scripting Interface (2.1)
   - How does the Abaqus Scripting Interface interact with Abaqus/CAE? (2.2)
3. Simple examples
   - Creating a part (3.1)
   - Reading from an output database (3.2)
   - Summary (3.3)

### PART II: USING THE Abaqus Scripting Interface
4. Introduction to Python
   - Python and Abaqus (4.1)
   - Python resources (4.2)
   - Using the Python interpreter (4.3)
   - Object-oriented basics (4.4)
   - The basics of Python (4.5)
   - Programming techniques (4.6)
   - Further reading (4.7)
5. Using Python and the Abaqus Scripting Interface
   - Executing scripts (5.1)
   - Abaqus Scripting Interface documentation style (5.2)
   - Abaqus Scripting Interface data types (5.3)
   - Object-oriented programming and the Abaqus Scripting Interface (5.4)
   - Error handling in the Abaqus Scripting Interface (5.5)
   - Extending the Abaqus Scripting Interface (5.6)
6. Using the Abaqus Scripting Interface with Abaqus/CAE
   - The Abaqus object model (6.1)
   - Copying, deleting, and renaming Abaqus Scripting Interface objects (6.2)
   - Abaqus/CAE sequences (6.3)
   - Namespace (6.4)
   - Specifying what is displayed in the viewport (6.5)
   - Specifying a region (6.6)
   - Prompting the user for input (6.7)
   - Interacting with Abaqus/Standard, Abaqus/Explicit, and Abaqus/CFD (6.8)
   - Using Abaqus Scripting Interface commands in your environment file (6.9)

### PART III: THE Abaqus PYTHON DEVELOPMENT ENVIRONMENT
7. Using the Abaqus Python development environment
   - An overview of the Abaqus Python development environment (7.1)
   - Abaqus PDE basics (7.2)
   - Using the Abaqus PDE (7.3)

### PART IV: PUTTING IT ALL TOGETHER: EXAMPLES
8. Abaqus Scripting Interface examples
   - Reproducing the cantilever beam tutorial (8.1)
   - Generating a customized plot (8.2)
   - Investigating the skew sensitivity of shell elements (8.3)
   - Editing display preferences and GUI settings (8.4)

### PART V: ACCESSING AN OUTPUT DATABASE
9. Using the Abaqus Scripting Interface to access an output database
   - What do you need to access the output database? (9.1)
   - How the object model for the output database relates to commands (9.2)
   - Object model for the output database (9.3)
   - Executing a script that accesses an output database (9.4)
   - Reading from an output database (9.5)
   - Writing to an output database (9.6)
   - Exception handling in an output database (9.7)
   - Computations with Abaqus results (9.8)
   - Improving the efficiency of your scripts (9.9)
   - Example scripts that access data from an output database (9.10)
10. Using C++ to access an output database
    - Overview (10.1)
    - What do you need to access the output database? (10.2)
    - Abaqus Scripting Interface documentation style (10.3)
    - How the object model for the output database relates to commands (10.4)
    - Object model for the output database (10.5)
    - Compiling and linking your C++ source code (10.6)
    - Accessing the C++ interface from an existing application (10.7)
    - The Abaqus C++ API architecture (10.8)
    - Utility interface (10.9)
    - Reading from an output database (10.10)
    - Writing to an output database (10.11)
    - Exception handling in an output database (10.12)
    - Computations with Abaqus results (10.13)
    - Improving the efficiency of your scripts (10.14)
    - Example programs that access data from an output database (10.15)
