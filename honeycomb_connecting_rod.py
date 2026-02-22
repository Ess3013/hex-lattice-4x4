# -*- coding: utf-8 -*-
"""
Abaqus Python Script: Honeycomb Lattice Connecting Rod with Vibration Absorption
MENG3505_Project01 Implementation

Design Variables:
- Beam slenderness ratio: beta = h/L
- Configuration angle: theta

Design Objectives:
- Eliminate plasticity in lattice members
- Minimize buckling instabilities
- Minimize onset frequency of first significant bandgap
- Maximize width of first significant bandgap
"""

from abaqus import *
from abaqusConstants import *
import part
import material
import section
import assembly
import step
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import regionToolset
import math
import os

# ============================================================
# PARAMETERS
# ============================================================

# Geometry Parameters (per project specifications)
L = 0.3                    # Beam length (hexagon side length) in cm
BETA = 1.0 / 15.0          # Initial slenderness ratio (h/L)
h = L * BETA               # Beam cross-section height/diameter in cm

# Configuration angle (angle from horizontal for lattice orientation)
THETA = 0.0                # Initial configuration angle in degrees (0 for standard honeycomb)

# Cell count - Aspect ratio Lx/Ly >= 2 for horizontal elongation
NUM_COLS = 20              # Number of hexagons horizontally (more for bandgap visibility)
NUM_ROWS = 10              # Number of hexagons vertically

# Material: Aluminum Boron Carbide Composite
# Using consistent cm-based units: Force in N, Length in cm, Time in s
YOUNGS_MODULUS = 70e5      # N/cm² (70 GPa)
POISSONS_RATIO = 0.33
DENSITY = 2.7e-6           # kg/cm³ (2700 kg/m³)
YIELD_STRESS = 276e3       # N/cm² (276 MPa) - typical for Al-B4C composite

# Load Parameters
STATIC_LOAD = 10000.0      # 10 kN compressive load in N
DYNAMIC_LOAD_AMPLITUDE = 10000.0  # 10^4 N for vibration analysis
FREQ_MIN = 0.0             # Minimum frequency in Hz
FREQ_MAX = 1000.0          # Maximum frequency in Hz

# Mesh Parameters
ELEM_PER_BEAM = 3          # Elements per beam segment

# ============================================================
# MODEL SETUP
# ============================================================
modelName = 'HoneycombRod'
mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)

# ============================================================
# CREATE PART
# ============================================================
partName = 'HoneycombLattice'
mdb.models[modelName].Part(name=partName, dimensionality=TWO_D_PLANAR,
                           type=DEFORMABLE_BODY)
p = mdb.models[modelName].parts[partName]

# ============================================================
# DEFINE MATERIAL
# ============================================================
matName = 'Aluminum_B4C'
mdb.models[modelName].Material(name=matName)
mdb.models[modelName].materials[matName].Elastic(
    table=((YOUNGS_MODULUS, POISSONS_RATIO), ))
mdb.models[modelName].materials[matName].Density(
    table=((DENSITY, ), ))

# Add plasticity data (elastic-perfectly plastic)
mdb.models[modelName].materials[matName].Plastic(
    table=((YIELD_STRESS, 0.0), ))

# ============================================================
# DEFINE BEAM SECTION
# ============================================================
sectionName = 'BeamSection'
# Circular cross-section with diameter = h
mdb.models[modelName].CircularProfile(name='CircProf', r=h/2)
mdb.models[modelName].BeamSection(name=sectionName,
                                  material=matName,
                                  integration=BEFORE_ANALYSIS,
                                  profile='CircProf',
                                  poissonRatio=POISSONS_RATIO)

# ============================================================
# HEXAGON GEOMETRY CALCULATIONS
# ============================================================
# For pointy-top hexagons (vertices at top/bottom):
# - Side length = L
# - Width (flat-to-flat) = L * sqrt(3)
# - Height (vertex-to-vertex) = 2 * L

hex_width = L * math.sqrt(3)       # Flat-to-flat width
hex_height = 2 * L                  # Vertex-to-vertex height

# Spacing for honeycomb pattern
h_spacing = hex_width               # Horizontal spacing between centers
v_spacing = 1.5 * L                 # Vertical spacing between row centers

