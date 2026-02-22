# -*- coding: utf-8 -*-
"""
Report Generation Script for Honeycomb Lattice Connecting Rod
MENG3505_Project01 Implementation

Generates comprehensive reports including:
- Results tables
- FRF plots
- Bandgap visualization
- Optimization recommendations
- Trade-off analysis
"""

import os
import json
import math

# ============================================================
# LOAD RESULTS
# ============================================================
def loadResults(resultsFile=None):
    """Load processed results from JSON file"""

    if resultsFile is None:
        resultsFile = os.path.join(os.getcwd(), 'processed_results.json')

    if not os.path.exists(resultsFile):
        # Try alternative file
        altFile = os.path.join(os.getcwd(), 'parametric_results.json')
        if os.path.exists(altFile):
            resultsFile = altFile
        else:
            print(f"Results file not found: {resultsFile}")
            return None
    
    with open(resultsFile, 'r') as f:
        results = json.load(f)
    
    print(f"Loaded results from: {resultsFile}")
    print(f"Configurations: {len(results)}")
    
    return results


# ============================================================
# GENERATE RESULTS TABLE
# ============================================================
def generateResultsTable(results):
    """Generate a formatted results table"""

    table = []
    headers = [
        'Config', 'β', 'θ (°)',
        'σ_max (MPa)', 'SF', 'Plastic?',
        'P_cr (kN)', 'LF', 'Buckle?',
        'f₁ (Hz)', '#BG', 'BG₁ Onset (Hz)', 'BG₁ Width (Hz)'
    ]

    for configKey, data in sorted(results.items()):
        row = {'Config': configKey}

        # Design variables
        beta_val = data.get('beta', 'N/A')
        theta_val = data.get('theta', 'N/A')
        row['β'] = f"{beta_val:.4f}" if isinstance(beta_val, (int, float)) else beta_val
        row['θ (°)'] = f"{theta_val:.0f}" if isinstance(theta_val, (int, float)) else theta_val

        # Plasticity results
        if 'plasticityCheck' in data:
            pc = data['plasticityCheck']
            stress_val = pc.get('maxStress_MPa', 'N/A')
            sf_val = pc.get('safetyFactor', 'N/A')
            row['σ_max (MPa)'] = f"{stress_val:.2f}" if isinstance(stress_val, (int, float)) else stress_val
            row['SF'] = f"{sf_val:.2f}" if isinstance(sf_val, (int, float)) and sf_val != 'N/A' else ('N/A' if sf_val == 'N/A' else f"{sf_val:.2f}")
            row['Plastic?'] = 'YES' if pc.get('hasPlasticity') else 'No'
        else:
            row['σ_max (MPa)'] = 'N/A'
            row['SF'] = 'N/A'
            row['Plastic?'] = 'N/A'

        # Buckling results
        if 'bucklingCheck' in data:
            bc = data['bucklingCheck']
            load_val = bc.get('criticalLoad_kN', 'N/A')
            lf_val = bc.get('loadFactor', 'N/A')
            row['P_cr (kN)'] = f"{load_val:.2f}" if isinstance(load_val, (int, float)) else load_val
            row['LF'] = f"{lf_val:.4f}" if isinstance(lf_val, (int, float)) and lf_val != 'N/A' else ('N/A' if lf_val == 'N/A' else f"{lf_val:.4f}")
            row['Buckle?'] = 'YES' if bc.get('willBuckle') else 'No'
        else:
            row['P_cr (kN)'] = 'N/A'
            row['LF'] = 'N/A'
            row['Buckle?'] = 'N/A'

        # Frequency results
        if 'frequency' in data and data['frequency'].get('naturalFrequencies'):
            freq_val = data['frequency']['naturalFrequencies'][0]
            row['f₁ (Hz)'] = f"{freq_val:.2f}" if isinstance(freq_val, (int, float)) else 'N/A'
        else:
            row['f₁ (Hz)'] = 'N/A'

        # Bandgap results
        if 'bandgaps' in data and len(data['bandgaps']) > 0:
            row['#BG'] = str(len(data['bandgaps']))
            bg1 = data['bandgaps'][0]
            onset_val = bg1.get('onset', 'N/A')
            width_val = bg1.get('width', 'N/A')
            row['BG₁ Onset (Hz)'] = f"{onset_val:.1f}" if isinstance(onset_val, (int, float)) else onset_val
            row['BG₁ Width (Hz)'] = f"{width_val:.1f}" if isinstance(width_val, (int, float)) else width_val
        else:
            row['#BG'] = '0'
            row['BG₁ Onset (Hz)'] = 'N/A'
            row['BG₁ Width (Hz)'] = 'N/A'

        table.append(row)

    return headers, table


