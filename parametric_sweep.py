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

# ============================================================
# SWEEP PARAMETERS
# ============================================================

# Slenderness ratio sweep: 1/20 <= beta <= 1/5 (reduced for testing)
BETA_VALUES = [1.0/15, 1.0/10, 1.0/8, 1.0/5]

# Configuration angle sweep: 0° <= theta <= 30° (reduced for testing)
THETA_VALUES = [0, 15, 30]

# Fixed parameters - Reduced for Abaqus Learning Edition (1000 node limit)
L = 0.3                    # Beam length in cm
NUM_COLS = 5               # Number of cells horizontally (reduced from 20)
NUM_ROWS = 3               # Number of cells vertically (reduced from 10)
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
resultsFile = os.path.join(os.getcwd(), 'parametric_results.json')
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

    # Assign beam orientation (for 2D beams, use global Z-axis as normal)
    p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0, 1.0))

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

    stepName_Freq = 'Step-Frequency'
    mdb.models[modelName].FrequencyStep(name=stepName_Freq, previous='Initial',
                                         numEigen=20, normalization=MASS)
    
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

    # Field output - simplified for beam elements
    mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(
        variables=('U', 'RF', 'ENER'))

    # Create job
    jobName = f'Job_b{betaStr}_t{thetaStr}'
    mdb.Job(name=jobName, model=modelName,
            description=f'beta={beta:.4f}, theta={theta}°',
            type=ANALYSIS, memory=90, memoryUnits=PERCENTAGE)
    
    return modelName, jobName, beta, theta, h

# ============================================================
# RESULTS EXTRACTION FUNCTION
# ============================================================
def extractResults(odbPath, beta, theta):
    """Extract results from ODB file"""
    import visualization
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
        print(f"  Opening ODB: {odbPath}")
        odb = openOdb(odbPath)
        print(f"  ODB opened successfully")

        # Static step results
        if 'Step-Static' in odb.steps:
            step = odb.steps['Step-Static']
            if 'U' in step.frames[-1].fieldOutputs:
                disp = step.frames[-1].fieldOutputs['U']
                maxDisp = max(v.magnitude for v in disp.values)
                results['maxDisplacement'] = maxDisp

        # Frequency step results
        if 'Step-Frequency' in odb.steps:
            step = odb.steps['Step-Frequency']
            for i in range(len(step.frames)):
                frame = step.frames[i]
                freq = frame.frameValue  # Frequency in Hz
                results['naturalFrequencies'].append(freq)

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
    
    # Debug: write start of sweep
    with open('sweep_debug.txt', 'w') as f:
        f.write(f"Starting sweep: {len(BETA_VALUES)} betas x {len(THETA_VALUES)} thetas = {totalConfigs} configs\n")

    for beta in BETA_VALUES:
        for theta in THETA_VALUES:
            configNum += 1
            betaStr = f"{beta:.4f}".replace('.', '_')
            thetaStr = f"{theta:.0f}"
            
            with open('sweep_debug.txt', 'a') as f:
                f.write(f"\n[{configNum}/{totalConfigs}] Processing: beta={beta:.4f}, theta={theta}°\n")

            print(f"\n[{configNum}/{totalConfigs}] Processing: beta={beta:.4f}, theta={theta}°")
            print("-" * 50)

            # Create model
            try:
                modelName, jobName, beta, theta, h = createModel(beta, theta)
                with open('sweep_debug.txt', 'a') as f:
                    f.write(f"  Model created: {modelName}\n")
                print(f"  Beam height: {h:.4f} cm")

                # Save model
                savePath = os.path.join(os.getcwd(), modelName)
                mdb.saveAs(pathName=savePath)
                with open('sweep_debug.txt', 'a') as f:
                    f.write(f"  Model saved: {savePath}.cae\n")
                print(f"  Model saved: {savePath}.cae")

                # Submit job
                with open('sweep_debug.txt', 'a') as f:
                    f.write(f"  Submitting job: {jobName}...\n")
                    f.write(f"  Jobs in mdb: {list(mdb.jobs.keys())}\n")
                print(f"  Submitting job: {jobName}...")
                
                # Check if job exists
                if jobName not in mdb.jobs:
                    with open('sweep_debug.txt', 'a') as f:
                        f.write(f"  ERROR: Job {jobName} not found in mdb.jobs\n")
                    raise Exception(f"Job {jobName} not found")
                
                # Submit and wait for completion
                mdb.jobs[jobName].submit()
                
                # Wait for completion with polling
                import time
                maxWait = 300  # 5 minutes max per job
                waitTime = 0
                while waitTime < maxWait:
                    time.sleep(2)
                    jobStatus = mdb.jobs[jobName].status
                    with open('sweep_debug.txt', 'a') as f:
                        f.write(f"    Waiting... status: {jobStatus}\n")
                    if jobStatus == COMPLETED or jobStatus == 'ABORTED' or jobStatus == 'FAILED':
                        break
                    waitTime += 2
                
                # Check job status
                jobStatus = mdb.jobs[jobName].status
                with open('sweep_debug.txt', 'a') as f:
                    f.write(f"  Final job status: {jobStatus}\n")
                print(f"  Final job status: {jobStatus}")

                if jobStatus == COMPLETED:
                    # Extract results
                    odbPath = os.path.join(os.getcwd(), f'{jobName}.odb')
                    print(f"  Extracting results from {odbPath}")
                    results = extractResults(odbPath, beta, theta)
                    print(f"  Results: {results}")

                    configKey = f"b{betaStr}_t{thetaStr}"
                    allResults[configKey] = results
                    print(f"  Results stored for {configKey}")

                    if results['maxStress']:
                        print(f"  Max Stress: {results['maxStress']/1e3:.2f} MPa")
                    if results['bucklingLoadFactors']:
                        print(f"  First Buckling LF: {results['bucklingLoadFactors'][0]:.4f}")
                    if results['naturalFrequencies']:
                        print(f"  First Natural Freq: {results['naturalFrequencies'][0]:.2f} Hz")
                else:
                    print(f"  Job did not complete successfully")

            except Exception as e:
                with open('sweep_debug.txt', 'a') as f:
                    f.write(f"  ERROR: {str(e)}\n")
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
    
    # Save all results to JSON after each iteration (for debugging)
    print(f"\n  Debug: allResults has {len(allResults)} entries")
    
    # Convert tuples to lists for JSON serialization
    jsonResults = {}
    for key, value in allResults.items():
        jsonResults[key] = {}
        for k, v in value.items():
            if isinstance(v, tuple):
                jsonResults[key][k] = list(v)
            else:
                jsonResults[key][k] = v

    print(f"  Debug: jsonResults has {len(jsonResults)} entries")
    with open(resultsFile, 'w') as f:
        json.dump(jsonResults, f, indent=2)
    print(f"  Debug: Results written to {resultsFile}")
    
    # Also write a simple text summary
    with open('sweep_summary.txt', 'w') as f:
        f.write(f"Total configurations: {len(allResults)}\n")
        for key, value in allResults.items():
            f.write(f"{key}: {value}\n")
    
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
