# -*- coding: utf-8 -*-
"""
Abaqus Python Script: 4x4 Hexagonal Lattice with Closed Sides
- Beam elements with circular cross-section
- Hexagon side length: 3 cm
- Beam thickness: 0.5 cm
- Material: Aluminum
- 4x4 hexagonal cell array with perimeter walls
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

# ============================================================
# PARAMETERS
# ============================================================
SIDE_LENGTH = 3.0      # Hexagon side length in cm
BEAM_THICKNESS = 0.5   # Beam circular cross-section diameter in cm
NUM_COLS = 4           # Number of hexagons horizontally
NUM_ROWS = 4           # Number of hexagons vertically

# Aluminum material properties (SI units converted to consistent units)
# Using cm-based units: Force in N, Length in cm, Time in s
# Young's Modulus: 70 GPa = 70e9 Pa = 70e5 N/cm²
YOUNGS_MODULUS = 70e5    # N/cm²
POISSONS_RATIO = 0.33
DENSITY = 2.7e-6         # kg/cm³ (2700 kg/m³ = 2.7e-6 kg/cm³)

# ============================================================
# CREATE MODEL AND PART
# ============================================================
modelName = 'HexLattice_4x4'
mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)

# Create a 2D planar wire part
partName = 'HexLattice'
mdb.models[modelName].Part(name=partName, dimensionality=TWO_D_PLANAR, 
                           type=DEFORMABLE_BODY)

# ============================================================
# DEFINE MATERIAL (ALUMINUM)
# ============================================================
matName = 'Aluminum'
mdb.models[modelName].Material(name=matName)
mdb.models[modelName].materials[matName].Elastic(
    table=((YOUNGS_MODULUS, POISSONS_RATIO), ))
mdb.models[modelName].materials[matName].Density(
    table=((DENSITY, ), ))

# ============================================================
# DEFINE BEAM SECTION (CIRCULAR CROSS-SECTION)
# ============================================================
sectionName = 'BeamSection'
# Use circular profile
mdb.models[modelName].CircularProfile(name='CircProf', 
                                      r=BEAM_THICKNESS/2)

mdb.models[modelName].BeamSection(name=sectionName, 
                                  material=matName,
                                  integration=BEFORE_ANALYSIS,
                                  profile='CircProf',
                                  poissonRatio=POISSONS_RATIO)

# ============================================================
# CREATE HEXAGONAL LATTICE GEOMETRY (HONEYCOMB TILING)
# ============================================================
p = mdb.models[modelName].parts[partName]

# Hexagon geometry for POINTY-TOP orientation (vertices at top/bottom)
# For regular hexagons with side length 'a' to share edges:
# - Width (flat-to-flat): a * sqrt(3)
# - Height (vertex-to-vertex): 2 * a
# - Horizontal spacing between centers: a * sqrt(3)  (flat-to-flat width)
# - Vertical spacing between row centers: 1.5 * a
# - Odd rows offset horizontally by: (a * sqrt(3)) / 2

hex_width = SIDE_LENGTH * math.sqrt(3)      # Flat-to-flat width
hex_height = 2 * SIDE_LENGTH                 # Vertex-to-vertex height

# Spacing for honeycomb (edge-sharing) pattern
h_spacing = hex_width                        # Horizontal: flat-to-flat
v_spacing = 1.5 * SIDE_LENGTH                # Vertical: 3/2 * side

# Calculate vertices for a single hexagon (pointy-top orientation)
# Vertices at 30°, 90°, 150°, 210°, 270°, 330° from center (pointy at top/bottom)
hex_vertices_local = []
for i in range(6):
    angle_deg = 30 + 60 * i  # Start at 30° for pointy-top
    angle_rad = math.radians(angle_deg)
    x = SIDE_LENGTH * math.cos(angle_rad)
    y = SIDE_LENGTH * math.sin(angle_rad)
    hex_vertices_local.append((x, y))

# Create a sketch to draw all hexagons
s = mdb.models[modelName].ConstrainedSketch(name='__profile__', 
                                            sheetSize=200.0)

# Function to add hexagon to sketch at a given center position
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

# Create 4x4 hexagonal array (honeycomb pattern - each hexagon shares edges with 6 neighbors)
# Store hexagon centers for boundary calculation
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
        # Add the hexagon to sketch
        addHexagonToSketch(centerX, centerY)

# Calculate boundary box that touches outermost hexagon vertices
# For pointy-top hexagons:
# - Leftmost/rightmost vertices are at 30°, 150°, 210°, 330°
# - Horizontal extent from center: SIDE_LENGTH * cos(30°) = SIDE_LENGTH * sqrt(3)/2
# - Top/bottom vertices are at 90°, 270°
# - Vertical extent from center: SIDE_LENGTH

horiz_extent = SIDE_LENGTH * math.sqrt(3) / 2  # Horizontal distance from center to vertex
vert_extent = SIDE_LENGTH  # Vertical distance from center to vertex

minX = min(cx - horiz_extent for cx, cy in hexCenters)  # Leftmost vertex
maxX = max(cx + horiz_extent for cx, cy in hexCenters)  # Rightmost vertex
minY = min(cy - vert_extent for cx, cy in hexCenters)   # Bottom vertex
maxY = max(cy + vert_extent for cx, cy in hexCenters)   # Top vertex

# ============================================================
# CREATE PERIMETER BOUNDARY WALLS (CLOSED SIDES)
# ============================================================
# Add boundary walls to the sketch - touching the hexagon vertices
# Bottom wall (connects to bottom vertices of row 0)
s.Line(point1=(minX, minY),
       point2=(maxX, minY))

# Top wall (connects to top vertices of last row)
s.Line(point1=(minX, maxY),
       point2=(maxX, maxY))

# Left wall (connects to leftmost vertices)
s.Line(point1=(minX, minY),
       point2=(minX, maxY))

# Right wall (connects to rightmost vertices)
s.Line(point1=(maxX, minY),
       point2=(maxX, maxY))

# Use the sketch to create wire geometry on the part
p.BaseWire(sketch=s)

# ============================================================
# ASSIGN BEAM SECTION TO ALL EDGES
# ============================================================
# Get all edges and assign the beam section
allEdges = p.edges
region = regionToolset.Region(edges=allEdges)
p.SectionAssignment(region=region, sectionName=sectionName, 
                    offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
                    thicknessAssignment=FROM_SECTION)

# ============================================================
# SEED EDGES FOR MESHING
# ============================================================
# Seed all edges with appropriate element size
elemSize = SIDE_LENGTH / 3  # Approximately 3 elements per hexagon side
p.seedEdgeBySize(edges=allEdges, size=elemSize, constraint=FINER)

# ============================================================
# CREATE ASSEMBLY
# ============================================================
a = mdb.models[modelName].rootAssembly
a.DatumCsysByDefault(CARTESIAN)

# Create instance of the part
instanceName = partName + '-1'
a.Instance(name=instanceName, part=p, dependent=ON)

# ============================================================
# CREATE STEP
# ============================================================
stepName = 'Step-1'
mdb.models[modelName].StaticStep(name=stepName, previous='Initial',
                                  nlgeom=OFF, timePeriod=1.0)

# ============================================================
# BOUNDARY CONDITIONS (FIXED BOTTOM EDGE)
# ============================================================
# Apply fixed BC on all edges at the bottom boundary
instance = a.instances[instanceName]
edges = instance.edges

# Find bottom edge by Y coordinate (boundary wall is at bottomY)
bottomY = minY
topY = maxY

bottomEdges = []
topEdges = []

for i, edge in enumerate(edges):
    # Get edge endpoints to determine position
    # Use query tool for edge information
    try:
        # Try to get edge midpoint
        pt1 = edge.getVertices()[0]
        pt2 = edge.getVertices()[1]
        # Get vertex coordinates from part
        y1 = p.vertices[pt1.index].point[1]
        y2 = p.vertices[pt2.index].point[1]
        avgY = (y1 + y2) / 2.0
        
        if abs(avgY - bottomY) < 0.5:
            bottomEdges.append(edge)
        elif abs(avgY - topY) < 0.5:
            topEdges.append(edge)
    except:
        pass

# Apply fixed BC on bottom edge
if bottomEdges:
    bottomRegion = regionToolset.Region(edges=bottomEdges)
    mdb.models[modelName].EncastreBC(name='BC-FixedBottom',
                                      createStepName=stepName,
                                      region=bottomRegion)

# ============================================================
# APPLY LOAD (OPTIONAL - VERTICAL PRESSURE ON TOP)
# ============================================================
# Apply load on top edge
if topEdges:
    topRegion = regionToolset.Region(edges=topEdges)
    mdb.models[modelName].ConcentratedForce(name='Load-Top',
                                            createStepName=stepName,
                                            region=topRegion,
                                            cf1=0.0, cf2=-100.0,
                                            distributionType=UNIFORM,
                                            field='', localCsys=None)

# ============================================================
# CREATE MESH
# ============================================================
# Assign beam element type
elemType = mesh.ElemType(elemCode=B21, elemLibrary=STANDARD)  # 2-node linear beam
p.setElementType(regions=region, elemTypes=(elemType,))

# Generate mesh
p.generateMesh()

# ============================================================
# CREATE JOB
# ============================================================
jobName = 'HexLattice_4x4_Job'
mdb.Job(name=jobName, model=modelName, description='4x4 Hexagonal Lattice Analysis',
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1)

# ============================================================
# SAVE MODEL
# ============================================================
mdb.saveAs(pathName='C:/Users/Eslam/Documents/355 Ansys/HexLattice_4x4')

print("=" * 60)
print("Hexagonal Lattice 4x4 Model Created Successfully!")
print("=" * 60)
print(f"Model Name: {modelName}")
print(f"Part Name: {partName}")
print(f"Number of Hexagons: {NUM_COLS} x {NUM_ROWS} = {NUM_COLS * NUM_ROWS}")
print(f"Hexagon Side Length: {SIDE_LENGTH} cm")
print(f"Beam Diameter: {BEAM_THICKNESS} cm")
print(f"Material: Aluminum (E = {YOUNGS_MODULUS/1e5:.1f} GPa)")
print(f"Job Name: {jobName}")
print("=" * 60)
print("\nTo run the analysis:")
print("  1. Open the model in Abaqus/CAE")
print("  2. Review/modify boundary conditions and loads as needed")
print("  3. Submit job: mdb.jobs['" + jobName + "'].submit()")
print("=" * 60)
