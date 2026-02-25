# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
import odbAccess

# Parameters extracted from reference model
WIDTH_SPACING = 0.01
HEIGHT_SPACING = 0.01
NUM_COLS = 8
NUM_ROWS = 4

# Model Initialization
modelName = 'LatticeModel'
if modelName in mdb.models:
    del mdb.models[modelName]
mdb.Model(name=modelName)
model = mdb.models[modelName]

# Part Creation (Building via Sketch)
s = model.ConstrainedSketch(name='UnitCell', sheetSize=1.0)

# Define a single unit cell (Re-entrant Honeycomb)
# Coordinates relative to cell center (0, 0)
# Height = 0.01 (9.99 to 10.00), Width = 0.01 (-0.005 to 0.005)
dx = 0.0025
dy = 0.005
dtip = 0.005

# Define a single unit cell (Re-entrant Honeycomb)
# Both top and bottom are single segments to match 16-node count
v_top_l = (-dx, 10.0)
v_top_r = (dx, 10.0)
v_bot_l = (-dx, 9.99)
v_bot_r = (dx, 9.99)
v_tip_l = (-dtip, 9.995)
v_tip_r = (dtip, 9.995)

# Lines
s.Line(point1=v_top_l, point2=v_top_r) # Top
s.Line(point1=v_bot_l, point2=v_bot_r) # Bottom
s.Line(point1=v_tip_l, point2=v_top_l) # Left V1
s.Line(point1=v_tip_l, point2=v_bot_l) # Left V2
s.Line(point1=v_tip_r, point2=v_top_r) # Right V1
s.Line(point1=v_tip_r, point2=v_bot_r) # Right V2

# Part
p = model.Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=DEFORMABLE_BODY)
p.BaseWire(sketch=s)

# Pattern the geometry
p.projectReferencesOntoSketch(filter=COPLANAR_EDGES, 
    sketch=model.ConstrainedSketch(name='__edit__', objectToCopy=p.features['Wire-1'].sketch), 
    upToFeature=p.features['Wire-1'])
s_edit = model.sketches['__edit__']
s_edit.linearPattern(angle1=0.0, angle2=90.0, 
    geomList=s_edit.geometry.values(), 
    number1=NUM_COLS, number2=NUM_ROWS, 
    spacing1=WIDTH_SPACING, spacing2=HEIGHT_SPACING)
p.features['Wire-1'].setValues(sketch=s_edit)
del s_edit
p.regenerate()

# Material and Section
mat = model.Material(name='Steel')
mat.Elastic(table=((200e9, 0.3), ))
model.CircularProfile(name='BeamProfile', r=0.001)
model.BeamSection(consistentMassMatrix=False, integration=DURING_ANALYSIS, 
    material='Steel', name='BeamSection', profile='BeamProfile')

# Section Assignment
p.SectionAssignment(region=p.Set(edges=p.edges, name='AllEdges'), sectionName='BeamSection')
p.assignBeamSectionOrientation(method=N1_COSINES, n1=(0.0, 0.0, -1.0), region=p.sets['AllEdges'])

# Assembly
a = model.rootAssembly
inst = a.Instance(dependent=ON, name='Part-1-1', part=p)

# Step
model.StaticStep(name='Step-1', previous='Initial')

# Mesh
a.makeIndependent(instances=(inst, ))
a.setElementType(elemTypes=(ElemType(elemCode=B21, elemLibrary=STANDARD), ), 
    regions=(inst.edges, ))
a.seedPartInstance(regions=(inst, ), size=1.0) # 1 element per segment
a.generateMesh(regions=(inst, ))

# Debug file
debugFile = open('debug.txt', 'w')
debugFile.write('Total Nodes in Assembly: %d\n' % len(inst.nodes))

# Boundary Conditions (Bottom Row Support)
eps = 0.0001
bottom_nodes = inst.nodes.getByBoundingBox(xMin=-1.0, xMax=1.0, yMin=9.99-eps, yMax=9.99+eps)
debugFile.write('Found %d support nodes at Y=9.99\n' % len(bottom_nodes))
if len(bottom_nodes) > 0:
    a.Set(nodes=bottom_nodes, name='SupportNodes')
    model.DisplacementBC(createStepName='Step-1', name='FixedSupport', 
        region=a.sets['SupportNodes'], u1=0.0, u2=0.0, ur3=0.0)

# Loads (Top Row Load)
top_nodes = inst.nodes.getByBoundingBox(xMin=-1.0, xMax=1.0, yMin=10.03-eps, yMax=10.03+eps)
debugFile.write('Found %d load nodes at Y=10.03\n' % len(top_nodes))
if len(top_nodes) > 0:
    a.Set(nodes=top_nodes, name='LoadNodes')
    model.ConcentratedForce(cf2=-3200.0, createStepName='Step-1', 
        name='VerticalLoad', region=a.sets['LoadNodes'])

debugFile.close()

# Job
jobName = 'LatticeJob'
if jobName in mdb.jobs:
    del mdb.jobs[jobName]
mdb.Job(model=modelName, name=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()

# Post-Processing
odb = odbAccess.openOdb(jobName + '.odb')
frame = odb.steps['Step-1'].frames[-1]
stress = frame.fieldOutputs['S']

max_mises = 0.0
max_val = None

for v in stress.values:
    if v.mises > max_mises:
        max_mises = v.mises
        max_val = v

with open('results.txt', 'w') as f:
    f.write('Abaqus Lattice Simulation Results\n')
    f.write('=================================\n\n')
    if max_val:
        f.write('Maximum Von Mises Stress: %e Pa\n' % max_mises)
        f.write('Element ID: %d\n' % max_val.elementLabel)
        
        # Get location
        inst_res = odb.rootAssembly.instances[max_val.instance.name]
        elem = inst_res.elements[max_val.elementLabel-1]
        node = inst_res.nodes[elem.connectivity[0]-1]
        f.write('Approx. Location (X, Y): (%f, %f)\n' % (node.coordinates[0], node.coordinates[1]))
    else:
        f.write('No stress results found.\n')

odb.close()
print('Simulation complete. Results in results.txt')