# Calculate vertices for a single hexagon (pointy-top orientation)
# Apply configuration angle rotation if theta != 0
hex_vertices_local = []
for i in range(6):
    base_angle_deg = 30 + 60 * i  # Pointy-top: 30°, 90°, 150°, 210°, 270°, 330°
    base_angle_rad = math.radians(base_angle_deg)
    
    # Apply configuration angle rotation
    if THETA != 0:
        theta_rad = math.radians(THETA)
        # Rotate the vertex position
        x_local = L * math.cos(base_angle_rad)
        y_local = L * math.sin(base_angle_rad)
        # Rotate by theta
        x_rot = x_local * math.cos(theta_rad) - y_local * math.sin(theta_rad)
        y_rot = x_local * math.sin(theta_rad) + y_local * math.cos(theta_rad)
        hex_vertices_local.append((x_rot, y_rot))
    else:
        x = L * math.cos(base_angle_rad)
        y = L * math.sin(base_angle_rad)
        hex_vertices_local.append((x, y))

# ============================================================
# CREATE SKETCH AND GEOMETRY
# ============================================================
s = mdb.models[modelName].ConstrainedSketch(name='__profile__',
                                            sheetSize=200.0)

def addHexagonToSketch(centerX, centerY):
    """Add a hexagon wire to the sketch at the specified center location"""
    coords = []
    for vx, vy in hex_vertices_local:
        coords.append((centerX + vx, centerY + vy))
    
    # Create 6 lines to form the hexagon
    for i in range(6):
        startIdx = i
        endIdx = (i + 1) % 6
        s.Line(point1=coords[startIdx], point2=coords[endIdx])

# Create hexagonal array (honeycomb pattern)
hexCenters = []
for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        # Calculate center position
        centerX = col * h_spacing
        centerY = row * v_spacing
        
        # Stagger odd rows horizontally for honeycomb pattern
        if row % 2 == 1:
            centerX += h_spacing / 2
        
        hexCenters.append((centerX, centerY))
        addHexagonToSketch(centerX, centerY)

# ============================================================
# CALCULATE BOUNDARY BOX
# ============================================================
# Find extreme points for perimeter walls
all_vertices = []
for cx, cy in hexCenters:
    for vx, vy in hex_vertices_local:
        all_vertices.append((cx + vx, cy + vy))

minX = min(v[0] for v in all_vertices)
maxX = max(v[0] for v in all_vertices)
minY = min(v[1] for v in all_vertices)
maxY = max(v[1] for v in all_vertices)

# ============================================================
# CREATE PERIMETER BOUNDARY WALLS
# ============================================================
# Bottom wall
s.Line(point1=(minX, minY), point2=(maxX, minY))
# Top wall
s.Line(point1=(minX, maxY), point2=(maxX, maxY))
# Left wall
s.Line(point1=(minX, minY), point2=(minX, maxY))
# Right wall
s.Line(point1=(maxX, minY), point2=(maxX, maxY))

# Create wire geometry from sketch
p.BaseWire(sketch=s)

# ============================================================
# ASSIGN BEAM SECTION
# ============================================================
allEdges = p.edges
region = regionToolset.Region(edges=allEdges)
p.SectionAssignment(region=region, sectionName=sectionName,
                    offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
                    thicknessAssignment=FROM_SECTION)

# ============================================================
# MESH SEEDING
# ============================================================
elemSize = L / ELEM_PER_BEAM
p.seedEdgeBySize(edges=allEdges, size=elemSize, constraint=FINER)

# ============================================================
# CREATE ASSEMBLY
# ============================================================
a = mdb.models[modelName].rootAssembly
a.DatumCsysByDefault(CARTESIAN)

instanceName = partName + '-1'
a.Instance(name=instanceName, part=p, dependent=ON)

# ============================================================
# CREATE ANALYSIS STEPS
# ============================================================

# Step 1: Static Analysis (compressive load)
stepName_Static = 'Step-Static'
mdb.models[modelName].StaticStep(name=stepName_Static, previous='Initial',
                                  nlgeom=OFF, timePeriod=1.0,
                                  initialInc=0.1, minInc=1e-5, maxInc=0.1)

