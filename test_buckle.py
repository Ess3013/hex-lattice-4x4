# Test script to find correct BuckleStep syntax
from abaqus import *
from abaqusConstants import *
import step

# Create a test model
mdb.Model(name='TestModel')

# Try different BuckleStep syntaxes
try:
    # Try with numEigenvalues
    mdb.models['TestModel'].BuckleStep(name='Buckle1', previous='Initial', numEigenvalues=10)
    print("SUCCESS: numEigenvalues works")
except Exception as e:
    print(f"FAILED numEigenvalues: {e}")

try:
    # Try with eigenvalue
    mdb.models['TestModel'].BuckleStep(name='Buckle2', previous='Initial', eigenvalue=10.0)
    print("SUCCESS: eigenvalue works")
except Exception as e:
    print(f"FAILED eigenvalue: {e}")

try:
    # Try with minEigenvalue
    mdb.models['TestModel'].BuckleStep(name='Buckle3', previous='Initial', minEigenvalue=0.0, maxEigenvalue=100.0)
    print("SUCCESS: min/maxEigenvalue works")
except Exception as e:
    print(f"FAILED min/maxEigenvalue: {e}")

try:
    # Try with acousticEigenvalue
    mdb.models['TestModel'].BuckleStep(name='Buckle4', previous='Initial', acousticEigenvalue=10)
    print("SUCCESS: acousticEigenvalue works")
except Exception as e:
    print(f"FAILED acousticEigenvalue: {e}")

try:
    # Try minimal with just name and previous
    mdb.models['TestModel'].BuckleStep(name='Buckle5', previous='Initial')
    print("SUCCESS: minimal works")
except Exception as e:
    print(f"FAILED minimal: {e}")
