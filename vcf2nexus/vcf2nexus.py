import os, re, getopt, sys
import snp_sequences

def getVcfPaths(inputDir, rePattern):
	'''
	Find all names of files in vcfPath that match regex pattern (rePattern)
	'''
	regex = re.compile(rePattern)

	vcfFilePathList = []
	
	for dirName, subdirList, fileList in os.walk(inputDir):
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
	file.close()

if __name__ == "__main__":
	options = "hi:o:r:"

	try:
		opts, args = getopt.getopt(argv, options)
	except getopt.GetoptError:
		sys.exit(2)

	inputDir = ''
	nexusPath = 'vcf2nexus.out'
	regex = ''

	for opt, arg in opts:
		if opt == '-h':
			print "Usage"
		elif opt == '-i':
			inputDir = arg
		elif opt == '-o':
			nexusPath = arg
		elif opt == '-r':
			regex = arg

	snpSequences = snp_sequences.SnpSequences()
	sampleNames = getSampleNames(inputDir)
	
	for sampleName in sampleNames:
		vcfDir = "%s/%s" % (inputDir, sampleName)
		vcfPaths = getVcfPaths(vcfDir, regex)

		for vcfPath in vcfPaths:
			readVcf(vcfPath, sampleName, snpSequences) 

	writeNexus(nexusPath, sampleNames, snpSequences)
