#!/usr/bin/python
import os, sys, subprocess
from collections import deque
sys.path.insert(0, '../../cnf/cnf')

from Formula import Formula
import ConvertToCNF as CNF
import MiniSATCaller as minisat
import CaseEnumerator

sampleInput2 = "> & - p q & p > r q"
sampleInput = [6, [[2, 1],[ 1, 3], [1, 2], [3], [4], [1]],
			   6, [[1], [5], [2], [5], [2, 1], [2]]]
sampleInput3 = [2, [[2, 1, 2],[ 1, 3] ],
			   10, [[1], [5], [2], [5], [2, 1], [2],[2], [5], [2, 1], [2]]]

locationArr = []
rowEnumerate = []
columnEnumerate = []

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

def enumerateCases(input, isRow, lineIndex, recNum):
	if isRow == True:
		if recNum == len(input[1][lineIndex])-1: #lineIndex #2
			if locationArr[recNum]+input[1][lineIndex][recNum] <= input[2]:
				rowEnumerate.append([1, lineIndex, input[1][lineIndex], locationArr.copy()])
			return

		min = locationArr[recNum] + input[1][lineIndex][recNum] + 1
		for iter in range(min,input[2]): # 0 ~ 5
			locationArr.append(iter)
			enumerateCases(input, isRow, lineIndex, recNum + 1)
			locationArr.pop()

	else:
		if recNum == len(input[3][lineIndex]) - 1:  # lineIndex #2
			if locationArr[recNum] + input[3][lineIndex][recNum] <= input[0]:
				columnEnumerate.append([3, lineIndex, input[3][lineIndex], locationArr.copy()])
			return

		min = locationArr[recNum] + input[3][lineIndex][recNum] + 1
		for iter in range(min, input[0]):  # 0 ~ 5
			locationArr.append(iter)
			enumerateCases(input, isRow, lineIndex, recNum + 1)
			locationArr.pop()

	return

def caseEnumaration(input):
	# Add the case 0

	for lineNum in range(input[0]):
		for iter in range(input[2]):
			locationArr.append(iter)
			enumerateCases(input, True, lineNum, 0)
			locationArr.pop()

	for lineNum in range(input[2]):
		for iter in range(input[0]):
			locationArr.append(iter)
			enumerateCases(input, False, lineNum, 0)
			locationArr.pop()


def formulateOneCase(input, locArray):

	dnfStr = ""
	numOfVar = 0
	if locArray[0] == 1:
		numOfVar = input[2]
	else:
		numOfVar = input[0]


	for iter in range(numOfVar-1):
		dnfStr += "& "
	lst = [0 for _ in range(numOfVar)]

	# for locIter in range(len(locArray[2])):
	# 	j = locArray[2][locIter]
	# 	k = locArray[3][locIter]
	for j, k in zip(locArray[2], locArray[3]):
		for iter in range(numOfVar):
			if k <= iter and iter < j + k:
				lst[iter] = 1
	# print(lst)
	iterNum = 0
	for isNot in lst:
		if locArray[0] == 1: # row
			if isNot == 1:
				dnfStr += "a"+str(locArray[1])+str(iterNum) +" "
			else:
				dnfStr += "- a" + str(locArray[1]) + str(iterNum) + " "
		else:
			if isNot == 1:
				dnfStr += "a" + str(iterNum)+ str(locArray[1]) +" "
			else:
				dnfStr += "- a" + str(iterNum) + str(locArray[1]) + " "
		iterNum += 1

	# print(dnfStr)
	return dnfStr

def getDNFFormulaDic(enumerates):
	oldVar = 0
	formulaDic = []
	formulaDic.append([])
	for iter in enumerates:
		dnfInput = formulateOneCase(sampleInput, iter)
		dnfForm = Formula(deque(dnfInput.split()))
		if iter[1] != oldVar:
			oldVar = iter[1]
			formulaDic.append([])
		formulaDic[oldVar].append(dnfForm)
	return formulaDic

def main(argv):
	# print(getInputFromUser())

	caseEnumaration(sampleInput)
	print(rowEnumerate)
	print(columnEnumerate)

	formulaDic = getDNFFormulaDic(rowEnumerate)
	formulaDic2 = getDNFFormulaDic(columnEnumerate)

	for iter in formulaDic2:
		formulaDic.append(iter)

	print(formulaDic)


	resultFormula = getCNFformEntireLine(formulaDic)


	infix = resultFormula.formulaAsInfixString()
	varDictionary = minisat.createVarDictionary(resultFormula)
	miniSATStr = minisat.getMiniSATString(infix, varDictionary)
	print(minisat.getMiniSATResult(miniSATStr))

	originalFormula = Formula(deque(sampleInput2.split()))
	print(originalFormula.formulaAsString())

def getCNFformOneLine(formulaList):
	masterFormula = formulaList[0]
	for iter in formulaList:
		if iter != masterFormula:
			masterFormula = CNF.wrapBinFormula("|", masterFormula, iter)
	return CNF.conjunctiveNormalForm(masterFormula)

def getCNFformEntireLine(formulaDic):
	cnfFormList = []
	for iter in formulaDic:
		oneLineFormula = getCNFformOneLine(iter)
		cnfFormList.append(oneLineFormula)
	print(cnfFormList)

	masterFormula = cnfFormList[0]
	for iter in cnfFormList:
		if iter != masterFormula:
			masterFormula = CNF.wrapBinFormula("&", masterFormula, iter)
	return masterFormula

if __name__ == "__main__":
	main(sys.argv[1:])