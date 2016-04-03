import os, sys
from collections import deque
sys.path.insert(0, '../../cnf/cnf')

import ConvertToCNF as CNF
from Formula import Formula


def createCNF(input, enumerated):
	rowEnumerate = enumerated[0]
	columnEnumerate = enumerated[1]

	formulaDic = getDNFFormulaDic(input, rowEnumerate)
	formulaDic2 = getDNFFormulaDic(input, columnEnumerate)

	for iter in formulaDic2:
		formulaDic.append(iter)

	# print(formulaDic)

	return getCNFformEntireLine(formulaDic)


def getDNFFormulaDic(input, enumerates):
	oldVar = 0
	formulaDic = []
	formulaDic.append([])
	for iter in enumerates:
		dnfInput = formulateOneCase(input, iter)
		dnfForm = Formula(deque(dnfInput.split()))
		if iter[1] != oldVar:
			oldVar = iter[1]
			formulaDic.append([])
		formulaDic[oldVar].append(dnfForm)
	return formulaDic


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

	for j, k in zip(locArray[2], locArray[3]):
		for iter in range(numOfVar):
			if k <= iter and iter < j + k:
				lst[iter] = 1

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
