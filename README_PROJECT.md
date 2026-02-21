# M ENG3505_Project01 - Honeycomb Lattice Connecting Rod with Vibration Absorption

## Project Overview

This project implements a **Finite Element Analysis (FEA)** model for designing and optimizing a **hexagonal honeycomb lattice structure** for use as a lightweight connecting rod with enhanced vibration-damping capabilities.

### Design Objectives

1. **Eliminate plasticity** in lattice members
2. **Minimize buckling** instabilities
3. **Minimize onset frequency** of the first significant bandgap
4. **Maximize width** of the first significant bandgap

### Design Variables

| Variable | Symbol | Range | Description |
|----------|--------|-------|-------------|
| Slenderness Ratio | β = h/L | 1/20 ≤ β ≤ 1/5 | Beam thickness to length ratio |
| Configuration Angle | θ | 10° ≤ θ ≤ 30° | Lattice orientation angle |

---

## Project Structure

```
hex-lattice-4x4/
├── honeycomb_connecting_rod.py    # Main model generation script
├── parametric_sweep.py            # Automated parameter variation
├── post_process_results.py        # ODB results extraction
├── generate_report.py             # Results compilation and plotting
├── Section0_Introduction.md       # Industrial applications review
├── README_PROJECT.md              # This file
└── [Generated Files]
    ├── HoneycombRod.cae           # Abaqus model file
    ├── HoneycombRod_Analysis.odb  # Results database
    ├── results_table.csv          # Summary table
    ├── optimization_report.txt    # Design recommendations
    └── *.png                      # Result plots
```

---

## Usage Instructions

### Prerequisites

- **Abaqus/CAE** (version 6.14 or later recommended)
- **Python 3.x** with matplotlib (for report generation)
- **JSON support** (built into Python 3)

### Step 1: Generate Base Model

**Option A: From Abaqus/CAE GUI**
1. Open Abaqus/CAE
2. Go to `File → Run Script...`
3. Select `honeycomb_connecting_rod.py`
4. Model will be generated and saved as `HoneycombRod.cae`

**Option B: Command Line**
```bash
abaqus cae noGUI=honeycomb_connecting_rod.py
```

### Step 2: Run Single Analysis (Optional)

To analyze the base configuration (β = 1/15, θ = 0°):

1. Open `HoneycombRod.cae` in Abaqus/CAE
2. Navigate to the **Job** module
3. Right-click `HoneycombRod_Analysis` → **Submit**
4. Wait for completion
5. Click **Results** to view

### Step 3: Run Parametric Sweep

To analyze multiple configurations across the design space:

**From Abaqus/CAE GUI:**
1. Open Abaqus/CAE
2. Go to `File → Run Script...`
3. Select `parametric_sweep.py`
4. The script will:
   - Generate models for all (β, θ) combinations
   - Submit jobs automatically
   - Save results to `parametric_results.json`

**Command Line:**
```bash
abaqus cae noGUI=parametric_sweep.py
```

**Note:** The parametric sweep may take several hours depending on:
- Number of configurations (default: 7 β values × 6 θ values = 42 jobs)
- Mesh density
- Computer specifications

### Step 4: Post-Process Results

Extract and analyze results from ODB files:

**From Abaqus/CAE GUI:**
1. Open Abaqus/CAE
2. Go to `File → Run Script...`
3. Select `post_process_results.py`
4. Results will be saved to:
   - `processed_results.json` (detailed results)
   - `results_summary.csv` (summary table)

**Command Line:**
```bash
abaqus cae noGUI=post_process_results.py
```

### Step 5: Generate Report

Compile results and generate optimization recommendations:

**From Python (outside Abaqus):**
```bash
python generate_report.py
```

This will generate:
- `results_table.csv` - Comprehensive results table
- `optimization_report.txt` - Design recommendations
- `stress_vs_beta.png` - Stress distribution plot
- `buckling_vs_beta.png` - Buckling analysis plot
- `bandgap_width_vs_beta.png` - Bandgap width plot
- `bandgap_onset_vs_beta.png` - Bandgap onset frequency plot
- `tradeoff_stress_bandgap.png` - Trade-off analysis

---

## Model Specifications

### Default Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Beam Length (L) | 0.3 cm | Hexagon side length |
| Slenderness (β) | 1/15 | h/L ratio (default) |
| Beam Height (h) | 0.02 cm | Cross-section diameter |
| Num Columns | 20 | Cells horizontally |
| Num Rows | 10 | Cells vertically |
| Aspect Ratio | ~3.5 | Lx/Ly ≥ 2 (per specs) |

### Material Properties (Aluminum-B₄C Composite)

| Property | Value | Unit |
|----------|-------|------|
| Young's Modulus | 70×10⁵ | N/cm² (70 GPa) |
| Poisson's Ratio | 0.33 | - |
| Density | 2.7×10⁻⁶ | kg/cm³ (2700 kg/m³) |
| Yield Stress | 276×10³ | N/cm² (276 MPa) |

### Analysis Steps

