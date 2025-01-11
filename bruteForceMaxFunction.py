possibleValues = {}


class Counter:
    # Assume that all values are greater than or equal to 0
    # Smallest value(base range(maxCounterValue and startCounterValue)) to Largest Value
    def __init__(self, numCounters, maxCounterValue, startCounterValue=0):
        self.counterList = [startCounterValue for x in range(numCounters)]
        self.maxCounterValue = maxCounterValue
        self.startCounterValue = startCounterValue

    def increment(self):
        if self.isMaxed():
            return

        self.counterList[0] += 1
        for x in range(len(self.counterList)):
            if self.counterList[x] > self.maxCounterValue:
                try:
                    self.counterList[x+1] += 1
                    self.counterList[x] = self.startCounterValue
                except IndexError:
                    break

            else:
                break

    def takeHighestSum(self, numHighestCounters):
        numHighestCounters = min(numHighestCounters, len(self.counterList))
        values = sorted(self.counterList, reverse=True)
        total = 0
        for value in values[0:numHighestCounters]:
            total += value
        return total

    def printCounter(self, reverse=True, includeHighest=False, numHighest=1):
        items = self.counterList
        if reverse:
            items = reversed(items)
        outputStr = ""
        for value in items:
            outputStr += f"{value:4}, "

        if includeHighest:
            outputStr += f"{self.takeHighestSum(numHighest): 5}"
        print(outputStr)

    def isMaxed(self):
        for value in self.counterList:
            if value < self.maxCounterValue:
                return False
        return True


def calculateMaxCombinations(numDice, diceSize):
    return pow(diceSize, numDice)


def addToPossibleValues(givenCounter: Counter, numHighest=1):
    summedHighest = givenCounter.takeHighestSum(numHighest)
    if summedHighest in possibleValues:
        possibleValues[summedHighest] += 1
    else:
        possibleValues[summedHighest] = 1


def printValuesAndProbability(numDice, diceSize):
    maxCombinations = calculateMaxCombinations(numDice, diceSize)
    outputStr = "Values | Count | Chance\n"
    expectedValue = 0
    for value, count in possibleValues.items():
        outputStr += f"{value: <7}|{count:^7}|{count/maxCombinations*100:6.2f}%\n"
        expectedValue += value * (count/maxCombinations)
    outputStr += f"Expected Value: {expectedValue}"
    print(outputStr)
    return expectedValue


def displayHeaders():
    outputStr = ""
    for x in range(totalCounters):
        outputStr += f"C{x + 1:2}, "
    outputStr += "  Sum"
    print(outputStr)


numDice = 3
diceSize = 5
display = False

totalCounters = numDice * 2
counter = Counter(totalCounters, diceSize, 1)

if display:
    displayHeaders()
    counter.printCounter(includeHighest=False, numHighest=numDice)

addToPossibleValues(counter, numDice)

while not counter.isMaxed():
    counter.increment()

    if display:
        counter.printCounter(includeHighest=False, numHighest=numDice)

    addToPossibleValues(counter, numDice)

print()
printValuesAndProbability(totalCounters, diceSize)
print(calculateMaxCombinations(totalCounters, diceSize))
