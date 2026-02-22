# -*- coding: utf-8 -*-
"""
Parametric Sweep Script for Honeycomb Lattice Connecting Rod
MENG3505_Project01 Implementation

Sweeps design variables:
- Slenderness ratio beta: 1/20 <= beta <= 1/5
- Configuration angle theta: 10° <= theta <= 30°

Generates models, submits jobs, and collects results.
"""

from abaqus import *
from abaqusConstants import *
import os
import sys
import math
import json
import part
import material
import section
import assembly
import step
import load
import mesh
import job
import sketch
import regionToolset
import mdb

# ============================================================
# SWEEP PARAMETERS
# ============================================================

# Slenderness ratio sweep: 1/20 <= beta <= 1/5
BETA_VALUES = [1.0/20, 1.0/15, 1.0/12, 1.0/10, 1.0/8, 1.0/6, 1.0/5]

# Configuration angle sweep: 10° <= theta <= 30°
THETA_VALUES = [0, 10, 15, 20, 25, 30]  # Include 0 as baseline

# Fixed parameters
L = 0.3                    # Beam length in cm
NUM_COLS = 20              # Number of cells horizontally
NUM_ROWS = 10              # Number of cells vertically
YOUNGS_MODULUS = 70e5      # N/cm²
POISSONS_RATIO = 0.33
DENSITY = 2.7e-6           # kg/cm³
YIELD_STRESS = 276e3       # N/cm²
STATIC_LOAD = 10000.0      # N
DYNAMIC_LOAD_AMPLITUDE = 10000.0  # N
FREQ_MIN = 0.0             # Hz
FREQ_MAX = 1000.0          # Hz
ELEM_PER_BEAM = 3          # Elements per beam

# Results storage
resultsFile = os.path.join(os.path.dirname(__file__), 'parametric_results.json')
allResults = {}

