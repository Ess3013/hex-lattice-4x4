# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-10.0, 10.0), 
    point2=(0.0, 10.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[2])
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -9.68338775634766, 20.5971183776855), value=0.0025, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1])
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, 10.0), point2=(
    0.00470569357275963, 10.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[3])
mdb.models['Model-1'].sketches['__profile__'].ParallelConstraint(addUndoState=
    False, entity1=mdb.models['Model-1'].sketches['__profile__'].geometry[2], 
    entity2=mdb.models['Model-1'].sketches['__profile__'].geometry[3])
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    0.00260110385715961, 10.0042190551758), value=0.0025, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[1], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[2])
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    sheetAuto=OFF, sheetSize=50.0)
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(gridAuto=
    OFF, gridSpacing=10.0)
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    sheetSize=500.0)
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    gridSpacing=1.0)
mdb.models['Model-1'].sketches['__profile__'].sketchOptions.setValues(
    sheetSize=50.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-0.0025, 10.0), 
    point2=(-0.0025, 9.99070358276367))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[4])
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[2], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[4])
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    -0.00680125784128904, 9.99757385253906), value=0.01, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[3])
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025, 10.0), 
    point2=(0.0025, 9.99022102355957))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[5])
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[3], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[5])
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-0.0025, 9.99), 
    point2=(0.0042437706142664, 9.99))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[4], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[5], ))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025, 10.0), 
    point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[3], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[6], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[6])
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[6], ))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-0.0025, 9.99), 
    point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[8])
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[4], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[8])
mdb.models['Model-1'].sketches['__profile__'].Spot(point=(-0.0025, 9.995))
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[7], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[4])
mdb.models['Model-1'].sketches['__profile__'].EqualDistanceConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[0], entity2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[3], midpoint=
    mdb.models['Model-1'].sketches['__profile__'].vertices[7])
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-0.0025, 10.0), 
    point2=(-0.00672508496791124, 9.99496269226074))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(
    -0.00672508496791124, 9.99496269226074), point2=(-0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(
    -0.00647402537500365, 9.9946678031619), point2=(0.00701137632131577, 
    9.9946678031619))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[11])
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[9], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[10])
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(
    -0.00672508496791124, 9.99496269226074), point2=(0.0053101871162653, 
    9.99496269226074))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[11])
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025, 10.0), 
    point2=(0.0053101871162653, 9.99496269226074))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0053101871162653, 
    9.99496269226074), point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].HorizontalDimension(textPoint=(
    -0.00362739921547472, 10.0015287399292), value=0.002, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[8], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[7])
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[12], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[13]))
mdb.models['Model-1'].sketches['__profile__'].Spot(point=(0.0025, 
    9.99496269226074))
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[10], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[7])
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[7], ))
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[11], ))
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].vertices[10], ))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025171919260174, 
    9.99792861938477), point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025, 10.0), 
    point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=mdb.models['Model-1'].sketches['__profile__'].geometry[14])
mdb.models['Model-1'].sketches['__profile__'].PerpendicularConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[3], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[14])
mdb.models['Model-1'].sketches['__profile__'].Spot(point=(0.0025, 9.995))
mdb.models['Model-1'].sketches['__profile__'].CoincidentConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[11], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[14])
mdb.models['Model-1'].sketches['__profile__'].EqualDistanceConstraint(
    addUndoState=False, entity1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[2], entity2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[6], midpoint=
    mdb.models['Model-1'].sketches['__profile__'].vertices[11])
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025, 10.0), 
    point2=(0.0040914248675108, 9.99501323699951))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0040914248675108, 
    9.99501323699951), point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].ObliqueDimension(textPoint=(
    0.0041675977408886, 10.0031766891479), value=0.002, vertex1=
    mdb.models['Model-1'].sketches['__profile__'].vertices[11], vertex2=
    mdb.models['Model-1'].sketches['__profile__'].vertices[12])
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0025, 10.0), 
    point2=(0.0045992424711585, 9.99496269226074))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0045992424711585, 
    9.99496269226074), point2=(0.0025, 9.99))
