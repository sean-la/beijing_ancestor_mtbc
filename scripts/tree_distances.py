from __future__ import division
import sys
import getopt
import dendropy
from dendropy.calculate import treecompare

def readNewick(path):
	'''
	Reads Newick file to retrieve tree. Assumes first tree in file is the
	target tree.
	Inputs
	- (string) path: path to the Newick file
	Returns
	- (string) tree: the tree in Newick format
	'''
	with open(path, 'r') as file:
		tree = file.read()
		tree = tree.rstrip()
	return tree

helpMessage = "Finds the Robinson-Foulds distance of the inputted trees."
usageMessage = "[-h help and usage] [-b BEAST Bayesian consensus tree path] [-m RAxML maximum likelihood tree path] [-n MEGA neighbor-joining tree path] [-o output file path]"

options = "hb:m:n:o:"

try:
        opts, args = getopt.getopt(sys.argv[1:], options)
except getopt.GetoptError:
        print "Error: unable to read command line arguments."
        sys.exit(2)

if len(sys.argv) == 1:
        print usageMessage
        sys.exit(2)

beastPath = None
raxmlPath = None
megaPath = None
outputPath = None

for opt, arg in opts:
        if opt == '-h':
		print helpMessage
		print usageMessage
		sys.exit()
	elif opt == '-b':
		beastPath = arg
	elif opt == '-m':
		raxmlPath = arg
	elif opt == '-n':
		megaPath = arg
	elif opt == '-o':
		outputPath = arg

optsIncomplete = False

if beastPath is None:
	optsIncomplete = True
	print "Please specify the path to the Bayesian consensus tree."
if raxmlPath is None:
	optsIncomplete = True
	print "Please specify the path to the RAxML maximum likelihood tree path."
if megaPath is None:
	optsIncomplete = True
	print "Please specify the path to the MEGA neighbor-joining tree path."
if outputPath is None:
	optsIncomplete = True
	print "Please specify the path to the output file."

if optsIncomplete:
	print usageMessage
	sys.exit(2)

# Get the trees from the input files
mlRawTree = readNewick(raxmlPath)
njRawTree = readNewick(megaPath)
bayesRawTree = readNewick(beastPath)

# Make the the taxon namespace is established
tns = dendropy.TaxonNamespace()

# Each tree should have the same taxon namespace
mlTree = dendropy.Tree.get(
		data=mlRawTree,
		schema='newick',
		taxon_namespace=tns)

njTree = dendropy.Tree.get(
		data=njRawTree,
		schema='newick',
		taxon_namespace=tns)

bayesTree = dendropy.Tree.get(
		data=bayesRawTree,
		schema='newick',
		taxon_namespace=tns)

treeList = dendropy.TreeList()
treeList.read(data=mlRawTree, schema="newick")
numTaxa = len( treeList.taxon_namespace )
maxDistance = (2*numTaxa)-6

with open(outputPath, 'w') as file:
	# Distance between ML and NJ
	distance = treecompare.symmetric_difference(mlTree, njTree)
	normalizedDistance = distance / maxDistance 

	result = "Distance between ML and NJ is %d, normalized distance is %f" % (distance, normalizedDistance)
	print result
	file.write(result)
	file.write('\n')

	# Distance between ML and Bayes
	distance = treecompare.symmetric_difference(mlTree, bayesTree)
	normalizedDistance = distance / maxDistance 

	result = "Distance between ML and Bayes is %d, normalized distance is %f" % (distance, normalizedDistance)
	print result
	file.write(result)
	file.write('\n')

	# Distance between NJ and Bayes
	distance = treecompare.symmetric_difference(njTree, bayesTree)
	normalizedDistance = distance / maxDistance 

	result = "Distance between NJ and Bayes is %d, normalized distance is %f" % (distance, normalizedDistance)
	print result
	file.write(result)
	file.write('\n')
