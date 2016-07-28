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

def getSampleNames(sampleListPath):
	'''
	Get the sample names. We assume the sample names are the names of the directories that
	contain the vcf files.
	'''
	sampleNames = []
	with open(sampleListPath, 'r') as file:
		for line in file:
			sampleNames.append( line.rstrip() )	
	return sampleNames

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

def writeNexus(output, sampleNames, snpSequences):
	'''
	Write the sequences into the nexus file.
	'''
	ntax = len(sampleNames)
	nchar = len(snpSequences.getRefSeq())

	file = open(output, 'w')

	file.write("#NEXUS\n")
	file.write("BEGIN DATA;\n")

	dimensions = "DIMENSIONS NTAX=%d NCHAR=%d;\n" % (ntax, nchar)
	file.write(dimensions)

	format = "FORMAT DATATYPE=DNA MISSING=? GAP=-;\n"
	file.write(format)

	file.write("MATRIX\n")
	
	for sampleName in sampleNames:
		sampleSeq = snpSequences.getSampleSeq(sampleName)
		sampleLine = "%s %s\n" % (sampleName, sampleSeq)
		file.write(sampleLine)

	file.write(";\n")
	file.write("END;\n")	
	file.close()

def writeFasta(output, sampleNames, snpSequences):
	'''
	Write the sequences into fasta file.
	'''
	with open(output, 'w') as file:
		for sampleName in sampleNames:
			header = ">%s\n" %(sampleName)
			sequence = "%s\n" %( snpSequences.getSampleSeq(sampleName) )
			file.write(header)
			file.write(sequence)

def writePhylip(output, sampleNames, snpSequences):
	'''
	Write the sequences into PHYLIP file.
	'''
	with open(output, 'w') as file:
		ntax = len(sampleNames)
		nchar = len(snpSequences.getRefSeq())
		header = "%d %d\n" % (ntax, nchar)
		file.write(header)

		for sampleName in sampleNames:
			line = "%s %s\n" % ( sampleName, snpSequences.getSampleSeq(sampleName) )
			file.write(line)

if __name__ == "__main__":
	# The recursion limit needs to be set higher so that the BST recursive algorithms can work.
	# Python only allows a maximum recursive depth of 1000, while the samples we are working with
	# have around 1200 SNPs. Once the binary search tree implementation is changed from a recursive 
	# to an iterative method, this won't be necessary.
	sys.setrecursionlimit(2000)

	options = "hi:o:s:r:fnp"

	help = "Convert VCF files to NEXUS, FASTA or PHYLIP format.\n You add more than one '-i' arguments at a time to specify multiple input directories."
	usage = "Usage: %s [-i input directory] [-o output prefix] [-s path to text file with list of strains] [-r VCF files regular expression] [-f fasta] [-n nexus] [-p phylip]" % (sys.argv[0])

	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
	except getopt.GetoptError:
		sys.exit(2)

	if (len(sys.argv) == 1):
		print usage	
		sys.exit()

	inputDirs = []
	output = 'vcf2nexus'
	regex = '(\d|\D)*.vcf$'
	fasta = False
	nexus = False
	phylip = False
	sampleListPath = None

	for opt, arg in opts:
		if opt == '-h':
			print help
			print usage
			print "Default: -o vcf2nexus -r (\d|\D)*.vcf$"
			sys.exit()
		elif opt == '-i':
			inputDirs.append(arg)
		elif opt == '-o':
			output = arg
		elif opt == '-r':
			regex = arg
		elif opt == '-f':
			fasta = True
		elif opt == '-n':
			nexus = True
		elif opt == '-p':
			phylip = True
		elif opt == '-s':
			sampleListPath = arg

	optsIncomplete = False

	if inputDirs == []:
		print "Please provide an input directory."
		optsIncomplete = True
	if not fasta and not nexus and not phylip:
		print "Please indicate the output file format: nexus, fasta, or phylip"
		optsIncomplete = True
	if sampleListPath is None:
		print "Please provide the path to the text file with the list of strains."
		optsIncomplete = True
	if optsIncomplete:
		print usage
		sys.exit(2)

	snpSequences = snp_sequences.SnpSequences()
	# First, find the sample names. We assume the sample names are the same as the names of the
	# directories.

	if len(inputDirs) == 1:
		print "User inputted %d directory" % ( len(inputDirs) )
	else:
		print "User inputted %d directories" % ( len(inputDirs) )
	
	sampleNames = getSampleNames(sampleListPath)

	print "Found %d sample names" % ( len(sampleNames) )
	print

	# Keep track of repeated samples in the directories.
	alreadyReadSamples = []
	repeatedSamplesExist = False
	repeatedSamples = []

	for inputDir in inputDirs:
		print "Input directory: %s" % (inputDir)

		for sampleName in sampleNames:
			if inputDir[-1] == "/":
				vcfDir = "%s%s" % (inputDir, sampleName)
			else:
				vcfDir = "%s/%s" % (inputDir, sampleName)

			# Find all the VCF file paths in the directories that match the regex.
			vcfPaths = getVcfPaths(vcfDir, regex)

			if len( vcfPaths ) > 0:
				if sampleName in alreadyReadSamples:
					print "Error: Sample %s has already been read!" % (sampleName)
					repeatedSampleExists = True
				else:
					alreadyReadSamples.append( sampleName )
					for vcfPath in vcfPaths:
						print "Reading file: %s" %(vcfPath)
						# Read and store the SNPs in the snp BST
						if not repeatedSamplesExist:
							readVcf(vcfPath, sampleName, snpSequences) 
			else:
				print "Error: Sample %s not found in input directory." % (sampleName)
		print

	if repeatedSamplesExist:
		print "Please ensure that all samples appear only once over all inputted directories."
		print "Exiting program..."
		sys.exit(2)

	# Finally, write the SNPs into the nexus file
	if nexus:
		print "Converting to NEXUS format."
		nexusOutput = "%s.nex" %(output)	
		writeNexus(nexusOutput, sampleNames, snpSequences)
	if fasta:
		print "Converting to FASTA format."
		fastaOutput = "%s.fasta" %(output)	
		writeFasta(fastaOutput, sampleNames, snpSequences)
	if phylip:
		print "Converting to PHYLIP format."
		output = "%s.phy" %(output)
		writePhylip(output, sampleNames, snpSequences)