mdb.models['Model-1'].sketches['__profile__'].EqualLengthConstraint(entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[9], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[15])
mdb.models['Model-1'].sketches['__profile__'].EqualLengthConstraint(entity1=
    mdb.models['Model-1'].sketches['__profile__'].geometry[10], entity2=
    mdb.models['Model-1'].sketches['__profile__'].geometry[16])
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[4], ))
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[14], ))
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].vertices[7], ))
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].vertices[11], ))
mdb.models['Model-1'].sketches['__profile__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__profile__'].geometry[2], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[3], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[8], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[9], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[10], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[15], 
    mdb.models['Model-1'].sketches['__profile__'].geometry[16], 
    mdb.models['Model-1'].sketches['__profile__'].dimensions[2], 
    mdb.models['Model-1'].sketches['__profile__'].constraints[4], 
    mdb.models['Model-1'].sketches['__profile__'].constraints[7], 
    mdb.models['Model-1'].sketches['__profile__'].constraints[8], 
    mdb.models['Model-1'].sketches['__profile__'].constraints[28], 
    mdb.models['Model-1'].sketches['__profile__'].constraints[54], 
    mdb.models['Model-1'].sketches['__profile__'].constraints[55]))
mdb.models['Model-1'].sketches['__profile__'].undo()
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseWire(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=
    mdb.models['Model-1'].parts['Part-1'].features['Wire-1'].sketch)
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__edit__'], 
    upToFeature=mdb.models['Model-1'].parts['Part-1'].features['Wire-1'])
mdb.models['Model-1'].sketches['__edit__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__edit__'].dimensions[1], ))
mdb.models['Model-1'].sketches['__edit__'].delete(objectList=(
    mdb.models['Model-1'].sketches['__edit__'].dimensions[0], ))
mdb.models['Model-1'].sketches['__edit__'].ObliqueDimension(textPoint=(
    -0.0013471667189151, 10.0019941329956), value=0.0025, vertex1=
    mdb.models['Model-1'].sketches['__edit__'].vertices[0], vertex2=
    mdb.models['Model-1'].sketches['__edit__'].vertices[1])
mdb.models['Model-1'].sketches['__edit__'].ObliqueDimension(textPoint=(
    0.00102444994263351, 10.0015630722046), value=0.0025, vertex1=
    mdb.models['Model-1'].sketches['__edit__'].vertices[1], vertex2=
    mdb.models['Model-1'].sketches['__edit__'].vertices[2])
mdb.models['Model-1'].sketches['__edit__'].HorizontalDimension(textPoint=(
    0.00241046003066003, 10.0027627944946), value=0.01, vertex1=
    mdb.models['Model-1'].sketches['__edit__'].vertices[8], vertex2=
    mdb.models['Model-1'].sketches['__edit__'].vertices[12])
mdb.models['Model-1'].sketches['__edit__'].linearPattern(angle1=0.0, angle2=
    90.0, geomList=(mdb.models['Model-1'].sketches['__edit__'].geometry[2], 
    mdb.models['Model-1'].sketches['__edit__'].geometry[3], 
    mdb.models['Model-1'].sketches['__edit__'].geometry[8], 
    mdb.models['Model-1'].sketches['__edit__'].geometry[9], 
    mdb.models['Model-1'].sketches['__edit__'].geometry[10], 
    mdb.models['Model-1'].sketches['__edit__'].geometry[15], 
    mdb.models['Model-1'].sketches['__edit__'].geometry[16]), number1=8, 
    number2=4, spacing1=0.01, spacing2=0.01, vertexList=())
mdb.models['Model-1'].parts['Part-1'].features['Wire-1'].setValues(sketch=
    mdb.models['Model-1'].sketches['__edit__'])
del mdb.models['Model-1'].sketches['__edit__']
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=
    mdb.models['Model-1'].parts['Part-1'].features['Wire-1'].sketch)
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__edit__'], 
    upToFeature=mdb.models['Model-1'].parts['Part-1'].features['Wire-1'])
del mdb.models['Model-1'].sketches['__edit__']
mdb.models['Model-1'].parts['Part-1'].regenerate()
# Save by AC3 on 2026_02_22-01.15.31; build Unofficial Packaging Version 2022_09_28-20.11.55 183150
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
mdb.models['Model-1'].Material(name='steel')
mdb.models['Model-1'].materials['steel'].Elastic(table=((200000000000.0, 0.3), 
    ))
