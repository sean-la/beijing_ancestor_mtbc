import sys
import os
import getopt
import re

pattern = "[&height=(.+),height_95%_HPD={(.+),(.+)},height_median=(.+),height_range={(.+),(.+)},length=(.+),length_95%_HPD={(.+),(.+)},length_median=(.+),length_range={(.+),(.+)}]:(.+)"

helpMessage = "Reads three-way alignment MAF files and outputs another three-way MAF file without extended segments on reads and a second MAF file with only alignment between the reference and the extended segment of the read."
usageMessage = "[-h help and usage] [-i three-way MAF file] [-r reference FASTA] [-m unextended MAF output path] [-e extension segments MAF output path] [-p used PBSim]"

options = "hi:r:m:e:t"

try:
        opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
        print "Error: unable to read command line arguments."
        sys.exit(2)

if len(sys.argv) == 1:
        print usageMessage
        sys.exit(2)

mafInputPath = None
refPath = None
unextendedPath = None
extensionPath = None
usedPbsim = False

for opt, arg in opts:
        if opt == '-h':
                print helpMessage
                print usageMessage
                sys.exit()
        elif opt == '-i':
                mafInputPath = arg
        elif opt == '-r':
                refPath = arg
        elif opt == '-m':
                unextendedPath = arg
        elif opt == '-e':
                extensionPath = True
        elif opt == '-p':
                usedPbsim = True
        elif opt == '-t':
                test()
                sys.exit()

