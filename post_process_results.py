# -*- coding: utf-8 -*-
"""
Post-Processing Results Script for Honeycomb Lattice Connecting Rod
MENG3505_Project01 Implementation

Extracts and analyzes results from Abaqus ODB files:
- Maximum stress (plasticity check)
- Buckling load factors
- Natural frequencies
- Frequency Response Function (FRF)
- Bandgap identification
"""

import os
import sys
import json
import math

# Add Abaqus Python modules to path (adjust path as needed for your installation)
# These are typically available when running from Abaqus/CAE

def extractResultsFromOdb(odbPath):
    """
    Extract comprehensive results from an Abaqus ODB file.
    
    Args:
        odbPath: Path to the .odb file
        
    Returns:
        Dictionary containing extracted results
    """
    try:
        from odbAccess import openOdb
    except ImportError:
        print("Error: odbAccess not available. Run this script from Abaqus/CAE or with proper environment.")
        return None
    
    results = {
        'odbPath': odbPath,
        'static': {
            'maxStress': None,
            'maxDisplacement': None,
            'maxStrain': None,
            'reactionForce': None
        },
        'buckling': {
            'loadFactors': [],
            'modes': []
        },
        'frequency': {
            'naturalFrequencies': []
        },
        'ssd': {
            'frequencies': [],
            'strainEnergy': [],
            'kineticEnergy': [],
            'displacement': []
        },
        'bandgaps': []
    }
    
    try:
        odb = openOdb(odbPath)
        
        # ========== STATIC STEP RESULTS ==========
        if 'Step-Static' in odb.steps:
            step = odb.steps['Step-Static']
            lastFrame = step.frames[-1]
            
            # Stress
            if 'S' in lastFrame.fieldOutputs:
                stress = lastFrame.fieldOutputs['S']
                maxStress = max(v.mises for v in stress.values)
                results['static']['maxStress'] = maxStress
                
                # Also get max principal stress for tension check
                maxPrincipal = max(v.principal[0] for v in stress.values)
                results['static']['maxPrincipalStress'] = maxPrincipal
            
            # Displacement
            if 'U' in lastFrame.fieldOutputs:
                disp = lastFrame.fieldOutputs['U']
                maxDisp = max(v.magnitude for v in disp.values)
                results['static']['maxDisplacement'] = maxDisp
                
                # Get Y-displacement (loading direction)
                uyValues = [v.data[1] for v in disp.values if len(v.data) > 1]
                if uyValues:
                    results['static']['maxUY'] = min(uyValues)  # Negative for compression
            
            # Strain
            if 'E' in lastFrame.fieldOutputs:
                strain = lastFrame.fieldOutputs['E']
                maxStrain = max(v.magnitude for v in strain.values)
                results['static']['maxStrain'] = maxStrain
            
            # Reaction Force
            if 'RF' in lastFrame.fieldOutputs:
                rf = lastFrame.fieldOutputs['RF']
                # Sum reaction forces at fixed boundary
                totalRFy = sum(v.data[1] for v in rf.values if len(v.data) > 1)
                results['static']['reactionForce'] = abs(totalRFy)
            
            # Plastic strain (if elastic-plastic analysis)
            if 'PEEQ' in lastFrame.fieldOutputs:
                peeq = lastFrame.fieldOutputs['PEEQ']
                maxPEEQ = max(v.data for v in peeq.values)
                results['static']['maxPlasticStrain'] = maxPEEQ
        
        # ========== BUCKLING STEP RESULTS ==========
        if 'Step-Buckling' in odb.steps:
            step = odb.steps['Step-Buckling']
            
            for i, frame in enumerate(step.frames):
                lf = frame.frameValue  # Load factor
                modeShape = f"Mode {i+1}"
                results['buckling']['loadFactors'].append(lf)
                results['buckling']['modes'].append(modeShape)
        
        # ========== FREQUENCY STEP RESULTS ==========
        if 'Step-Frequency' in odb.steps:
            step = odb.steps['Step-Frequency']
            
            for frame in step.frames:
                freq = frame.frameValue  # Frequency in Hz
                results['frequency']['naturalFrequencies'].append(freq)
        
        # ========== SSD STEP RESULTS (FRF) ==========
        if 'Step-SSD' in odb.steps:
            step = odb.steps['Step-SSD']
            
            # Get history output for strain energy
            if 'H-StrainEnergy' in step.historyRegions:
                histRegion = step.historyRegions['H-StrainEnergy']
                
                if 'ALLSE' in histRegion.historyOutputs:
                    data = histRegion.historyOutputs['ALLSE'].data
                    for freq, energy in data:
                        results['ssd']['frequencies'].append(freq)
                        results['ssd']['strainEnergy'].append(energy)
                
                if 'ALLIE' in histRegion.historyOutputs:
                    data = histRegion.historyOutputs['ALLIE'].data
                    results['ssd']['kineticEnergy'] = [e for _, e in data]
            
            # Get displacement frequency response from field output
            for frame in step.frames:
                freq = frame.frameValue
                if 'U' in frame.fieldOutputs:
                    disp = frame.fieldOutputs['U']
                    maxDisp = max(v.magnitude for v in disp.values)
                    results['ssd']['displacement'].append(maxDisp)
        
        odb.close()
        
    except Exception as e:
        print(f"Error extracting results from {odbPath}: {str(e)}")
        results['error'] = str(e)
    
    return results