mdb.models['Model-1'].CircularProfile(name='Profile-1', r=0.001)
mdb.models['Model-1'].BeamSection(consistentMassMatrix=False, integration=
    DURING_ANALYSIS, material='steel', name='Beam section', poissonRatio=0.0, 
    profile='Profile-1', temperatureVar=LINEAR)
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges.getSequenceFromMask((
    '[#ffffffff:6 #ff ]', ), ), name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
    'Beam section', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges.getSequenceFromMask((
    '[#ffffffff:6 #ff ]', ), ), name='Set-2')
mdb.models['Model-1'].parts['Part-1'].assignBeamSectionOrientation(method=
    N1_COSINES, n1=(0.0, 0.0, -1.0), region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-2'])
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-2', 
    part=mdb.models['Model-1'].parts['Part-1'])
del mdb.models['Model-1'].rootAssembly.features['Part-1-2']
del mdb.models['Model-1'].rootAssembly.features['Part-1-1']
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
    ('[#0 #4000408 #10000080 #200000 #4000 #80 ]', ), ), name='Set-1')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=0.0, 
    u2=UNSET, ur3=0.0)
mdb.models['Model-1'].rootAssembly.Set(name='Set-2', vertices=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].vertices.getSequenceFromMask(
    ('[#420a00 #4000 #140008 #1400050 #50500 ]', ), ))
mdb.models['Model-1'].ConcentratedForce(cf2=-3200.0, createStepName='Step-1', 
    distributionType=UNIFORM, field='', localCsys=None, name='Load-1', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-2'])
mdb.models['Model-1'].rootAssembly.makeIndependent(instances=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=B21, elemLibrary=STANDARD), ), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getSequenceFromMask(
    ('[#ffffffff:6 #ff ]', ), ), ))
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=5.0)
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=2.0)
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=10.0)
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=5.0)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, numThreadsPerMpiProcess=1, queue=None, resultsFormat=
    ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, 
    waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1']._Message(STARTED, {'phase': BATCHPRE_PHASE, 
    'clientHost': 'DESKTOP-SFFMJE4', 'handle': 0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': BATCHPRE_PHASE, 
    'message': 'For 112 beam elements either the average curvature about the local 1-direction differs by more than 0.1 degrees per unit length as compared to the default curvature or the approximate integrated curvature for the entire beam differs by more than 5 degrees as compared to the approximate integrated default curvature. This may be due to a user-specified normal or due to the nodal averaging routine used by Abaqus. This difference may cause unexpected behavior of the beam and you may want to verify that the beam normals are correct for your problem. The elements have been identified in element set WarnBeamCurvature1.', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FILE, {'phase': BATCHPRE_PHASE, 
    'file': 'C:\\temp\\Job-1.odb', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(COMPLETED, {'phase': BATCHPRE_PHASE, 
    'message': 'Analysis phase complete', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STARTED, {'phase': STANDARD_PHASE, 
    'clientHost': 'DESKTOP-SFFMJE4', 'handle': 6432, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STEP, {'phase': STANDARD_PHASE, 'stepId': 1, 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FRAME, {'phase': STANDARD_PHASE, 'step': 0, 
    'frame': 0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(MEMORY_ESTIMATE, {'phase': STANDARD_PHASE, 
    'jobName': 'Job-1', 'memory': 24.0})
mdb.jobs['Job-1']._Message(PHYSICAL_MEMORY, {'phase': STANDARD_PHASE, 
    'physical_memory': 8104.0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(MINIMUM_MEMORY, {'minimum_memory': 17.0, 
    'phase': STANDARD_PHASE, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 0.0, 'attempts': ' 1U', 
    'timeIncrement': 1.0, 'increment': 1, 'stepTime': 0.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 4, 'phase': STANDARD_PHASE, 
    'equilibrium': 4})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 0.0, 'attempts': ' 2U', 
    'timeIncrement': 0.25, 'increment': 1, 'stepTime': 0.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 4, 'phase': STANDARD_PHASE, 
    'equilibrium': 4})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 0.0, 'attempts': ' 3U', 
    'timeIncrement': 0.0625, 'increment': 1, 'stepTime': 0.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 4, 'phase': STANDARD_PHASE, 
    'equilibrium': 4})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 0.0, 'attempts': ' 4U', 
    'timeIncrement': 0.015625, 'increment': 1, 'stepTime': 0.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 4, 'phase': STANDARD_PHASE, 
    'equilibrium': 4})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': STANDARD_PHASE, 
    'message': 'Solver problem. Numerical singularity when processing node PART-1-1.63 D.O.F. 2 ratio = 602.655E+12  .', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 0.0, 'attempts': ' 5U', 
    'timeIncrement': 0.00390625, 'increment': 1, 'stepTime': 0.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 4, 'phase': STANDARD_PHASE, 
    'equilibrium': 4})