# Step 2: Buckling Analysis (linear perturbation)
stepName_Buckling = 'Step-Buckling'
mdb.models[modelName].BuckleStep(name=stepName_Buckling, previous=stepName_Static,
                                  eigenvalue=10.0)

# Step 3: Frequency Extraction (for vibration analysis)
stepName_Freq = 'Step-Frequency'
mdb.models[modelName].FrequencyStep(name=stepName_Freq, previous='Initial',
                                     numEigenvalues=50, 
                                     acousticScaleFactor=1.0,
                                     normalization=MASS)

# Step 4: Steady State Dynamics (for FRF)
stepName_SSD = 'Step-SSD'
mdb.models[modelName].SteadyStateDynamicsStep(
    name=stepName_SSD, previous=stepName_Freq,
    frequencyScaleFactor=1.0,
    numIntervals=100,
    freqMin=FREQ_MIN,
    freqMax=FREQ_MAX,
    scaling=UNIFORM,
    damping=0.02)  # 2% structural damping

# ============================================================
# BOUNDARY CONDITIONS
# ============================================================
instance = a.instances[instanceName]
edges = instance.edges

bottomEdges = []
topEdges = []
leftEdges = []
rightEdges = []

# Find edges by position
for edge in edges:
    try:
        verts = edge.getVertices()
        if len(verts) >= 2:
            y1 = p.vertices[verts[0].index].point[1]
            y2 = p.vertices[verts[1].index].point[1]
            x1 = p.vertices[verts[0].index].point[0]
            x2 = p.vertices[verts[1].index].point[0]
            avgY = (y1 + y2) / 2.0
            avgX = (x1 + x2) / 2.0
            
            tolerance = 0.1
            
            if abs(avgY - minY) < tolerance:
                bottomEdges.append(edge)
            if abs(avgY - maxY) < tolerance:
                topEdges.append(edge)
            if abs(avgX - minX) < tolerance:
                leftEdges.append(edge)
            if abs(avgX - maxX) < tolerance:
                rightEdges.append(edge)
    except:
        pass

# Fixed BC on bottom edge (Encastre - all DOF fixed)
if bottomEdges:
    bottomRegion = regionToolset.Region(edges=bottomEdges)
    mdb.models[modelName].EncastreBC(name='BC-FixedBottom',
                                      createStepName=stepName_Static,
                                      region=bottomRegion)

# Symmetry BC on left edge (optional - for symmetric model)
# Uncomment if symmetry is desired
# if leftEdges:
#     leftRegion = regionToolset.Region(edges=leftEdges)
#     mdb.models[modelName].XsymmBC(name='BC-LeftSymm',
#                                   createStepName=stepName_Static,
#                                   region=leftRegion)

# ============================================================
# LOADS
# ============================================================

# Static compressive load on top edge
if topEdges:
    topRegion = regionToolset.Region(edges=topEdges)
    # Distribute 10 kN across top nodes
    mdb.models[modelName].ConcentratedForce(name='Load-Static',
                                            createStepName=stepName_Static,
                                            region=topRegion,
                                            cf1=0.0, cf2=-STATIC_LOAD,
                                            distributionType=UNIFORM,
                                            field='', localCsys=None)

# Dynamic harmonic load for vibration analysis (applied in SSD step)
# Create amplitude for harmonic loading
mdb.models[modelName].HarmonicAmplitude(name='HarmonicLoad',
                                        frequency=FREQ_MIN,
                                        start=0.0, end=1.0)

if topEdges:
    # Get top nodes for nodal force application
    topNodes = []
    inst = a.instances[instanceName]
    nodes = inst.nodes
    
    for node in nodes:
        nodeY = node.coord[1]
        if abs(nodeY - maxY) < 0.1:
            topNodes.append(node.label)
    
    if topNodes:
        topNodeRegion = regionToolset.Region(nodes=topNodes)
        # Apply harmonic force per node (distributed)
        forcePerNode = DYNAMIC_LOAD_AMPLITUDE / len(topNodes)
        mdb.models[modelName].ConcentratedForce(name='Load-Dynamic',
                                                createStepName=stepName_SSD,
                                                region=topNodeRegion,
                                                cf1=0.0, cf2=forcePerNode,
                                                amplitude='HarmonicLoad',
                                                distributionType=UNIFORM,
                                                field='', localCsys=None)