def identifyBandgaps(frequencies, strainEnergy, threshold_factor=0.1):
    """
    Identify bandgaps from the FRF (strain energy vs frequency).
    
    A bandgap is a frequency range where vibration transmission is significantly
    attenuated (low strain energy indicates vibration absorption).
    
    Args:
        frequencies: List of frequencies (Hz)
        strainEnergy: List of strain energy values
        threshold_factor: Fraction of max SE to use as threshold
        
    Returns:
        List of bandgap dictionaries with onset, width, and center frequency
    """
    if not frequencies or not strainEnergy:
        return []
    
    import numpy as np
    
    freq_arr = np.array(frequencies)
    se_arr = np.array(strainEnergy)
    
    # Normalize strain energy
    se_max = np.max(se_arr)
    if se_max == 0:
        return []
    
    se_normalized = se_arr / se_max
    
    # Threshold for bandgap detection
    threshold = threshold_factor
    
    # Find frequency ranges where SE is below threshold (bandgaps)
    below_threshold = se_normalized < threshold
    
    bandgaps = []
    in_bandgap = False
    bandgap_start = None
    
    for i, is_below in enumerate(below_threshold):
        if is_below and not in_bandgap:
            # Start of bandgap
            in_bandgap = True
            bandgap_start = freq_arr[i]
        elif not is_below and in_bandgap:
            # End of bandgap
            in_bandgap = False
            bandgap_end = freq_arr[i]
            
            bandgaps.append({
                'onset': float(bandgap_start),
                'end': float(bandgap_end),
                'width': float(bandgap_end - bandgap_start),
                'center': float((bandgap_start + bandgap_end) / 2)
            })
    
    # Handle case where bandgap extends to end of frequency range
    if in_bandgap:
        bandgap_end = freq_arr[-1]
        bandgaps.append({
            'onset': float(bandgap_start),
            'end': float(bandgap_end),
            'width': float(bandgap_end - bandgap_start),
            'center': float((bandgap_start + bandgap_end) / 2)
        })
    
    return bandgaps


def checkPlasticity(maxStress, yieldStress=276e3):
    """
    Check if stress exceeds yield stress (plasticity onset).
    
    Args:
        maxStress: Maximum von Mises stress (N/cm²)
        yieldStress: Material yield stress (N/cm²), default 276 MPa for Al-B4C
        
    Returns:
        Dictionary with plasticity check results
    """
    if maxStress is None:
        return {'hasPlasticity': None, 'safetyFactor': None}
    
    safetyFactor = yieldStress / maxStress
    hasPlasticity = maxStress > yieldStress
    
    return {
        'hasPlasticity': hasPlasticity,
        'safetyFactor': safetyFactor,
        'maxStress_MPa': maxStress / 1e3,
        'yieldStress_MPa': yieldStress / 1e3
    }


def checkBuckling(loadFactors, appliedLoad=10000.0):
    """
    Check buckling stability.
    
    Args:
        loadFactors: List of buckling load factors
        appliedLoad: Applied compressive load (N)
        
    Returns:
        Dictionary with buckling check results
    """
    if not loadFactors:
        return {'willBuckle': None, 'criticalLoad': None}
    
    firstLF = loadFactors[0]
    criticalLoad = firstLF * appliedLoad
    willBuckle = firstLF < 1.0  # Buckles if load factor < 1
    
    return {
        'willBuckle': willBuckle,
        'criticalLoad_N': criticalLoad,
        'criticalLoad_kN': criticalLoad / 1000,
        'loadFactor': firstLF,
        'safetyMargin': (firstLF - 1.0) * 100 if firstLF > 1 else 0
    }


def processAllResults(resultsDir=None):
    """
    Process all ODB files in the results directory.
    
    Args:
        resultsDir: Directory containing ODB files (default: current directory)
        
    Returns:
        Dictionary with all processed results
    """
    if resultsDir is None:
        resultsDir = os.path.dirname(__file__)
    
    # Find all ODB files
    odbFiles = [f for f in os.listdir(resultsDir) if f.endswith('.odb')]
    
    if not odbFiles:
        print(f"No ODB files found in {resultsDir}")
        return {}
    
    print(f"Found {len(odbFiles)} ODB files to process")
    
    allResults = {}
    
    for odbFile in odbFiles:
        odbPath = os.path.join(resultsDir, odbFile)
        print(f"\nProcessing: {odbFile}")
        
        results = extractResultsFromOdb(odbPath)
        
        if results:
            # Extract beta and theta from filename
            # Expected format: Job_b0_0667_t10.odb or similar
            nameParts = odbFile.replace('.odb', '').split('_')
            beta = None
            theta = None
            
            for part in nameParts:
                if part.startswith('b'):
                    try:
                        beta = float(part[1:])
                    except:
                        pass
                elif part.startswith('t'):
                    try:
                        theta = float(part[1:])
                    except:
                        pass
            
            results['beta'] = beta
            results['theta'] = theta
            
            # Perform analysis
            results['plasticityCheck'] = checkPlasticity(results['static']['maxStress'])
            results['bucklingCheck'] = checkBuckling(results['buckling']['loadFactors'])
            
            # Identify bandgaps
            if results['ssd']['frequencies'] and results['ssd']['strainEnergy']:
                results['bandgaps'] = identifyBandgaps(
                    results['ssd']['frequencies'],
                    results['ssd']['strainEnergy']
                )
            
            # Store in dictionary
            configKey = f"b{beta}_t{theta}" if beta is not None and theta is not None else odbFile
            allResults[configKey] = results
    
    return allResults