# ============================================================
# MODEL GENERATION FUNCTION
# ============================================================
def createModel(beta, theta):
    """Create a honeycomb lattice model with given parameters"""
    
    # Calculate derived parameters
    h = L * beta  # Beam height
    
    # Model name based on parameters
    betaStr = f"{beta:.4f}".replace('.', '_')
    thetaStr = f"{theta:.0f}"
    modelName = f'HoneycombRod_b{betaStr}_t{thetaStr}'
    
    # Check if model already exists
    if modelName in mdb.models:
        del mdb.models[modelName]
    
    # Create new model
    mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)
    
    # Create part
    partName = 'HoneycombLattice'
    mdb.models[modelName].Part(name=partName, dimensionality=TWO_D_PLANAR,
                               type=DEFORMABLE_BODY)
    p = mdb.models[modelName].parts[partName]
    
    # Define material
    matName = 'Aluminum_B4C'
    mdb.models[modelName].Material(name=matName)
    mdb.models[modelName].materials[matName].Elastic(
        table=((YOUNGS_MODULUS, POISSONS_RATIO), ))
    mdb.models[modelName].materials[matName].Density(
        table=((DENSITY, ), ))
    mdb.models[modelName].materials[matName].Plastic(
        table=((YIELD_STRESS, 0.0), ))
    
    # Define beam section
    sectionName = 'BeamSection'
    profileName = f'CircProf_b{betaStr}'
    mdb.models[modelName].CircularProfile(name=profileName, r=h/2)
    mdb.models[modelName].BeamSection(name=sectionName,
                                      material=matName,
                                      integration=BEFORE_ANALYSIS,
                                      profile=profileName,
                                      poissonRatio=POISSONS_RATIO)
    
    # Hexagon geometry
    hex_width = L * math.sqrt(3)
    h_spacing = hex_width
    v_spacing = 1.5 * L
    
    # Calculate vertices with rotation for theta
    hex_vertices_local = []
    for i in range(6):
        base_angle_deg = 30 + 60 * i
        base_angle_rad = math.radians(base_angle_deg)
        
        if theta != 0:
            theta_rad = math.radians(theta)
            x_local = L * math.cos(base_angle_rad)
            y_local = L * math.sin(base_angle_rad)
            x_rot = x_local * math.cos(theta_rad) - y_local * math.sin(theta_rad)
            y_rot = x_local * math.sin(theta_rad) + y_local * math.cos(theta_rad)
            hex_vertices_local.append((x_rot, y_rot))
        else:
            x = L * math.cos(base_angle_rad)
            y = L * math.sin(base_angle_rad)
            hex_vertices_local.append((x, y))
    
    # Create sketch
    s = mdb.models[modelName].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    
    def addHexagonToSketch(centerX, centerY):
        coords = []
        for vx, vy in hex_vertices_local:
            coords.append((centerX + vx, centerY + vy))
        for i in range(6):
            s.Line(point1=coords[i], point2=coords[(i + 1) % 6])
    
    # Create hexagonal array
    hexCenters = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            centerX = col * h_spacing
            centerY = row * v_spacing
            if row % 2 == 1:
                centerX += h_spacing / 2
            hexCenters.append((centerX, centerY))
            addHexagonToSketch(centerX, centerY)
    
    # Calculate boundary box
    all_vertices = []
    for cx, cy in hexCenters:
        for vx, vy in hex_vertices_local:
            all_vertices.append((cx + vx, cy + vy))
    
    minX = min(v[0] for v in all_vertices)
    maxX = max(v[0] for v in all_vertices)
    minY = min(v[1] for v in all_vertices)
    maxY = max(v[1] for v in all_vertices)
    
    # Create perimeter walls
    s.Line(point1=(minX, minY), point2=(maxX, minY))
    s.Line(point1=(minX, maxY), point2=(maxX, maxY))
    s.Line(point1=(minX, minY), point2=(minX, maxY))
    s.Line(point1=(maxX, minY), point2=(maxX, maxY))
    
    # Create wire geometry
    p.BaseWire(sketch=s)
    
    # Assign section
    allEdges = p.edges
    region = regionToolset.Region(edges=allEdges)
    p.SectionAssignment(region=region, sectionName=sectionName,
                        offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE,
                        thicknessAssignment=FROM_SECTION)
    
    # Seed edges
    elemSize = L / ELEM_PER_BEAM
    p.seedEdgeBySize(edges=allEdges, size=elemSize, constraint=FINER)
    
    # Create assembly
    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    instanceName = partName + '-1'
    a.Instance(name=instanceName, part=p, dependent=ON)
    
    # Create steps
    stepName_Static = 'Step-Static'
    mdb.models[modelName].StaticStep(name=stepName_Static, previous='Initial',
                                      nlgeom=OFF, timePeriod=1.0)
    
    stepName_Buckling = 'Step-Buckling'
    mdb.models[modelName].BuckleStep(name=stepName_Buckling, previous=stepName_Static,
                                      numEigenvalues=10)
    
    stepName_Freq = 'Step-Frequency'
    mdb.models[modelName].FrequencyStep(name=stepName_Freq, previous='Initial',
                                         numEigenvalues=50, normalization=MASS)
    
    stepName_SSD = 'Step-SSD'
    mdb.models[modelName].SteadyStateDynamicsStep(
        name=stepName_SSD, previous=stepName_Freq,
        frequencyScaleFactor=1.0, numIntervals=100,
        freqMin=FREQ_MIN, freqMax=FREQ_MAX,
        scaling=UNIFORM, damping=0.02)
    
    # Boundary conditions
    instance = a.instances[instanceName]
    edges = instance.edges
    
    bottomEdges = []
    topEdges = []
    
    for edge in edges:
        try:
            verts = edge.getVertices()
            if len(verts) >= 2:
                y1 = p.vertices[verts[0].index].point[1]
                y2 = p.vertices[verts[1].index].point[1]
                avgY = (y1 + y2) / 2.0
                if abs(avgY - minY) < 0.1:
                    bottomEdges.append(edge)
                if abs(avgY - maxY) < 0.1:
                    topEdges.append(edge)
        except:
            pass
    
    if bottomEdges:
        bottomRegion = regionToolset.Region(edges=bottomEdges)
        mdb.models[modelName].EncastreBC(name='BC-FixedBottom',
                                          createStepName=stepName_Static,
                                          region=bottomRegion)
    
    # Loads
    if topEdges:
        topRegion = regionToolset.Region(edges=topEdges)
        mdb.models[modelName].ConcentratedForce(name='Load-Static',
                                                createStepName=stepName_Static,
                                                region=topRegion,
                                                cf1=0.0, cf2=-STATIC_LOAD,
                                                distributionType=UNIFORM)
    
    # Mesh
    elemType = mesh.ElemType(elemCode=B21, elemLibrary=STANDARD)
    p.setElementType(regions=region, elemTypes=(elemType,))
    p.generateMesh()
    
    # Field output
    mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(
        variables=('U', 'RF', 'S', 'E', 'LE', 'PE', 'PEEQ'),
        energyOutputRequested=ON)
    
    # History output
    mdb.models[modelName].HistoryOutputRequest(name='H-StrainEnergy',
                                               createStepName=stepName_SSD,
                                               variables=('ALLSE', 'ALLIE'),
                                               frequency=1)
    
    # Create job
    jobName = f'Job_b{betaStr}_t{thetaStr}'
    mdb.Job(name=jobName, model=modelName,
            description=f'beta={beta:.4f}, theta={theta}°',
            type=ANALYSIS, numCpus=4, memory=90, memoryUnits=PERCENTAGE)
    
    return modelName, jobName, beta, theta, h