1. **Step-Static**: Static compressive load (10 kN)
2. **Step-Buckling**: Linear buckling analysis (10 modes)
3. **Step-Frequency**: Natural frequency extraction (50 modes)
4. **Step-SSD**: Steady-state dynamics (0-1000 Hz, FRF)

### Boundary Conditions

- **Bottom Edge**: Encastre (fully fixed - all DOF constrained)
- **Top Edge**: Concentrated compressive force (10 kN static, 10⁴ N dynamic)

---

## Modifying Parameters

### Change Default Configuration

Edit `honeycomb_connecting_rod.py`:

```python
# Geometry Parameters
L = 0.3                    # Beam length in cm
BETA = 1.0 / 15.0          # Slenderness ratio
THETA = 0.0                # Configuration angle (degrees)

# Cell count
NUM_COLS = 20              # Horizontal cells
NUM_ROWS = 10              # Vertical cells

# Load
STATIC_LOAD = 10000.0      # 10 kN
```

### Modify Sweep Range

Edit `parametric_sweep.py`:

```python
# Slenderness ratio sweep
BETA_VALUES = [1.0/20, 1.0/15, 1.0/12, 1.0/10, 1.0/8, 1.0/6, 1.0/5]

# Configuration angle sweep
THETA_VALUES = [0, 10, 15, 20, 25, 30]
```

### Adjust Frequency Range

```python
FREQ_MIN = 0.0             # Minimum frequency in Hz
FREQ_MAX = 1000.0          # Maximum frequency in Hz
```

---

## Understanding Results

### Plasticity Check

- **Safety Factor (SF)**: σ_yield / σ_max
  - SF > 1: No plasticity (safe)
  - SF < 1: Plasticity occurs (fail)

### Buckling Analysis

- **Load Factor (LF)**: Multiplier at which buckling occurs
  - LF > 1: Stable at applied load (safe)
  - LF < 1: Buckles before full load (fail)

### Bandgap Analysis

- **Onset Frequency**: Start of vibration attenuation band
- **Bandgap Width**: Frequency range of attenuation
- **Goal**: Low onset + wide bandgap = better vibration absorption

### Optimization Criteria

The optimal configuration balances:
1. No plasticity (SF > 1)
2. No buckling (LF > 1)
3. Lowest bandgap onset frequency
4. Widest bandgap width

---

## Troubleshooting

### Common Issues

**1. "Job did not complete successfully"**
- Check model for geometric errors
- Verify boundary conditions are properly applied
- Reduce mesh density if memory issues occur

**2. "No bandgap detected"**
- May need more unit cells (increase NUM_COLS, NUM_ROWS)
- Check frequency range covers bandgap location
- Verify SSD step is properly configured

**3. "Matplotlib not available"**
- Install: `pip install matplotlib`
- Or skip plot generation, use CSV output only

**4. Long computation times**
- Reduce number of sweep points
- Decrease mesh density (ELEM_PER_BEAM)
- Use fewer eigenvalues in frequency steps

### Cleaning Up

To regenerate from scratch:
```bash
# Delete generated files
rm *.cae *.jnl *.odb *.lck *.sta *.msg *.dat *.res *.prt *.mdl
rm parametric_results.json processed_results.json results_*.csv
rm optimization_report.txt *.png
```

---

## Output Files

### Model Files
- `*.cae` - Abaqus model database
- `*.jnl` - Journal file (command history)

### Results Files
- `*.odb` - Output database (results)
- `*.sta` - Status file (convergence)
- `*.msg` - Message file (warnings/errors)
- `*.dat` - Data file (summary)

### Report Files
- `results_table.csv` - Comprehensive results
- `optimization_report.txt` - Design recommendations
- `*.png` - Visualization plots
- `*.json` - Raw data (for further analysis)

---

## Project Deliverables

Per M ENG3505_Project01 requirements:

- [x] **Section 0**: Introduction with industrial applications review
- [x] **Model Construction**: Abaqus honeycomb lattice model
- [x] **Static Analysis**: 10 kN compressive load, elastic and elastic-plastic
- [x] **Buckling Analysis**: Linear perturbation buckling
- [x] **Vibration Analysis**: FRF and bandgap identification
- [x] **Parametric Sweep**: β and θ variation
- [x] **Optimization**: Optimal configuration selection
- [x] **Reporting**: Results tables, plots, and recommendations

---

## Additional Resources

### Abaqus Documentation
- [Abaqus Analysis User's Guide](https://help.3ds.com/products/simulia/abaqus/6.14/)
- [Abaqus Scripting Reference](https://help.3ds.com/products/simulia/abaqus/6.14/)

### Honeycomb Literature
- Gibson, L.J. & Ashby, M.F. (1997). *Cellular Solids: Structure and Properties*
- Ruzzene, M. & Scarpa, F. (2005). "Directional and wave propagation properties of auxetic honeycomb structures"

### Phononic Crystals
- Hussein, M.I. et al. (2014). "Dynamics of phononic materials and structures"
- Liu, Z. et al. (2000). "Locally resonant sonic materials"

---

## Contact & Support

For questions or issues:
1. Check this README first
2. Review Abaqus documentation
3. Consult course materials (M ENG3505)

---

*Last updated: February 2026*
