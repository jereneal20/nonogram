#!/usr/bin/python
import os, sys, subprocess
from collections import deque
sys.path.insert(0, '../../cnf/cnf')
sys.path.insert(0, '../cnf/cnf')

from Formula import Formula
import ConvertToCNF as CNF
import MiniSATCaller as minisat
import CaseEnumerator
import FormulateCNF

sampleInput2 = "> & - p q & p > r q"
sampleInput = [6, [[2, 1],[ 1, 3], [1, 2], [3], [4], [1]],
			   6, [[1], [5], [2], [5], [2, 1], [2]]]
sampleInput3 = [2, [[2, 1, 2],[1, 3]],
			   10, [[1], [5], [2], [5], [2, 1], [2],[2], [5], [2, 1], [2]]]
sampleInput4 = [2, [[1, 3],[3]],
			   6, [[1], [1], [1], [2], [1], [1]]]
sampleInput5 = [2, [[2], [2]],
				3, [[1], [2], [1]]]
sampleInput6 = [2, [[2], [1]],
				3, [[1], [2], [0]]]
sampleInput7 = [10, [[3, 3], [1], [1], [5], [2], [2], [2], [2], [2], [2]],
				10, [[1], [1], [10], [7], [1], [1], [1], [1], [1], [1]]]



def getInputFromUser():
	numOfRows = int(input())
	numOfCols = int(input())
	rowInfo = []
	columnInfo = []
	for iter in range(numOfRows):
		intArr = []
		for token in input().split():
			intArr.append(int(token))
		rowInfo.append(intArr)

	for iter in range(numOfCols):
		intArr = []
		for token in input().split():
			intArr.append(int(token))
		columnInfo.append(intArr)

	return [numOfRows,rowInfo,numOfCols,columnInfo]


def getNonogramString(input, varDictionary):
	f = open("miniSAT.out", 'r')
	resultDic = minisat.getResultDictionary(f, varDictionary)
	# print(resultDic)
	lastString = ""
	for iter in range(input[0]):
		for iter2 in range(input[2]):
			if resultDic["a" + str(iter) + str(iter2)] == "1":
				lastString += "#"
			else:
				lastString += "."
		lastString += "\n"
	return lastString

def main(argv):
	# print(getInputFromUser())
	input = getInputFromUser()

	enumerated = CaseEnumerator.caseEnumaration(input)
	# print(enumerated[0])
	# print(enumerated[1])

	resultFormula = FormulateCNF.createCNF(input, enumerated)

	infix = resultFormula.formulaAsInfixString()
	varDictionary = minisat.createVarDictionary(resultFormula)
	miniSATStr = minisat.getMiniSATString(infix, varDictionary)
	minisat.getMiniSATResult(miniSATStr)

	lastString = getNonogramString(input, varDictionary)
	print(lastString)




if __name__ == "__main__":
	main(sys.argv[1:])