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

def findRobinsonFoulds(mlTree, njTree, bayesTree):
	treeList = dendropy.TreeList()
	treeList.read(data=mlRawTree, schema="newick")
	numTaxa = len( treeList.taxon_namespace )
	MaxDistance = (2*numTaxa)-6

	with open(outputPath, 'w') as file:
		# Distance between ML and NJ
		distance = treecompare.symmetric_difference(mlTree, njTree)
		normalizedDistance = distance / MaxDistance 

		result = "Distance between ML and NJ is %d, normalized distance is %f" % (distance, normalizedDistance)
		print result
		file.write(result)
		file.write('\n')

		# Distance between ML and Bayes
		distance = treecompare.symmetric_difference(mlTree, bayesTree)
		normalizedDistance = distance / MaxDistance 

		result = "Distance between ML and Bayes is %d, normalized distance is %f" % (distance, normalizedDistance)
		print result
		file.write(result)
		file.write('\n')

		# Distance between NJ and Bayes
		distance = treecompare.symmetric_difference(njTree, bayesTree)
		normalizedDistance = distance / MaxDistance 

		result = "Distance between NJ and Bayes is %d, normalized distance is %f" % (distance, normalizedDistance)
		print result
		file.write(result)
		file.write('\n')

def cladesExists(mlTree, bayesTree):
	clade1 = [551494, 552090, 552482, 553068, 551212, 552136, 
			551554, 552580, 552429, 551311, 553237, 551090]
	clade1MaxDistance = ( 2*len(clade1) )-6

	clade2 = [551556, 552358, 552939, 552493, 551821, 550778, 551944, 551804, 551360, 552907, 
			550658, 550782, 551167, 550984, 552130, 553139, 551293, 551159, 553098, 551879, 551201]
	clade2MaxDistance = ( 2*len(clade2) )-6

	clade1 = ["ERR%d" % (name) for name in clade1]
	clade2 = ["ERR%d" % (name) for name in clade2]

	mlClade1 = mlTree.extract_tree_with_taxa_labels(labels=clade1)
	bayesClade1 = bayesTree.extract_tree_with_taxa_labels(labels=clade1)

	if mlClade1 == bayesClade1:
		print "Clade 1 from ML tree exists in Bayes tree"
	else:
		print "Clade 1 from ML tree does not exist in Bayes tree"

	distance = treecompare.symmetric_difference(mlClade1, bayesClade1)
	normalizedDistance = distance / clade1MaxDistance 

	print "Normalized distance = %f" % (normalizedDistance)

	mlClade2 = mlTree.extract_tree_with_taxa_labels(labels=clade2)
	bayesClade2 = bayesTree.extract_tree_with_taxa_labels(labels=clade2)

	if mlClade2 == bayesClade2:
		print "Clade 2 from ML tree exists in Bayes tree"
	else:
		print "Clade 2 from ML tree does not exist in Bayes tree"

	distance = treecompare.symmetric_difference(mlClade2, bayesClade2)
	normalizedDistance = distance / clade2MaxDistance 

	print "Normalized distance = %f" % (normalizedDistance)


'''
options = "hb:m:n:o:s:"

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
strainsPath = None

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
	elif opt =='-s':
		strainsPath = arg

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

with open(strainsPath, 'r') as file:
	tns = []
	for line in file:
		line = line.rstrip('\n')
		tns.append(line)	

# Get the trees from the input files
mlRawTree = readNewick(raxmlPath)
njRawTree = readNewick(megaPath)
bayesRawTree = readNewick(beastPath)

# Make the taxon namespace established
tns = dendropy.TaxonNamespace(tns)

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


cladesExists(mlTree, bayesTree)
'''
tns = dendropy.TaxonNamespace(tns)

run7path = "/home/seanla/Projects/beijing_ancestor_mtbc/runs/run7/bayes/run7bayes.newick"
run7RawTree = readNewick(run7path)
run7Tree = dendropy.Tree.get(
		data=run7RawTree,
		schema='newick',
		taxon_namespace=tns)

run8path = "/home/seanla/Projects/beijing_ancestor_mtbc/runs/run8/bayes/run8bayes.newick"
run8RawTree = readNewick(run8path)
run8Tree = dendropy.Tree.get(
		data=run8RawTree,
		schema='newick',
		taxon_namespace=tns)

distance = treecompare.symmetric_difference(run7tree, run8tree)

treeList = dendropy.TreeList()
treeList.read(data=run7RawTree, schema="newick")
numTaxa = len( treeList.taxon_namespace )
MaxDistance = (2*numTaxa)-6

normalizedDistance = distance/maxDistance
print "Distance = %f" % (normalizedDistance)
