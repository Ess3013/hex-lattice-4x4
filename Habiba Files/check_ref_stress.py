import odbAccess
odb = odbAccess.openOdb('Job-1.odb')
frame = odb.steps.values()[-1].frames[-1]
stress = frame.fieldOutputs['S']
max_mises = 0.0
for v in stress.values:
    if v.mises > max_mises:
        max_mises = v.mises
with open('ref_stress.txt', 'w') as f:
    f.write('Reference Max Mises: %e\n' % max_mises)
odb.close()
