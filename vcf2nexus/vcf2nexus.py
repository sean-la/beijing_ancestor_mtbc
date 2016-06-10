import os, re
import snp_sequences

def getVcfPaths(vcfPath, rePattern):
	'''
	Find all names of files in vcfPath that match regex pattern (rePattern)
	'''
	regex = re.compile(rePattern)

	vcfFilePathList = []
	
	for dirName, subdirList, fileList in os.walk(vcfPath):
		for filename in fileList:
			if regex.match(filename):
				vcfFilePath = "%s/%s" % ( str(dirName), str(filename) )
				vcfFilePathList.append(vcfFilePath)
	return vcfFilePathList

def getSampleNames(dirName):
	return [x[1] for x in os.walk(dirName)][0]

def readVcf(vcfFilePath, sampleName, snpSequences):
	file = open(vcfFilePath, 'r')

	for line in file:
		line = line.split()
		if len(line) > 0 and "#" not in line[0]:
			snpPosition = int(line[1])
			refBase = line[3]
			sampleBase = line[4]
			snpSequences.addSnp(sampleName, snpPosition, refBase, sampleBase)

	file.close()

def writeNexus(nexusPath, sampleNames, snpSequences):
	ntax = len(sampleNames) + 1
	nchar = len(snpSequences.getRefSeq())

	file = open(nexusPath, 'w')

	file.write("#NEXUS\n")
	file.write("Begin data;\n")

	dimensions = "Dimensions ntax=%d nchar=%d;\n" % (ntax, nchar)
	file.write(dimensions)

	format = "Format datatype=dna missing=? gap=-;\n"
	file.write(format)

	file.write("Matrix\n")
	
	refSeq = snpSequences.getRefSeq()
	referenceLine = "Reference   %s\n" % (refSeq)
	file.write(referenceLine)

	for sampleName in sampleNames:
		sampleSeq = snpSequences.getSampleSeq(sampleName)
		sampleLine = "%s   %s\n" % (sampleName, sampleSeq)
		file.write(sampleLine)

	file.write(";\n")
	file.write("End;\n")	

