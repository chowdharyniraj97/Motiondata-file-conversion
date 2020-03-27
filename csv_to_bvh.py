"""
This script serves to convert frame motions within a csv to bvh. The skeleton
currently is being populated from a bvh, but should eventually be replaced with
information for a generic child/adult.

Batch operations can be performed with space separated .bvh files. This script
will fail with files that DNE and non-.csv files, but will successfully export
all preceding files. If run multiple times, the .csv file(s) will be overidden.

New bvh files are created in an output directory within the same location as
the csv file. Lines marked with '# TEMP' represent the logic to do this - as it
is a temporary solution until the generic skeletons are made.

Ex syntax) csv_to_bvh.py motionfile.csv skeletonfile.bvh
"""
import sys
import csv
import os
from pathlib import Path

FRAME_TIME = 0.00833333  # 120fps

"""
This function populates the motion data within @csvFile to @bvhFile. It assumes
@bvhFile already has skeleton data.

@param bvhFile: the bvh file to write to
@param csvFile: the csv file to retrieve motion data from
"""


def writeFromCsv(bvhFile, csvFile):
    csvReader = csv.reader(csvFile, delimiter=',')
    next(csvReader, None)  # skip the headers
    # Used since frame amount must be known before looping
    rows = list(csvReader)
    frameCnt = len(rows)

    bvhFile.write('Frames: ' + str(frameCnt) +
                  '\nFrame Time: ' + str(FRAME_TIME) + '\n')

    for _, line in enumerate(rows):
        # Used for if file has 6dof and only either pos or rot is needed
        # pos = [line[i] for i in range(0, len(line)) if i%6 == 0 or (i - 1)%6 == 0 or (i - 2)%6 == 0]
        # rot = [line[i] for i in range(0, len(line)) if (i + 3)%6 == 0 or (i + 2)%6 == 0 or (i + 1)%6 == 0]

        bvhFile.write(" ".join(line) + '\n')


"""
This function copies the skeleton data (hierarchy info, offsets, channels,
etc.) from @oldBvh to @newBvh.

@param newBvh: the bvh file to copy the data to
@param oldBvh: the bvh file to copy the data from
"""


def writeFromBvh(newBvh, oldBvh):
    for line in oldBvh:  # Write beginning hierarchy info
        newBvh.write(line)

        if 'MOTION' in line:  # Next lines are motion data -> break
            break


if __name__ == '__main__':
    # Check file arguments exists
    print(len(sys.argv))
    if (len(sys.argv) < 3):

        print('Error: too few arguments specified')

    # Loop over batch
    for i in range(1, len(sys.argv), 2):
        # Generate paths
        csvName, csvType = os.path.splitext(sys.argv[i])
        bvhName, bvhType = os.path.splitext(sys.argv[i + 1])

        # Check file types
        if (csvType.lower() != '.csv' or bvhType.lower() != '.bvh'):
            print('Error: unsupported file type')

        # Path('output').mkdir(parents=True, exist_ok=True)  # TEMP

        # Open files
        csvFile = open(sys.argv[i], 'r')  # Will throw error if file DNE
        oldBvhFile = open(sys.argv[i + 1], 'r')  # Will throw error if file DNE
        # Will override if file exists # TEMP

        newBvhFile = open(csvName.split('/')[-1] + '.bvh', 'w')

        # Write new file
        writeFromBvh(newBvhFile, oldBvhFile)  # TEMP
        writeFromCsv(newBvhFile, csvFile)

        # Close files
        newBvhFile.close()
        oldBvhFile.close()
        csvFile.close()