def printTable(headers, table):
    """Print formatted table to console"""
    
    # Calculate column widths
    widths = {h: len(h) for h in headers}
    for row in table:
        for h in headers:
            widths[h] = max(widths[h], len(str(row.get(h, ''))))
    
    # Print header
    headerLine = ' | '.join(h.center(widths[h]) for h in headers)
    separator = '-+-'.join('-' * widths[h] for h in headers)
    
    print("\n" + "=" * len(headerLine))
    print("RESULTS TABLE")
    print("=" * len(headerLine))
    print(headerLine)
    print(separator)
    
    # Print rows
    for row in table:
        rowLine = ' | '.join(str(row.get(h, '')).center(widths[h]) for h in headers)
        print(rowLine)
    
    print(separator)
    print(f"Total configurations: {len(table)}")
    print("=" * len(headerLine) + "\n")


def exportTableToCSV(headers, table, outputPath=None):
    """Export table to CSV file"""
    
    import csv

    if outputPath is None:
        outputPath = os.path.join(os.getcwd(), 'results_table.csv')
    
    with open(outputPath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(table)
    
    print(f"Table exported to: {outputPath}")
    return outputPath


# ============================================================
# GENERATE PLOTS
# ============================================================
def generatePlots(results):
    """Generate matplotlib plots for results visualization"""

    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
    except ImportError:
        print("Matplotlib not available. Skipping plot generation.")
        return []

    outputFiles = []
    outputDir = os.getcwd()

    # Extract data for plotting
    betas = []
    thetas = []
    maxStresses = []
    bucklingLFs = []
    firstFreqs = []
    bandgapWidths = []
    bandgapOnsets = []

    for configKey, data in results.items():
        beta_val = data.get('beta', 0)
        theta_val = data.get('theta', 0)
        betas.append(beta_val if isinstance(beta_val, (int, float)) else 0)
        thetas.append(theta_val if isinstance(theta_val, (int, float)) else 0)

        # Max stress
        if 'plasticityCheck' in data:
            stress_val = data['plasticityCheck'].get('maxStress_MPa')
            maxStresses.append(stress_val if isinstance(stress_val, (int, float)) else None)
        else:
            maxStresses.append(None)

        # Buckling LF
        if 'bucklingCheck' in data:
            lf_val = data['bucklingCheck'].get('loadFactor')
            bucklingLFs.append(lf_val if isinstance(lf_val, (int, float)) else None)
        else:
            bucklingLFs.append(None)

        # First natural frequency
        if 'frequency' in data and data['frequency'].get('naturalFrequencies'):
            freq_val = data['frequency']['naturalFrequencies'][0]
            firstFreqs.append(freq_val if isinstance(freq_val, (int, float)) else None)
        else:
            firstFreqs.append(None)

        # Bandgap info
        if 'bandgaps' in data and len(data['bandgaps']) > 0:
            onset_val = data['bandgaps'][0].get('onset')
            width_val = data['bandgaps'][0].get('width')
            bandgapOnsets.append(onset_val if isinstance(onset_val, (int, float)) else None)
            bandgapWidths.append(width_val if isinstance(width_val, (int, float)) else None)
        else:
            bandgapOnsets.append(None)
            bandgapWidths.append(None)
    
    # ========== Plot 1: Max Stress vs Beta ==========
    fig, ax = plt.subplots(figsize=(10, 6))
    
    validIdx = [i for i, v in enumerate(maxStresses) if v is not None]
    if validIdx:
        plotBetas = [betas[i] for i in validIdx]
        plotStresses = [maxStresses[i] for i in validIdx]
        plotThetas = [thetas[i] for i in validIdx]
        
        scatter = ax.scatter(plotBetas, plotStresses, c=plotThetas, 
                            cmap='viridis', s=100, alpha=0.7)
        ax.axhline(y=276, color='r', linestyle='--', label='Yield Stress (276 MPa)')
        
        ax.set_xlabel('Slenderness Ratio (β = h/L)')
        ax.set_ylabel('Maximum Stress (MPa)')
        ax.set_title('Maximum Stress vs Slenderness Ratio')
        ax.legend()
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Configuration Angle θ (°)')
        
        plt.tight_layout()
        plotFile = os.path.join(outputDir, 'stress_vs_beta.png')
        plt.savefig(plotFile, dpi=150)
        plt.close()
        outputFiles.append(plotFile)
        print(f"Generated: {plotFile}")
    
    # ========== Plot 2: Buckling LF vs Beta ==========
    fig, ax = plt.subplots(figsize=(10, 6))
    
    validIdx = [i for i, v in enumerate(bucklingLFs) if v is not None]
    if validIdx:
        plotBetas = [betas[i] for i in validIdx]
        plotLFs = [bucklingLFs[i] for i in validIdx]
        plotThetas = [thetas[i] for i in validIdx]
        
        scatter = ax.scatter(plotBetas, plotLFs, c=plotThetas, 
                            cmap='viridis', s=100, alpha=0.7)
        ax.axhline(y=1.0, color='r', linestyle='--', label='Buckling Threshold (LF=1)')
        
        ax.set_xlabel('Slenderness Ratio (β = h/L)')
        ax.set_ylabel('Buckling Load Factor')
        ax.set_title('Buckling Load Factor vs Slenderness Ratio')
        ax.legend()
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Configuration Angle θ (°)')
        
        plt.tight_layout()
        plotFile = os.path.join(outputDir, 'buckling_vs_beta.png')
        plt.savefig(plotFile, dpi=150)
        plt.close()
        outputFiles.append(plotFile)
        print(f"Generated: {plotFile}")
    
    # ========== Plot 3: Bandgap Width vs Beta ==========
    fig, ax = plt.subplots(figsize=(10, 6))
    
    validIdx = [i for i, v in enumerate(bandgapWidths) if v is not None]
    if validIdx:
        plotBetas = [betas[i] for i in validIdx]
        plotWidths = [bandgapWidths[i] for i in validIdx]
        plotThetas = [thetas[i] for i in validIdx]
        
        scatter = ax.scatter(plotBetas, plotWidths, c=plotThetas, 
                            cmap='viridis', s=100, alpha=0.7)
        
        ax.set_xlabel('Slenderness Ratio (β = h/L)')
        ax.set_ylabel('First Bandgap Width (Hz)')
        ax.set_title('Bandgap Width vs Slenderness Ratio')
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Configuration Angle θ (°)')
        
        plt.tight_layout()
        plotFile = os.path.join(outputDir, 'bandgap_width_vs_beta.png')
        plt.savefig(plotFile, dpi=150)
        plt.close()
        outputFiles.append(plotFile)
        print(f"Generated: {plotFile}")
    
    # ========== Plot 4: Bandgap Onset vs Beta ==========
    fig, ax = plt.subplots(figsize=(10, 6))
    
    validIdx = [i for i, v in enumerate(bandgapOnsets) if v is not None]
    if validIdx:
        plotBetas = [betas[i] for i in validIdx]
        plotOnsets = [bandgapOnsets[i] for i in validIdx]
        plotThetas = [thetas[i] for i in validIdx]
        
        scatter = ax.scatter(plotBetas, plotOnsets, c=plotThetas, 
                            cmap='viridis', s=100, alpha=0.7)
        
        ax.set_xlabel('Slenderness Ratio (β = h/L)')
        ax.set_ylabel('First Bandgap Onset Frequency (Hz)')
        ax.set_title('Bandgap Onset Frequency vs Slenderness Ratio')
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Configuration Angle θ (°)')
        
        plt.tight_layout()
        plotFile = os.path.join(outputDir, 'bandgap_onset_vs_beta.png')
        plt.savefig(plotFile, dpi=150)
        plt.close()
        outputFiles.append(plotFile)
        print(f"Generated: {plotFile}")
    
    # ========== Plot 5: Trade-off Chart (Stress vs Bandgap Width) ==========
    fig, ax = plt.subplots(figsize=(10, 6))
    
    validIdx = [i for i in range(len(maxStresses)) 
                if maxStresses[i] is not None and bandgapWidths[i] is not None]
    if validIdx:
        plotStresses = [maxStresses[i] for i in validIdx]
        plotWidths = [bandgapWidths[i] for i in validIdx]
        plotBetas = [betas[i] for i in validIdx]
        plotThetas = [thetas[i] for i in validIdx]
        
        scatter = ax.scatter(plotStresses, plotWidths, c=plotBetas, 
                            cmap='plasma', s=100, alpha=0.7)
        
        ax.set_xlabel('Maximum Stress (MPa)')
        ax.set_ylabel('First Bandgap Width (Hz)')
        ax.set_title('Trade-off: Stress vs Bandgap Width')
        
        cbar = plt.colorbar(scatter)
        cbar.set_label('Slenderness Ratio (β)')
        
        plt.tight_layout()
        plotFile = os.path.join(outputDir, 'tradeoff_stress_bandgap.png')
        plt.savefig(plotFile, dpi=150)
        plt.close()
        outputFiles.append(plotFile)
        print(f"Generated: {plotFile}")
    
    return outputFiles


# ============================================================
# OPTIMIZATION RECOMMENDATION
# ============================================================
def findOptimalConfiguration(results):
    """
    Find the optimal configuration based on design objectives:
    1. No plasticity (σ < σ_yield)
    2. No buckling (LF > 1)
    3. Minimize first bandgap onset frequency
    4. Maximize first bandgap width
    """
    
    YIELD_STRESS_MPa = 276  # Aluminum-B4C composite
    
    candidates = []
    
    for configKey, data in results.items():
        score = 0
        issues = []
        
        # Check plasticity
        hasPlasticity = False
        safetyFactor = None
        if 'plasticityCheck' in data:
            pc = data['plasticityCheck']
            hasPlasticity = pc.get('hasPlasticity', False)
            safetyFactor = pc.get('safetyFactor')
            
            if hasPlasticity:
                issues.append('Plasticity detected')
                score -= 100  # Heavy penalty
            elif safetyFactor and safetyFactor > 1:
                score += safetyFactor * 10  # Reward high safety factor
        
        # Check buckling
        willBuckle = False
        bucklingLF = None
        if 'bucklingCheck' in data:
            bc = data['bucklingCheck']
            willBuckle = bc.get('willBuckle', False)
            bucklingLF = bc.get('loadFactor')
            
            if willBuckle:
                issues.append('Buckling instability')
                score -= 100  # Heavy penalty
            elif bucklingLF and bucklingLF > 1:
                score += (bucklingLF - 1) * 50  # Reward safety margin
        
        # Bandgap objectives
        bandgapOnset = None
        bandgapWidth = None
        if 'bandgaps' in data and len(data['bandgaps']) > 0:
            bandgapOnset = data['bandgaps'][0]['onset']
            bandgapWidth = data['bandgaps'][0]['width']
            
            # Lower onset is better (normalize to 0-1000 Hz range)
            if bandgapOnset:
                score -= bandgapOnset / 10  # Penalty for high onset
            
            # Wider bandgap is better
            if bandgapWidth:
                score += bandgapWidth / 5  # Reward for width
        else:
            issues.append('No bandgap detected')
            score -= 50
        
        candidates.append({
            'config': configKey,
            'beta': data.get('beta'),
            'theta': data.get('theta'),
            'score': score,
            'issues': issues,
            'hasPlasticity': hasPlasticity,
            'willBuckle': willBuckle,
            'safetyFactor': safetyFactor,
            'bucklingLF': bucklingLF,
            'bandgapOnset': bandgapOnset,
            'bandgapWidth': bandgapWidth
        })
    
    # Sort by score (descending)
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    return candidates


def generateOptimizationReport(candidates, outputPath=None):
    """Generate optimization recommendation report"""

    if outputPath is None:
        outputPath = os.path.join(os.getcwd(), 'optimization_report.txt')
    
    with open(outputPath, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("OPTIMIZATION REPORT - HONEYCOMB LATTICE CONNECTING ROD\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("DESIGN OBJECTIVES:\n")
        f.write("  1. Eliminate plasticity in lattice members (σ < 276 MPa)\n")
        f.write("  2. Minimize buckling instabilities (LF > 1)\n")
        f.write("  3. Minimize onset frequency of first bandgap\n")
        f.write("  4. Maximize width of first bandgap\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("TOP 5 RECOMMENDED CONFIGURATIONS:\n")
        f.write("-" * 80 + "\n\n")
        
        for i, cand in enumerate(candidates[:5], 1):
            f.write(f"Rank #{i}: {cand['config']}\n")
            f.write(f"  Score: {cand['score']:.2f}\n")
            f.write(f"  Design Variables: β = {cand['beta']:.4f}, θ = {cand['theta']}°\n")
            
            if cand['issues']:
                f.write(f"  Issues: {', '.join(cand['issues'])}\n")
            else:
                f.write(f"  Issues: None - All criteria satisfied\n")
            
            f.write(f"  Performance Metrics:\n")
            if cand['safetyFactor']:
                f.write(f"    - Stress Safety Factor: {cand['safetyFactor']:.2f}\n")
            if cand['bucklingLF']:
                f.write(f"    - Buckling Load Factor: {cand['bucklingLF']:.4f}\n")
            if cand['bandgapOnset']:
                f.write(f"    - First Bandgap Onset: {cand['bandgapOnset']:.1f} Hz\n")
            if cand['bandgapWidth']:
                f.write(f"    - First Bandgap Width: {cand['bandgapWidth']:.1f} Hz\n")
            
            f.write("\n")
        
        f.write("-" * 80 + "\n")
        f.write("OPTIMAL CONFIGURATION:\n")
        f.write("-" * 80 + "\n\n")
        
        optimal = candidates[0]
        f.write(f"Recommended Design: {optimal['config']}\n\n")
        f.write(f"Design Variables:\n")
        f.write(f"  - Slenderness Ratio (β): {optimal['beta']:.4f}\n")
        f.write(f"  - Configuration Angle (θ): {optimal['theta']}°\n\n")
        
        f.write(f"Expected Performance:\n")
        if optimal['safetyFactor']:
            f.write(f"  - Stress Safety Factor: {optimal['safetyFactor']:.2f}\n")
        if optimal['bucklingLF']:
            f.write(f"  - Buckling Load Factor: {optimal['bucklingLF']:.4f}\n")
        if optimal['bandgapOnset']:
            f.write(f"  - First Bandgap Onset: {optimal['bandgapOnset']:.1f} Hz\n")
        if optimal['bandgapWidth']:
            f.write(f"  - First Bandgap Width: {optimal['bandgapWidth']:.1f} Hz\n")
        
        f.write("\n")
        f.write("-" * 80 + "\n")
        f.write("TRADE-OFF ANALYSIS:\n")
        f.write("-" * 80 + "\n\n")
        
        f.write("Impact of Design Variables:\n\n")
        
        f.write("1. Slenderness Ratio (β = h/L):\n")
        f.write("   - Higher β (thicker beams):\n")
        f.write("     * Lower stress (better for plasticity)\n")
        f.write("     * Higher buckling resistance\n")
        f.write("     * Higher bandgap onset frequency\n")
        f.write("     * Increased weight and material cost\n\n")
        f.write("   - Lower β (thinner beams):\n")
        f.write("     * Higher stress (risk of plasticity)\n")
        f.write("     * Lower buckling resistance\n")
        f.write("     * Lower bandgap onset frequency\n")
        f.write("     * Reduced weight and material cost\n\n")
        
        f.write("2. Configuration Angle (θ):\n")
        f.write("   - Affects load distribution in lattice members\n")
        f.write("   - Influences natural frequencies and bandgap locations\n")
        f.write("   - May affect manufacturing complexity\n\n")
        
        f.write("Other Considerations:\n")
        f.write("  - Weight: Proportional to β (beam cross-section)\n")
        f.write("  - Cost: Higher β increases material usage\n")
        f.write("  - Durability: Higher safety factors improve fatigue life\n")
        f.write("  - Manufacturing: Very low β may be challenging to fabricate\n")
        f.write("  - Friction: Surface treatment may be needed for wet/dry conditions\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("END OF OPTIMIZATION REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"Optimization report saved to: {outputPath}")
    return outputPath


# ============================================================
# MAIN REPORT GENERATION
# ============================================================
def generateFullReport():
    """Generate complete report package"""
    
    print("=" * 80)
    print("GENERATING COMPREHENSIVE REPORT")
    print("=" * 80)
    
    # Load results
    results = loadResults()
    
    if not results:
        print("No results available. Run parametric sweep and post-processing first.")
        return
    
    # Generate results table
    headers, table = generateResultsTable(results)
    printTable(headers, table)
    exportTableToCSV(headers, table)
    
    # Generate plots
    plotFiles = generatePlots(results)
    
    # Find optimal configuration
    candidates = findOptimalConfiguration(results)
    
    # Generate optimization report
    generateOptimizationReport(candidates)
    
    # Print summary
    print("\n" + "=" * 80)
    print("GENERATED FILES:")
    print("=" * 80)
    print("  - results_table.csv (Results summary)")
    print("  - optimization_report.txt (Design recommendations)")
    for plotFile in plotFiles:
        print(f"  - {os.path.basename(plotFile)}")
    print("=" * 80)
    
    return {
        'table': (headers, table),
        'plots': plotFiles,
        'candidates': candidates
    }


# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == '__main__':
    generateFullReport()
