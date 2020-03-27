"""
This script serves to extract frame motions in all six degrees of freedom (DOF)
from .bvh files and export those into .csv files. The .csv file(s) maintain the
same name as the .bvh(s). In a .csv, each column corresponds to one DOF (six
columns per joint) and each row corresponds to a frame. Joints retain the same
ordering.

Batch operations can be performed with space separated .bvh files. This  script
will fail with files that DNE and non-.bvh files, but will successfully export
all preceding files. If run multiple times, the .csv file(s) will be overidden.

Ex syntax) bvh_to_csv.py file1.bvh relPath/file2.bvh C:absPath/file2.bvh
"""

import sys
import os


def writeToCvs(bvh, csv):
    for line in bvh_iterator(bvh):
        csv.write(','.join(line.split()))
        csv.write('\n')


def bvh_iterator(file):
    header = []

    for line in file:  # Go through beginning hierarchy info -> need to write headers
        if 'ROOT' in line or 'JOINT' in line:
            currJoint = line.split()[1]  # line format ROOT/JOINT jointName

        if 'CHANNELS' in line:
            chanList = line.split()[2:]  # line format CHANNELS chanCount [dof]

            header += [('_'.join([currJoint, c[1:4], c[0]])) for c in chanList]

        if 'Frame Time:' in line:  # Next lines are motion data -> break
            break

    csv.write(','.join(header) + '\n')  # Write header
    zz = 1
    for line in file:  # For each frame line
        if zz > 250:
            yield line
        else:
            zz = zz+1


if __name__ == '__main__':
    # Check file argument exists
    if (len(sys.argv) < 2):
        print('Error: too few arguments specified')

    for i in range(1, len(sys.argv)):
        fileName, fileType = os.path.splitext(sys.argv[i])

        # Check file type
        if (fileType.lower() != '.bvh'):
            print('Error: unsupported file type')
        bvh = open(sys.argv[i], 'r')  # Will throw error if file DNE
        csv = open(fileName + '.csv', 'w')  # Will override if file exists

        writeToCvs(bvh, csv)

        bvh.close()
        csv.close()
