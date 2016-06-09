class NexusSequences(object):
	'''
	Contains sequences of the SNPs of the strains suitable for writing into NEXUS file for phylogenetic tree construction

	Inputs:
		genomeSize - The expected genome size of the samples. This number should be somewhat higher than
			the actual genome size of the samples to avoid overflow of the matrix.

		numSamples - The number of sample genomes i.e. from the Beijing lineage, excluding the reference genome.

	Methods:
		addSnp(strainNumber, snpPosition, refBase, sampleBase)
			Adds SNP

		getSequence(strainNumber)
			Returns a string of the sequence for the particular strain, ready to be written into a NEXUS file
	'''

	def __init__(self, genomeSize, numSamples):
		'''
		Initializes SNP sparse matrix and cleaned matrix with extra row for reference genome
		'''
		self.genomeSize = genomeSize

		# +1 to account for reference genome
		self.numStrains = numSamples + 1

		# Set which row will contain the reference sequence
		self.refRow = 0

		# Sparse matrix to hold SNPs
		# "*" is the placeholder character indicating an empty position in the matrix
		self.sparseMatrix = [ ["*" for i in xrange(genomeSize)] for u in xrange(self.numStrains) ]

		# Informally, cleanMatrix is sparseMatrix without columns of "*", and thus "cleaned"
		# Formally, cleanMatrix is defined as the matrix that contains all SNPs in sparseMatrix
		# in the other for which they appear
		self.cleanMatrix = [ [] for u in xrange(self.numStrains) ]

		# Member variable to check if cleanMatrix contains all SNPs of sparseMatrix.
		# Since no SNPs have been aded to sparseMatrix yet, cleanMatrix trivially contains all SNPs in sparseMatrix.
		self.matrixIsClean = True

	def addSnp(self, sampleNumber, snpPosition, refBase, sampleBase):
		'''
		Add SNP from sparse matrix
		'''
		# If the SNP position in the reference sequence is "*", then it follows that the SNP position in every
		# strain is "*" too, so we need to set the SNP position for every strain
		if self.sparseMatrix[self.refRow][snpPosition] == "*":
			for strainIndex in xrange(self.numStrains):
				if strainIndex != sampleNumber:
					self.sparseMatrix[strainIndex][snpPosition] = refBase
				elif strainIndex == sampleNumber:
					self.sparseMatrix[strainIndex][snpPosition] = sampleBase 
		# Otherwise, just change the base in the sample strain
		else:
			self.sparseMatrix[sampleNumber][snpPosition] = sampleBase

		# Since we added an SNP to sparseMatrix, cleanMatrix is not "clean"
		self.matrixIsClean = False
		
				
	def createCleanMatrix(self): 
		'''
		Add all SNPs of sparse matrix into clean matrix in order of appearance i.e. clean
		the sparse matrix
		'''
		self.cleanMatrix = [[base for base in self.sparseMatrix[strainIndex] if base is not "*"] 
					for strainIndex in xrange(self.numStrains)]

		# Since we've "cleaned" the matrix.
		self.matrixIsClean = True

	def getSequence(self, strainNumber):
		'''
		Returns the sequences of the SNPs of the inputted strain suitable for writing into NEXUS file 
		'''
		# Clean the matrix if not cleaned yet
		if not(self.matrixIsClean):
			self.createCleanMatrix()	
		
		# Get the sequence
		sequence = ''.join(self.cleanMatrix[strainNumber])

		return sequence	
	
	def printSparseMatrix(self):
		'''
		Print sparseMatrix for debugging purposes.
		'''
		for strainIndex in xrange(self.numStrains):
			for genomeIndex in xrange(self.genomeSize):
				print self.sparseMatrix[strainIndex][genomeIndex] + " ",
			print