mdb.jobs['Job-1']._Message(ERROR, {'phase': STANDARD_PHASE, 
    'message': 'Too many attempts made for this increment', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ABORTED, {'phase': STANDARD_PHASE, 
    'message': 'Analysis phase failed due to errors', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ERROR, {
    'message': 'Abaqus/Standard Analysis exited with an error - Please see the  message file for possible error messages if the file exists.', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(JOB_ABORTED, {
    'message': 'Abaqus/Standard Analysis exited with an error - Please see the  message file for possible error messages if the file exists.', 
    'jobName': 'Job-1'})
mdb.models['Model-1'].boundaryConditions['BC-1'].setValues(u2=0.0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1']._Message(STARTED, {'phase': BATCHPRE_PHASE, 
    'clientHost': 'DESKTOP-SFFMJE4', 'handle': 0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(WARNING, {'phase': BATCHPRE_PHASE, 
    'message': 'For 112 beam elements either the average curvature about the local 1-direction differs by more than 0.1 degrees per unit length as compared to the default curvature or the approximate integrated curvature for the entire beam differs by more than 5 degrees as compared to the approximate integrated default curvature. This may be due to a user-specified normal or due to the nodal averaging routine used by Abaqus. This difference may cause unexpected behavior of the beam and you may want to verify that the beam normals are correct for your problem. The elements have been identified in element set WarnBeamCurvature1.', 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FILE, {'phase': BATCHPRE_PHASE, 
    'file': 'C:\\temp\\Job-1.odb', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(COMPLETED, {'phase': BATCHPRE_PHASE, 
    'message': 'Analysis phase complete', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STARTED, {'phase': STANDARD_PHASE, 
    'clientHost': 'DESKTOP-SFFMJE4', 'handle': 7600, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STEP, {'phase': STANDARD_PHASE, 'stepId': 1, 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FRAME, {'phase': STANDARD_PHASE, 'step': 0, 
    'frame': 0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(MEMORY_ESTIMATE, {'phase': STANDARD_PHASE, 
    'jobName': 'Job-1', 'memory': 24.0})
mdb.jobs['Job-1']._Message(PHYSICAL_MEMORY, {'phase': STANDARD_PHASE, 
    'physical_memory': 8104.0, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(MINIMUM_MEMORY, {'minimum_memory': 17.0, 
    'phase': STANDARD_PHASE, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(ODB_FRAME, {'phase': STANDARD_PHASE, 'step': 0, 
    'frame': 1, 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(STATUS, {'totalTime': 1.0, 'attempts': 1, 
    'timeIncrement': 1.0, 'increment': 1, 'stepTime': 1.0, 'step': 1, 
    'jobName': 'Job-1', 'severe': 0, 'iterations': 1, 'phase': STANDARD_PHASE, 
    'equilibrium': 1})
mdb.jobs['Job-1']._Message(END_STEP, {'phase': STANDARD_PHASE, 'stepId': 1, 
    'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(COMPLETED, {'phase': STANDARD_PHASE, 
    'message': 'Analysis phase complete', 'jobName': 'Job-1'})
mdb.jobs['Job-1']._Message(JOB_COMPLETED, {'time': 'Sun Feb 22 01:28:39 2026', 
    'jobName': 'Job-1'})
# Save by AC3 on 2026_02_22-01.29.11; build Unofficial Packaging Version 2022_09_28-20.11.55 183150
# Save by AC3 on 2026_02_22-01.29.57; build Unofficial Packaging Version 2022_09_28-20.11.55 183150
