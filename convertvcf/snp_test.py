import snp_sequences

snpSequences = snp_sequences.SnpSequences()

reference = "A A A A A A A A A A"

sample__1 = "A C A A A G A A G A"
sample__2 = "G A A A T A A C A A"
sample__3 = "A A T A A C A A A T"
sample__4 = "A A A G A A G A A A"

sample1name = "1"
sample2name = "2"
sample3name = "3"
sample4name = "4"

snp0 = (sample2name, 0, "A", "G") 
snp1 = (sample1name, 1, "A", "C") 
snp2 = (sample3name, 2, "A", "T") 
snp3 = (sample4name, 3, "A", "G") 
snp4 = (sample2name, 4, "A", "T") 
snp5 = (sample1name, 5, "A", "G") 
snp6 = (sample3name, 5, "A", "C") 
snp7 = (sample4name, 6, "A", "G") 
snp8 = (sample2name, 7, "A", "C") 
snp9 = (sample1name, 8, "A", "G") 
snp10 = (sample3name, 9, "A", "T") 

snps = [snp0, snp1, snp2, snp3, snp4, snp5, snp6, snp7, snp8, snp9, snp10]

for snp in snps:
	snpSequences.addSnp( snp[0], snp[1], snp[2], snp[3] )

sampleNames = [sample1name, sample2name, sample3name, sample4name]

sample1 = "ACAAAGAAGA"
sample2 = "GAAATAACAA"
sample3 = "AATAACAAAT"
sample4 = "AAAGAAGAAA"

samples = [sample1, sample2, sample3, sample4]

for i in range(4):
	print samples[i]
	print snpSequences.getSampleSeq(sampleNames[i])
	print