# ============================================================
# RESULTS EXTRACTION FUNCTION
# ============================================================
def extractResults(odbPath, beta, theta):
    """Extract results from ODB file"""
    import visualization
    import xyPlot
    from odbAccess import openOdb
    
    results = {
        'beta': beta,
        'theta': theta,
        'odbPath': odbPath,
        'maxStress': None,
        'maxDisplacement': None,
        'bucklingLoadFactors': [],
        'naturalFrequencies': [],
        'strainEnergyFRF': [],
        'frequencies': []
    }
    
    try:
        odb = openOdb(odbPath)
        
        # Static step results
        if 'Step-Static' in odb.steps:
            step = odb.steps['Step-Static']
            if 'S' in step.frames[-1].fieldOutputs:
                stress = step.frames[-1].fieldOutputs['S']
                maxStress = max(v.mises for v in stress.values)
                results['maxStress'] = maxStress
            
            if 'U' in step.frames[-1].fieldOutputs:
                disp = step.frames[-1].fieldOutputs['U']
                maxDisp = max(v.magnitude for v in disp.values)
                results['maxDisplacement'] = maxDisp
        
        # Buckling step results
        if 'Step-Buckling' in odb.steps:
            step = odb.steps['Step-Buckling']
            for frame in step.frames:
                if frame.description:
                    try:
                        lf = frame.frameValue  # Load factor
                        results['bucklingLoadFactors'].append(lf)
                    except:
                        pass
        
        # Frequency step results
        if 'Step-Frequency' in odb.steps:
            step = odb.steps['Step-Frequency']
            for frame in step.frames:
                freq = frame.frameValue  # Frequency in Hz
                results['naturalFrequencies'].append(freq)
        
        # SSD step - Strain energy vs frequency
        if 'Step-SSD' in odb.steps:
            step = odb.steps['Step-SSD']
            if 'H-StrainEnergy' in step.historyRegions:
                histRegion = step.historyRegions['H-StrainEnergy']
                if 'ALLSE' in histRegion.historyOutputs:
                    data = histRegion.historyOutputs['ALLSE'].data
                    for time, energy in data:
                        # Time in SSD is actually frequency
                        freq = time
                        results['frequencies'].append(freq)
                        results['strainEnergyFRF'].append(energy)
        
        odb.close()
        
    except Exception as e:
        print(f"Error extracting results from {odbPath}: {str(e)}")
        results['error'] = str(e)
    
    return results

