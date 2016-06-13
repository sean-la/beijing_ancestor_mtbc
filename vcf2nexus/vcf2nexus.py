import os, re, getopt
import sys
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
	'''
	Get the sample names. We assume the sample names are the names of the directories that
	contain the vcf files.
	'''
	return [x[1] for x in os.walk(dirName)][0]

def readVcf(vcfFilePath, sampleName, snpSequences):
	'''
	Read and store the SNPs from the vcf files to the SNP BST.
	'''
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
	'''
	Write the sequences into the nexus file.
	'''
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
	# The recursion limit needs to be set higher so that the BST recursive algorithms can work.
	# Python only allows a maximum recursive depth of 1000, while the samples we are working with
	# have around 1200 SNPs. Once the binary search tree implementation is changed from a recursive 
	# to an iterative method, this won't be necessary.
	sys.setrecursionlimit(2000)

	options = "hi:o:r:"

	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
	except getopt.GetoptError:
		sys.exit(2)

	if (len(sys.argv) == 1):
		print "Usage: %s [-i input directory] [-o output path] [-r VCF files regular expression]" % (sys.argv[0])
		sys.exit()

	inputDir = ''
	nexusPath = 'vcf2nexus.nex'
	regex = '(\d|\D)*.vcf$'

	for opt, arg in opts:
		if opt == '-h':
			print "Usage: %s [-i input directory] [-o output path] [-r VCF files regular expression]" % (sys.argv[0])
			print "Default: -o vcf2nexus.nex -r (\d|\D)*.vcf$"
			sys.exit()
		elif opt == '-i':
			inputDir = arg
		elif opt == '-o':
			nexusPath = arg
		elif opt == '-r':
			regex = arg

	if inputDir == '':
		print "Please provide an input directory."
		print "Usage: %s [-i input directory] [-o output path] [-r VCF files regular expression]" % (sys.argv[0])
		sys.exit()

	snpSequences = snp_sequences.SnpSequences()
	# First, find the sample names. We assume the sample names are the same as the names of the
	# directories.
	sampleNames = getSampleNames(inputDir)

	for sampleName in sampleNames:
		if inputDir[-1] == "/":
			vcfDir = "%s%s" % (inputDir, sampleName)
		else:
			vcfDir = "%s/%s" % (inputDir, sampleName)

		# Find all the VCF file paths in the directories that match the regex.
		vcfPaths = getVcfPaths(vcfDir, regex)

		for vcfPath in vcfPaths:
			# Read and store the SNPs in the snp BST
			readVcf(vcfPath, sampleName, snpSequences) 

	# Finally, write the SNPs into the nexus file
	writeNexus(nexusPath, sampleNames, snpSequences)
