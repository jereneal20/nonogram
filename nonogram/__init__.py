#!/usr/bin/python
import os, sys, subprocess
from collections import deque
sys.path.insert(0, '../../cnf/cnf')

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


def main(argv):
	# print(getInputFromUser())

	enumerated = CaseEnumerator.caseEnumaration(sampleInput)
	print(enumerated[0])
	print(enumerated[1])

	resultFormula = FormulateCNF.createCNF(sampleInput, enumerated)


	infix = resultFormula.formulaAsInfixString()
	varDictionary = minisat.createVarDictionary(resultFormula)
	miniSATStr = minisat.getMiniSATString(infix, varDictionary)
	print(minisat.getMiniSATResult(miniSATStr))


if __name__ == "__main__":
	main(sys.argv[1:])