# ============================================================
# MAIN SWEEP EXECUTION
# ============================================================
def runSweep():
    """Run the complete parametric sweep"""
    
    print("=" * 70)
    print("PARAMETRIC SWEEP - HONEYCOMB LATTICE CONNECTING ROD")
    print("=" * 70)
    print(f"\nSweep Parameters:")
    print(f"  Slenderness ratios (beta): {BETA_VALUES}")
    print(f"  Configuration angles (theta): {THETA_VALUES}°")
    print(f"  Total configurations: {len(BETA_VALUES) * len(THETA_VALUES)}")
    print("=" * 70)
    
    totalConfigs = len(BETA_VALUES) * len(THETA_VALUES)
    configNum = 0
    
    for beta in BETA_VALUES:
        for theta in THETA_VALUES:
            configNum += 1
            betaStr = f"{beta:.4f}".replace('.', '_')
            thetaStr = f"{theta:.0f}"
            
            print(f"\n[{configNum}/{totalConfigs}] Processing: beta={beta:.4f}, theta={theta}°")
            print("-" * 50)
            
            # Create model
            try:
                modelName, jobName, beta, theta, h = createModel(beta, theta)
                print(f"  Model created: {modelName}")
                print(f"  Beam height: {h:.4f} cm")
                
                # Save model
                savePath = os.path.join(os.path.dirname(__file__), modelName)
                mdb.saveAs(pathName=savePath)
                print(f"  Model saved: {savePath}.cae")
                
                # Submit job
                print(f"  Submitting job: {jobName}...")
                mdb.jobs[jobName].submit()
                mdb.jobs[jobName].waitForCompletion()
                
                # Check job status
                jobStatus = mdb.jobs[jobName].status
                print(f"  Job status: {jobStatus}")
                
                if jobStatus == COMPLETED:
                    # Extract results
                    odbPath = os.path.join(os.path.dirname(__file__), f'{jobName}.odb')
                    results = extractResults(odbPath, beta, theta)

                    configKey = f"b{betaStr}_t{thetaStr}"
                    allResults[configKey] = results
                    print(f"  Results extracted successfully")

                    if results['maxStress']:
                        print(f"  Max Stress: {results['maxStress']/1e3:.2f} MPa")
                    if results['bucklingLoadFactors']:
                        print(f"  First Buckling LF: {results['bucklingLoadFactors'][0]:.4f}")
                    if results['naturalFrequencies']:
                        print(f"  First Natural Freq: {results['naturalFrequencies'][0]:.2f} Hz")
                else:
                    print(f"  Job did not complete successfully")

            except Exception as e:
                print(f"  ERROR: {str(e)}")
                configKey = f"b{betaStr}_t{thetaStr}"
                allResults[configKey] = {
                    'beta': beta,
                    'theta': theta,
                    'error': str(e)
                }
            finally:
                # Clean up: close ODB and delete model to save memory
                try:
                    import visualization
                    visualization.closeOdb()
                except:
                    pass
                # Delete model from memory if not needed
                try:
                    del mdb.models[modelName]
                except:
                    pass
    
    # Save all results to JSON
    # Convert tuples to lists for JSON serialization
    jsonResults = {}
    for key, value in allResults.items():
        jsonResults[key] = {}
        for k, v in value.items():
            if isinstance(v, tuple):
                jsonResults[key][k] = list(v)
            else:
                jsonResults[key][k] = v
    
    with open(resultsFile, 'w') as f:
        json.dump(jsonResults, f, indent=2)
    
    print("\n" + "=" * 70)
    print("PARAMETRIC SWEEP COMPLETED")
    print("=" * 70)
    print(f"Results saved to: {resultsFile}")
    print(f"Total configurations processed: {configNum}/{totalConfigs}")
    print("=" * 70)
    
    return allResults

# ============================================================
# RUN IF EXECUTED DIRECTLY
# ============================================================
if __name__ == '__main__':
    results = runSweep()
