sampleFilename = "sample_list.txt"
strainFilename = "strain_list.txt"
samples = 0
strains = 0

with open(sampleFilename, 'r') as input:
	with open(strainFilename, 'w') as output:
		previousSample = None
		for line in input:
			currentSample = int( line[3:].rstrip() )
			# If the current sample's ascension number is one more than the previous,
			# we assume that the current sample comes from the same strain.
			if previousSample is None or currentSample != previousSample + 1:
				print "Keeping sample  %s" % (line)
				output.write(line)
				strains += 1
			else:
				print "Skipping sample %s" % (line)
			previousSample = currentSample	
			samples += 1

print "Number of strains: %d" %(strains)
print "Number of samples: %d" %(samples)