def exportResultsToCSV(allResults, outputPath=None):
    """
    Export processed results to CSV format.
    
    Args:
        allResults: Dictionary of processed results
        outputPath: Output CSV file path
    """
    import csv
    
    if outputPath is None:
        outputPath = os.path.join(os.path.dirname(__file__), 'results_summary.csv')
    
    # Prepare rows
    rows = []
    for configKey, results in allResults.items():
        row = {
            'Configuration': configKey,
            'Beta': results.get('beta', 'N/A'),
            'Theta': results.get('theta', 'N/A'),
            'Max_Stress_MPa': results['plasticityCheck'].get('maxStress_MPa', 'N/A'),
            'Safety_Factor': results['plasticityCheck'].get('safetyFactor', 'N/A'),
            'Has_Plasticity': results['plasticityCheck'].get('hasPlasticity', 'N/A'),
            'Critical_Load_kN': results['bucklingCheck'].get('criticalLoad_kN', 'N/A'),
            'Buckling_LF': results['bucklingCheck'].get('loadFactor', 'N/A'),
            'First_Natural_Freq_Hz': results['frequency']['naturalFrequencies'][0] if results['frequency']['naturalFrequencies'] else 'N/A',
            'Num_Bandgaps': len(results['bandgaps']),
        }
        
        if results['bandgaps']:
            firstBandgap = results['bandgaps'][0]
            row['First_Bandgap_Onset_Hz'] = firstBandgap['onset']
            row['First_Bandgap_Width_Hz'] = firstBandgap['width']
        else:
            row['First_Bandgap_Onset_Hz'] = 'N/A'
            row['First_Bandgap_Width_Hz'] = 'N/A'
        
        rows.append(row)
    
    # Write CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(outputPath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\nResults exported to: {outputPath}")
    
    return outputPath


def printSummary(allResults):
    """Print a summary of all results"""
    
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    for configKey, results in sorted(allResults.items()):
        print(f"\nConfiguration: {configKey}")
        print("-" * 50)
        
        # Plasticity
        pc = results['plasticityCheck']
        if pc['maxStress_MPa']:
            print(f"  Max Stress: {pc['maxStress_MPa']:.2f} MPa")
            print(f"  Safety Factor: {pc['safetyFactor']:.2f}")
            print(f"  Plasticity: {'YES - FAIL' if pc['hasPlasticity'] else 'No - OK'}")
        
        # Buckling
        bc = results['bucklingCheck']
        if bc['loadFactor']:
            print(f"  Critical Load: {bc['criticalLoad_kN']:.2f} kN")
            print(f"  Buckling LF: {bc['loadFactor']:.4f}")
            print(f"  Buckling: {'YES - FAIL' if bc['willBuckle'] else 'No - OK'}")
        
        # Frequencies
        if results['frequency']['naturalFrequencies']:
            print(f"  1st Natural Freq: {results['frequency']['naturalFrequencies'][0]:.2f} Hz")
        
        # Bandgaps
        if results['bandgaps']:
            print(f"  Bandgaps Found: {len(results['bandgaps'])}")
            for i, bg in enumerate(results['bandgaps'][:3]):  # Show first 3
                print(f"    Bandgap {i+1}: {bg['onset']:.1f} - {bg['end']:.1f} Hz (width: {bg['width']:.1f} Hz)")
        else:
            print(f"  Bandgaps Found: 0")
    
    print("\n" + "=" * 80)


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == '__main__':
    print("=" * 80)
    print("POST-PROCESSING RESULTS - HONEYCOMB LATTICE CONNECTING ROD")
    print("=" * 80)
    
    # Process all ODB files
    allResults = processAllResults()
    
    if allResults:
        # Print summary
        printSummary(allResults)
        
        # Export to CSV
        exportResultsToCSV(allResults)
        
        # Save to JSON
        jsonPath = os.path.join(os.path.dirname(__file__), 'processed_results.json')
        
        # Convert for JSON serialization
        jsonResults = {}
        for key, value in allResults.items():
            jsonResults[key] = {}
            for k, v in value.items():
                if isinstance(v, (tuple,)):
                    jsonResults[key][k] = list(v)
                else:
                    jsonResults[key][k] = v
        
        with open(jsonPath, 'w') as f:
            json.dump(jsonResults, f, indent=2)
        
        print(f"\nResults saved to: {jsonPath}")
    else:
        print("\nNo results to process. Run the parametric sweep first.")
    
    print("\n" + "=" * 80)
