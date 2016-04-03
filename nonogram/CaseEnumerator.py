locationArr = []
rowEnumerate = []
columnEnumerate = []

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

	return (rowEnumerate, columnEnumerate)
