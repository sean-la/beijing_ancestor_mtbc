sampleFilename = "sample_list.txt"
redundantFileName = "redundant_samples.txt"
strainFilename = "strain_list.txt"
samples = 0
strains = 0

redundantStrains = []

with open(redundantFileName, 'r') as file:
	for line in file:
		redundantStrains.append( line.rstrip() )	

with open(sampleFilename, 'r') as input:
	with open(strainFilename, 'w') as output:
		for line in input:
			currentSample = line.rstrip()
			# If the current sample's ascension number is one more than the previous,
			# we assume that the current sample comes from the same strain.
			if currentSample not in redundantStrains:
				print "Keeping sample  %s" % (line)
				output.write(line)
				strains += 1
			else:
				print "Skipping sample %s" % (line)
			samples += 1

print "Number of strains: %d" %(strains)
print "Number of samples: %d" %(samples)