# ============================================================
# MESH - ELEMENT TYPE ASSIGNMENT
# ============================================================
# B21: 2-node linear beam element in plane
elemType = mesh.ElemType(elemCode=B21, elemLibrary=STANDARD)
p.setElementType(regions=region, elemTypes=(elemType,))

# Generate mesh
p.generateMesh()

# ============================================================
# FIELD OUTPUT REQUESTS
# ============================================================
# Ensure output for all steps
mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(
    variables=('U', 'RF', 'S', 'E', 'LE', 'PE', 'PEEQ'))

# Add strain energy output
mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(
    energyOutputRequested=ON)

# ============================================================
# HISTORY OUTPUT REQUESTS
# ============================================================
# Request reaction force and displacement history
mdb.models[modelName].historyOutputRequests['H-Output-1'].setValues(
    variables=('U', 'RF'))

# Add strain energy history for FRF analysis
mdb.models[modelName].HistoryOutputRequest(name='H-StrainEnergy',
                                           createStepName=stepName_SSD,
                                           variables=('ALLSE', 'ALLIE'),
                                           frequency=1)

# ============================================================
# CREATE JOB
# ============================================================
jobName = 'HoneycombRod_Analysis'
mdb.Job(name=jobName, model=modelName, 
        description='Honeycomb Lattice Connecting Rod Analysis',
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, 
        echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF,
        userSubroutine='', scratch='', resultsFormat=ODB, 
        multiprocessingMode=DEFAULT, numCpus=4)

# ============================================================
# SAVE MODEL
# ============================================================
savePath = os.path.join(os.path.dirname(__file__), 'HoneycombRod')
mdb.saveAs(pathName=savePath)

# ============================================================
# PRINT SUMMARY
# ============================================================
print("=" * 70)
print("HONEYCOMB LATTICE CONNECTING ROD MODEL CREATED SUCCESSFULLY!")
print("=" * 70)
print(f"\nModel Name: {modelName}")
print(f"Part Name: {partName}")
print(f"\nGEOMETRY PARAMETERS:")
print(f"  Beam Length (L): {L} cm")
print(f"  Slenderness Ratio (beta): {BETA} (1/{1/BETA:.0f})")
print(f"  Beam Height (h): {h:.4f} cm")
print(f"  Configuration Angle (theta): {THETA}°")
print(f"  Number of Cells: {NUM_COLS} x {NUM_ROWS} = {NUM_COLS * NUM_ROWS}")
print(f"  Aspect Ratio (Lx/Ly): {(NUM_COLS * h_spacing) / (NUM_ROWS * v_spacing):.2f}")
print(f"\nMATERIAL: Aluminum-B4C Composite")
print(f"  Young's Modulus: {YOUNGS_MODULUS/1e5:.1f} GPa")
print(f"  Poisson's Ratio: {POISSONS_RATIO}")
print(f"  Density: {DENSITY*1e6:.1f} kg/m³")
print(f"  Yield Stress: {YIELD_STRESS/1e3:.1f} MPa")
print(f"\nLOADS:")
print(f"  Static Compressive Load: {STATIC_LOAD/1000:.1f} kN")
print(f"  Dynamic Load Amplitude: {DYNAMIC_LOAD_AMPLITUDE/1000:.1f} kN")
print(f"  Frequency Range: {FREQ_MIN} - {FREQ_MAX} Hz")
print(f"\nANALYSIS STEPS:")
print(f"  1. {stepName_Static} - Static compressive load")
print(f"  2. {stepName_Buckling} - Linear buckling analysis")
print(f"  3. {stepName_Freq} - Natural frequency extraction")
print(f"  4. {stepName_SSD} - Steady-state dynamics (FRF)")
print(f"\nJob Name: {jobName}")
print("=" * 70)
print("\nTo run the analysis:")
print("  1. Open the model in Abaqus/CAE")
print("  2. Review/modify boundary conditions and loads")
print("  3. Submit job: mdb.jobs['" + jobName + "'].submit()")
print("=" * 70)
