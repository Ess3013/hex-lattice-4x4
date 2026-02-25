from abaqus import *
from abaqusConstants import *
import odbAccess

def inspect():
    try:
        odb = odbAccess.openOdb('Job-1.odb')
        a = odb.rootAssembly
        instance = a.instances.values()[0]
        
        with open('reference_data.txt', 'w') as f:
            f.write('Reference Model Data\n')
            f.write('====================\n\n')
            
            x_coords = [n.coordinates[0] for n in instance.nodes]
            y_coords = [n.coordinates[1] for n in instance.nodes]
            f.write('Part Bounding Box:\n')
            f.write('X: [%f, %f]\n' % (min(x_coords), max(x_coords)))
            f.write('Y: [%f, %f]\n\n' % (min(y_coords), max(y_coords)))
            
            for setName in ['SET-1', 'SET-2']:
                found = False
                if setName in a.nodeSets.keys():
                    found = True
                    f.write('--- %s (Node Set) ---\n' % setName)
                    ns = a.nodeSets[setName]
                    all_xs = []
                    all_ys = []
                    for inst_nodes in ns.nodes:
                        for n in inst_nodes:
                            all_xs.append(n.coordinates[0])
                            all_ys.append(n.coordinates[1])
                    f.write('Count: %d\n' % len(all_xs))
                    f.write('X Range: [%f, %f]\n' % (min(all_xs), max(all_xs)))
                    f.write('Y Range: [%f, %f]\n\n' % (min(all_ys), max(all_ys)))
                
                if setName in a.elementSets.keys():
                    found = True
                    f.write('--- %s (Element Set) ---\n' % setName)
                    es = a.elementSets[setName]
                    all_xs = []
                    all_ys = []
                    for inst_elems in es.elements:
                        for e in inst_elems:
                            for nLabel in e.connectivity:
                                c = instance.nodes[nLabel-1].coordinates
                                all_xs.append(c[0])
                                all_ys.append(c[1])
                    f.write('X Range: [%f, %f]\n' % (min(all_xs), max(all_xs)))
                    f.write('Y Range: [%f, %f]\n\n' % (min(all_ys), max(all_ys)))
                if not found:
                    f.write('Set %s not found\n' % setName)

        odb.close()
    except Exception as e:
        with open('reference_data.txt', 'a') as f:
            f.write('\nError: %s' % str(e))

if __name__ == '__main__':
    inspect()
