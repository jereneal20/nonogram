#!/usr/bin/python
import os, sys, subprocess
from collections import deque
sys.path.insert(0, '../../cnf/cnf')

from Formula import Formula
import ConvertToCNF as CNF

sampleInput2 = "> & - p q & p > r q"
sampleInput = [6, [[2, 1],[ 1, 3], [1, 2], [3], [4], [1]],
			   6, [[1], [5], [2], [5], [2, 1], [2]]]
sampleInput3 = [2, [[2, 1, 2],[ 1, 3] ],
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

def enumerate(input, lineIndex, locationArr, recNum):
	if recNum == len(input[1][0])-1: #lineIndex #2
		if locationArr[recNum]+input[1][0][recNum] <= input[2]:
			print(locationArr)
		return

	min = locationArr[recNum] + input[1][0][recNum] + 1
	for iter in range(min,input[2]): # 0 ~ 5
		locationArr.append(iter)
		enumerate(input, lineIndex, locationArr, recNum+1)
		locationArr.pop()




def main(argv):
	# print(getInputFromUser())
	print(sampleInput)
	ar = [1,2,3]
	print(len(ar))

	locationArr = []
	for iter in range(sampleInput3[2]):
		locationArr.append(iter)
		enumerate(sampleInput3, 2, locationArr, 0)
		locationArr.pop()

	originalFormula = Formula(deque(sampleInput2.split()))
	print(originalFormula.formulaAsString())


if __name__ == "__main__":
	main(sys.argv[1:])