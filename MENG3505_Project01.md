# DESIGN A HONEYCOMB LATTICE FOR A CONNECTING ROD WITH VIBRATION ABSORPTION CAPABILITIES

## Project Overview
Design a two-dimensional hexagonal honeycomb lattice structure to be used as the core of a lightweight connecting rod with enhanced vibration-damping capabilities. See Figure 1.

### Design Variables
*   **Beam slenderness ratio**: $\beta = h/L$
*   **Configuration angle**: $	heta$

### Design Objectives
*   Eliminate plasticity in the lattice members.
*   Minimize buckling instabilities in the lattice.
*   Minimize the onset frequency of the first significant bandgap.
*   Maximize the width of the first significant bandgap.

---

## Procedure

### 0) Introduction
Write a brief introduction (not longer than one page) with references, reviewing industrial applications for honeycomb lattice structures. 
*   What materials are used? Why? 
*   How are they being manufactured? Why?

### Model Construction
Construct the model in ABAQUS through the spatial repetition of beam elements. 
*   **Dimensions**: Let $L = 0.3$ cm and $\beta = 1/15$ (initial slenderness ratio).
*   **Material**: Use Aluminum (e.g., an Aluminum Boron Carbide composite) as your reference material.
*   **Setup**: Load and constrain the system as shown in Figure 2.

### Analysis Steps
1.  **Static Analysis**: Solve the system assuming a static compressive load of **10kN** is applied. Assume linear elastic material behavior, then elastic-perfectly plastic behavior.
2.  **Buckling Analysis**: Re-solve to check if the lattice members buckle for the selected slenderness ratio and load.
3.  **Vibration Analysis**: Re-solve and use the structure's frequency response function (FRF) to identify the vibration absorption capability of the lattice. You can use the strain energy for the entire system for analysis. Inspect the FRF curve and estimate:
    *   The onset frequency of the first significant bandgap.
    *   The width of the first significant bandgap.
4.  **Parametric Sweep**: Repeat the above analyses for several values of the lattice design variables and compare your results.
    *   Sweep range: $1/20 \le \beta \le 1/5$
    *   Sweep range: $10^\circ \le 	heta \le 30^\circ$
5.  **Optimization**: Pick the lattice configuration that optimizes the structure's performance based on the analyses. You can carry out the procedure manually or use the **PYTHON script** supplied to facilitate your lattice generation.
6.  **Reporting**: Present your results clearly. Comment on the impact that changes in the design variables might have on other properties of the part (weight, cost, durability, wet and dry friction coefficients, etc.).

---

## Hints

1.  **Vibration Analysis Force**: Apply to each of the top nodes the nodal force:
    $$F_y = F_{0y} e^{i\omega t}$$
    Where $F_{0y} = 10^4$ N and $\omega \in [0, 1000]$ Hz.
2.  **Unit Cell Density**: Choose the number of cells in the device by compromising between the performance of the device and the computational cost of the analysis. You need enough unit cells to see bandgaps.
3.  **Meshing**: Choose the elements per beam in your FE mesh by compromising the solution's accuracy and the analysis's computational cost.
4.  **Aspect Ratio**: Pick the number of cells along $x$ and $y$ so the structure is longer in the horizontal direction (suggested aspect ratio $2 \le L_x/L_y$).
