import snp_sequences

numSamples = 9

sequences = snp_sequences.SnpSequences()

for index in range(numSamples+1):
	sequences.addSnp(index, index, "A", "G")

sequences.addSnp(3, 8, "A", "C") 
sequences.addSnp(4, 8, "A", "G")

for index in range(numSamples+1):
	print sequences.getSampleSeq(index)

print sequences.getRefSeq()
