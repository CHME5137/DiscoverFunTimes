import os
import sys

import rmgpy
from rmgpy.molecule import Molecule
from rmgpy.reaction import Reaction
from rmgpy.species import Species
from rmgpy.data.kinetics import KineticsFamily, ReactionRecipe, KineticsDatabase
from rmgpy.data.rmg import RMGDatabase
from rmgpy.qm.main import QMCalculator
from rmgpy.qm.gaussian import GaussianTSB3LYP

if len(sys.argv)>1:
	i = int(sys.argv[-1])
elif os.getenv('SLURM_ARRAY_TASK_ID'):
	i = int(os.getenv('SLURM_ARRAY_TASK_ID'))
else:
	raise Exception("Specify a TS number!")

rxnFamiles = ['H_Abstraction', 'intra_H_migration']#,'Cl-Abstraction' ['intra_H_migration', 'R_Addition_MultipleBond', 'H_Abstraction', 'Disproportionation']

print 'Loading RMG Database ...'
rmgDatabase = RMGDatabase()
rmgDatabase.load(os.path.abspath(os.path.join(os.getenv('RMGpy'), '..', 'RMG-database', 'input')), kineticsFamilies=rxnFamiles, solvation=False)
print 'Finished loading RMG Database ...'
loadSpecies = rmgDatabase.kinetics.families[rxnFamiles[0]]
species_dict_file = 'RMG_Dictionary.txt'
species_dict = loadSpecies.getSpecies(species_dict_file)

file_object = open('mechanism.txt', 'r')
mechLines = file_object.readlines()

rxnList = []
gotit = []
for rxnFamily in rxnFamiles:
	for k, line in enumerate(mechLines):
		if '!{0}'.format(rxnFamily) in line:
			#for m in range(10):
			reaction = mechLines[k].split()[0]
				#if not reaction.startswith('!'):
					#break
			if reaction not in gotit:
				gotit.append(reaction)
				rxnList.append((rxnFamily, mechLines[k]))

import random
belindasNumber = 9
random.seed(belindasNumber)
randomList = random.sample(xrange(1,2982), 500)
RxnNumber = randomList[i-1]

print '*****'+str(RxnNumber)+'*****'
reactionTuple = rxnList[RxnNumber - 1]

rxnFamily, reactionLine = reactionTuple
rxnFormula = reactionLine.split()[0] #rxnFormula, A, n, Ea = reactionLine.split()
reactants, products = rxnFormula.split('=')
tooBig = False
if rxnFamily in ['H_Abstraction', 'Disproportionation', 'Cl-Abstraction']:
	rSpecies1, rSpecies2 = [species_dict[j] for j in reactants.split('+')]
	pSpecies1, pSpecies2 = [species_dict[j] for j in products.split('+')]
	if len(rSpecies1.molecule[0].atoms) + len(rSpecies2.molecule[0].atoms) >= 48:
		tooBig = True
	reactionList = []
    	if not tooBig:
		rSpecies1.generateResonanceIsomers()
		rSpecies2.generateResonanceIsomers()
		pSpecies1.generateResonanceIsomers()
		pSpecies2.generateResonanceIsomers()
		testReaction = Reaction(reactants=[rSpecies1, rSpecies2], products=[pSpecies1, pSpecies2], reversible=True)
		for moleculeA in rSpecies1.molecule:
	    		for moleculeB in rSpecies2.molecule:
	        		tempList = rmgDatabase.kinetics.generateReactionsFromFamilies([moleculeA, moleculeB], [], only_families=[rxnFamily])
				for rxn0 in tempList:
		    			reactionList.append(rxn0)

elif rxnFamily in ['intra_H_migration']:
	rSpecies = species_dict[reactants]
	pSpecies = species_dict[products]
	rSpecies.generateResonanceIsomers()
	pSpecies.generateResonanceIsomers()
	testReaction = Reaction(reactants=[rSpecies], products=[pSpecies], reversible=True)
	reactionList = []
	for moleculeA in rSpecies.molecule:
		tempList = rmgDatabase.kinetics.generateReactionsFromFamilies([moleculeA], [], only_families=[rxnFamily])
		for rxn0 in tempList:
			reactionList.append(rxn0)
elif rxnFamily in ['R_Addition_MultipleBond']:
	if '(+M)' in reactants:
		reactants = reactants.split('(+M)')[0]
		products = products.split('(+M)')[0]
	if len(reactants.split('+'))==2:
		rSpecies1, rSpecies2 = [species_dict[j] for j in reactants.split('+')]
		pSpecies = species_dict[products]
	else:
		rSpecies1, rSpecies2 = [species_dict[j] for j in products.split('+')]
		pSpecies = species_dict[reactants]
	rSpecies1.generateResonanceIsomers()
	rSpecies2.generateResonanceIsomers()
	pSpecies.generateResonanceIsomers()
	testReaction = Reaction(reactants=[rSpecies1, rSpecies2], products=[pSpecies], reversible=False)
	reactionList = []
	for moleculeA in rSpecies1.molecule:
		for moleculeB in rSpecies2.molecule:
			tempList = rmgDatabase.kinetics.generateReactionsFromFamilies([moleculeA, moleculeB], [], only_families=[rxnFamily])
			for rxn0 in tempList:
				reactionList.append(rxn0)
gotOne=False
for reaction in reactionList:
	# Check if any of the RMG proposed reactions matches the reaction in the mechanism
	if reaction.isIsomorphic(testReaction):
		# Now add the labeled atoms to the Molecule, and check all labels were added
		atLblsR = dict([(lbl[0], False) for lbl in reaction.labeledAtoms])
		atLblsP = dict([(lbl[0], False) for lbl in reaction.labeledAtoms])

		for reactant in reaction.reactants:
			reactant = reactant.molecule[0]
			reactant.clearLabeledAtoms()
			for atom in reactant.atoms:
				for atomLabel in reaction.labeledAtoms:
					if atom==atomLabel[1]:
						atom.label = atomLabel[0]
						atLblsR[atomLabel[0]] = True
		for product in reaction.products:
			product = product.molecule[0]
			product.clearLabeledAtoms()
			for atom in product.atoms:
				for atomLabel in reaction.labeledAtoms:
					if atom==atomLabel[1]:
						atom.label = atomLabel[0]
						atLblsP[atomLabel[0]] = True
		if all( atLblsR.values() ) and all( atLblsP.values() ):
			gotOne=True
			break

def calculate(reaction):
	rxnFamily = reaction.family.label
	tsDatabase = rmgDatabase.kinetics.families[rxnFamily].transitionStates
	reaction = qmCalc.getKineticData(reaction, tsDatabase)

	for files in os.listdir('./'):
		if files.startswith('core'):
			os.remove(files)

if not gotOne:
    if tooBig:
        print "Reaction was too big"
    else:
	print "No reactions found for reaction {4}: {0} + {1} = {2} + {3}".format(rSpecies1.molecule[0].toSMILES(), rSpecies2.molecule[0].toSMILES(), pSpecies1.molecule[0].toSMILES(), pSpecies2.molecule[0].toSMILES(), i)
else:
	qmCalc = QMCalculator(
									software='gaussian',
									method='m062x',
									fileStore='/gss_gpfs_scratch/cain.ja/QMfiles',
									scratchDirectory='/gss_gpfs_scratch/cain.ja/QMscratch',
									)
	calculate(reaction)
