# Hexagonal Lattice 4x4 - Abaqus FEA Model

## Project Overview

This project contains an **Abaqus Finite Element Analysis (FEA)** model for generating and analyzing a **4×4 hexagonal honeycomb lattice structure** with closed boundary walls. The lattice is designed with beam elements representing an aluminum material structure.

### Key Features

- **Honeycomb tiling pattern**: Each interior hexagon shares edges with 6 neighboring hexagons
- **Pointy-top hexagon orientation**: Vertices at top/bottom for proper edge-sharing geometry
- **Beam elements**: B21 (2-node linear beam) elements with circular cross-section
- **Aluminum material**: Young's modulus 70 GPa, Poisson's ratio 0.33
- **Perimeter boundary walls**: Closed sides touching outermost hexagon vertices
- **Pre-configured boundary conditions**: Fixed bottom edge, optional top load

## Specifications

| Parameter | Value | Description |
|-----------|-------|-------------|
| `SIDE_LENGTH` | 3.0 cm | Hexagon side length |
| `BEAM_THICKNESS` | 0.5 cm | Beam circular cross-section diameter |
| `NUM_COLS` | 4 | Number of hexagons horizontally |
| `NUM_ROWS` | 4 | Number of hexagons vertically |
| `YOUNGS_MODULUS` | 70e5 N/cm² | Aluminum elastic modulus |
| `POISSONS_RATIO` | 0.33 | Aluminum Poisson's ratio |
| `DENSITY` | 2.7e-6 kg/cm³ | Aluminum density |

### Geometry Calculations

- **Horizontal spacing** (between row centers): `SIDE_LENGTH × √3 ≈ 5.196 cm`
- **Vertical spacing** (between row centers): `1.5 × SIDE_LENGTH = 4.5 cm`
- **Odd row offset**: `h_spacing / 2 ≈ 2.598 cm`
- **Horizontal extent from center**: `SIDE_LENGTH × √3/2 ≈ 2.598 cm`
- **Vertical extent from center**: `SIDE_LENGTH = 3.0 cm`

## Files

| File | Description |
|------|-------------|
| `hex_lattice_4x4.py` | Python script to generate the Abaqus model |
| `HexLattice_4x4.cae` | Abaqus CAE model file (binary) |
| `.gitignore` | Git ignore rules for Abaqus temporary files |
| `QWEN.md` | This documentation file |

## Usage

### Running the Script

**Option 1: From Abaqus/CAE GUI**
1. Open Abaqus/CAE
2. Go to `File → Run Script...`
3. Select `hex_lattice_4x4.py`

**Option 2: Command Line**
```bash
abaqus cae noGUI=hex_lattice_4x4.py
```

### Running the Analysis

After generating the model:

1. Open `HexLattice_4x4.cae` in Abaqus/CAE
2. Navigate to the **Job** module
3. Right-click `HexLattice_4x4_Job` → **Submit**
4. Wait for completion, then click **Results** to view

### Modifying Parameters

Edit the `PARAMETERS` section at the top of `hex_lattice_4x4.py`:

```python
SIDE_LENGTH = 3.0      # Change hexagon size
BEAM_THICKNESS = 0.5   # Change beam diameter
NUM_COLS = 4           # Change number of columns
NUM_ROWS = 4           # Change number of rows
```

## Model Structure

### Abaqus Components

1. **Part**: `HexLattice` - 2D planar wire part with honeycomb geometry
2. **Material**: `Aluminum` - Elastic material with density
3. **Section**: `BeamSection` - Circular profile beam section
4. **Assembly**: Single instance of the lattice part
5. **Step**: `Step-1` - Static general step
6. **Boundary Conditions**:
   - `BC-FixedBottom`: Encastre (fully fixed) on bottom boundary
   - `Load-Top`: Concentrated force (-100 N) on top boundary
7. **Mesh**: B21 beam elements, ~3 elements per hexagon side
8. **Job**: `HexLattice_4x4_Job` - Analysis job ready to submit

### Geometry Generation

The script creates:
1. A constrained sketch with all hexagon edges
2. 4×4 honeycomb array with staggered rows
3. Perimeter boundary walls touching outermost vertices
4. Wire geometry from the sketch
5. Beam section assignment to all edges
6. Mesh seeding and element type assignment

## Development Notes

### Unit System

The model uses a **consistent cm-based unit system**:
- Length: cm
- Force: N
- Time: s
- Mass: kg (converted: 2700 kg/m³ → 2.7e-6 kg/cm³)
- Stress/Modulus: N/cm² (70 GPa → 70e5 N/cm²)

### Honeycomb Pattern

The lattice uses a **pointy-top hexagon orientation** with:
- Vertices at angles: 30°, 90°, 150°, 210°, 270°, 330°
- Odd rows offset horizontally by half the hexagon width
- This ensures each interior hexagon shares edges with exactly 6 neighbors

### Git Repository

The project is version-controlled and hosted at:
**https://github.com/Ess3013/hex-lattice-4x4**

```bash
git clone https://github.com/Ess3013/hex-lattice-4x4.git
```

## Troubleshooting

### Common Issues

1. **"No module named 'regionToolset'"**: Ensure all imports at the top of the script are present
2. **Beam section errors**: The script uses `CircularProfile` with `BEFORE_ANALYSIS` integration
3. **Boundary condition failures**: The script includes try/except for edge detection

### Cleaning Up

To regenerate the model from scratch:
1. Delete `HexLattice_4x4.cae` and `HexLattice_4x4.jnl`
2. Re-run `hex_lattice_4x4.py`

## Qwen Added Memories
- always push your changes to github
