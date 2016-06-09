import nexus_sequences

genomeSize = 10
numSamples = 9

sequences = nexus_sequences.NexusSequences(genomeSize, numSamples)

for index in range(numSamples+1):
	if index % 2 == 0:
		sequences.addSnp(index, index, "A", "G")

sequences.addSnp(3, 8, "A", "C") 

sequences.printSparseMatrix()

for index in range(numSamples+1):
	print sequences.getSequence(index)
