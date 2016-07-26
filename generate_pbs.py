import sys, getopt, os

def writeModelTest():
	jobPath = "%s/jmodeltest.pbs" % (jobsPath)
	with open(jobPath, 'w') as file:
		file.write("#!/bin/bash\n")

		jobName = "#PBS -N jmodeltest\n"
		file.write(jobName)
		
		email = "#PBS -M laseanl@sfu.ca\n"
		file.write(email)
		file.write("#PBS -m ea\n")

		epiloguePath = "#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n"
		file.write(epiloguePath)
		
		outputOnly = "#PBS -j oe\n"
		file.write(outputOnly)

		jobOutput = "#PBS -o %s/jmodeltest/jmodeltest-job.out\n"
		file.write(jobOutput)

		resources = ['walltime=1:00:00:00', 'mem=32gb', 'nodes=1:ppn=8']
		for resource in resources:
			line = "#PBS -l %s\n" % (resource)
			file.write(line)

		file.write('\n')

		runLine = "run=run%d\n" % (runNumber)
		file.write(runLine)

		prefixLine = "prefix=%s\n" % (outputPath)
		file.write(prefixLine)

		phylipLine = "phylip=$prefix/snps/$run.phy\n"
		file.write(phylipLine)

		jmodelDir = "jmodelDir=$prefix/jmodeltest\n"
		file.write(jmodelDir)

		output = "output=$jmodeldir/jmodeltest-results.out\n"
		file.write(output)

		jmodeltest = "jmodeltest=/home/seanla/Software/jmodeltest-2.1.10/jModelTest.jar\n\n"
		file.write(jmodeltest)

		mkdir = "mkdir -p $jmodeldir\n"
		file.write(mkdir)

		command = "java -jar $jmodeltest -tr ${PBS_NUM_PPN} -d $phylip -o $output -AIC -a -f -g 4 -i -H AIC\n"
		file.write(command)	

def writeMega():
	jobPath = "%s/mega.pbs" % (jobsPath)
	with open(jobPath, 'w') as file:
		file.write("#!/bin/bash\n")

		jobName = "#PBS -N mega\n"
		file.write(jobName)
		
		email = "#PBS -M laseanl@sfu.ca\n"
		file.write(email)
		file.write("#PBS -m ea\n")

		epiloguePath = "#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n"
		file.write(epiloguePath)
		
		outputOnly = "#PBS -j oe\n"
		file.write(outputOnly)

		jobOutput = "#PBS -o %s/nj/mega-nj.out\n"
		file.write(jobOutput)

		resources = ['walltime=1:00:00:00', 'mem=64gb', 'nodes=1:ppn=8']
		for resource in resources:
			line = "#PBS -l %s\n" % (resource)
			file.write(line)

		file.write('\n')

		runLine = "run=run%d\n" % (runNumber)
		file.write(runLine)

		prefixLine = "prefix=%s\n" % (outputPath)
		file.write(prefixLine)

		outputdir = "outputdir=$prefix/nj\n"
		file.write(outputdir)

		output = "output=$outputdir/${run}mega-nj\n"
		file.write(output)

		config = "config=$outputdir/infer_NJ_nucleotide.mao\n"
		file.write(config)

		input = "input=$prefix/snps/${run}.fasta\n"
		file.write(input)

		mega = "mega=/home/seanla/Software/mega/megacc\n\n"
		file.write(mega)

		mkdir = "mkdir -p $outputdir\n"
		file.write(mkdir)

		command = "$mega -a $config -d $input -o $output\n"
		file.write(command)	

def writeBeast():
	jobPath = "%s/beast.pbs" % (jobsPath)
	with open(jobPath, 'w') as file:
		file.write("#!/bin/bash\n")

		jobName = "#PBS -N beast\n"
		file.write(jobName)
		
		email = "#PBS -M laseanl@sfu.ca\n"
		file.write(email)
		file.write("#PBS -m ea\n")

		epiloguePath = "#PBS -l epilogue=/home/seanla/Jobs/epilogue.script\n"
		file.write(epiloguePath)
		
		outputOnly = "#PBS -j oe\n"
		file.write(outputOnly)

		jobOutput = "#PBS -o %s/bayes/beast.out\n"
		file.write(jobOutput)

		resources = ['walltime=1:00:00:00', 'mem=64gb', 'nodes=1:ppn=8']
		for resource in resources:
			line = "#PBS -l %s\n" % (resource)
			file.write(line)

		file.write('\n')

		runLine = "run=run%d\n" % (runNumber)
		file.write(runLine)

		prefixLine = "prefix=%s\n" % (outputPath)
		file.write(prefixLine)

		outputdir = "outputdir=$prefix/bayes\n"
		file.write(outputdir)

		output = "output=$outputdir\n"
		file.write(output)

		input = "input=$outputdir/${run}beast.xml\n\n"
		file.write(input)	

		mkdir = "mkdir -p $outputdir\n"
		file.write(mkdir)

		command = "beast -threads ${PBS_NUM_PPN} -prefix $output -overwrite -working $input\n"
		file.write(command)	

def writeRaxml():
	

helpMessage = "Generate PBS scripts for phylogenetic analysis."
usageMessage = "[-h help and usage] [-r run number]"

options = "hi:r:m:e:"

try:
        opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
        print "Error: unable to read command line arguments."
        sys.exit(2)

if len(sys.argv) == 1:
        print usageMessage
        sys.exit(2)

runNumber = None

for opt, arg in opts:
        if opt == '-h':
		print helpMessage
		print usageMessage
	if opt == '-r':
		runNumber = int(arg)

if runNumber is None:
	print "Please input the run number."
	print usageMessage
	sys.exit(2)

# Global - paths to scripts
jobsPath = "/home/seanla/Jobs/phylo/run%d" % (runNumber)
outputPath = "/home/seanla/Projects/beijing_ancestor_mtbc/run%d" % (runNumber)

#writeConvertVcf()
writeModelTest()
writeMega()
writeBeast()
writeRaxml()
