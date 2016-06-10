class Node(object):
	'''
	Class for implementation of binary search tree
	'''
	def __init__(self, data):
		'''
		Initializes data
		'''
		self.left = None
		self.right = None
		self.data = data
		self.positionKey = "POSITION"
		self.refBaseKey = "REFERENCE_BASE"

	def insert(self, data, sampleName): 
		'''
		Inserts data into binary tree. If the node with the given position already exists,
		then add data to the preexisting node.
		'''
		if self.data[self.positionKey] == data[self.positionKey]:
			# Insert new sample base into node
			self.data[sampleName] = data[sampleName]
		elif self.data[self.positionKey] > data[self.positionKey]:
			if self.left is None:
				self.left = Node(data)
			else:
				self.left.insert(data, sampleName)
		else:
			if self.right is None:
				self.right = Node(data)
			else:
				self.right.insert(data, sampleName)

	def getSampleSeq(self, sequence, sampleName):
		'''
		Find the SNP sequence of the given sample. If the sample has no SNP in the given
		position, then it is assumed that sample base is the same as the ref base.
		'''
		if self.left is not None:
			self.left.getSampleSeq(sequence, sampleName)

		if sampleName in self.data:
			sequence.append(self.data[sampleName])
		else:
			sequence.append(self.data[self.refBaseKey])

		if self.right is not None:
			self.right.getSampleSeq(sequence, sampleName)

	def getRefSeq(self, sequence):
		'''
		Find the SNP sequence for the reference.
		'''
		if self.left is not None:
			self.left.getRefSeq(sequence)

		sequence.append(self.data[self.refBaseKey])

		if self.right is not None:
			self.right.getRefSeq(sequence)
		
class SnpSequences(object):
	'''
	Contains sequences of the SNPs of the strains 

	Public Methods:
		addSnp(strainNumber, snpPosition, refBase, sampleBase)
			Adds SNP

		getSampleSeq(strainNumber)
			Returns a string of the sequence for the particular strain, ready to be written into a NEXUS file

		getRefSeq()
			Returns a string of the reference SNP sequence
	'''

	def __init__(self):
		'''
		Initialize data members.
		'''
		# Root of the BST to hold the sequences
		self.root = None
		# Keys to index node data dictionaries
		self.positionKey = "POSITION"
		self.refBaseKey = "REFERENCE_BASE"

	def addSnp(self, sampleName, snpPosition, refBase, sampleBase):
		'''
		Adds the SNP information to the binary search tree.
		TODO: Make this method non-recursive.
		'''
		# Initialize data in form of dictionary
		data = {}
		data[self.positionKey] = snpPosition
		data[self.refBaseKey] = refBase
		data[sampleName] = sampleBase
		# Put data into node

		if self.root is None:
			# If the root is empty, init the root
			node = Node(data)
			self.root = node
		else:
			# Otherwise, just add the data to the BST
			self.root.insert(data, sampleName)

	def getSampleSeq(self, sampleName):
		'''
		Returns the sequence of the SNPs of the inputted strain suitable for writing into NEXUS file 
		'''
		sequence = []
		if self.root is not None:
			self.root.getSampleSeq(sequence, sampleName)
		sequence = "".join(sequence)
		return sequence	

	def getRefSeq(self):	
		'''
		Returns the SNP sequence of the reference stran suitable for writing into NEXUS file
		'''
		sequence = []
		if self.root is not None:
			self.root.getRefSeq(sequence)
		sequence = "".join(sequence)
		return sequence
