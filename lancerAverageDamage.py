averageD3 = 2
averageD6 = 3.5

# Num d6, average crit value
averageD6CritTable = {
    # Calculated with bruteForceMaxFunction.py
    0: 0,
    1: 4.472222222222222,
    2: 9.344135802469136,
    3: 14.273791152263374,
    4: 19.222276996646855,
    5: 24.179310264303794,
    6: 29.141008834426703,
    # Calculated thanks to the website https://anydice.com/
    7: 34.11,
    8: 39.07,
    9: 44.04,
    10: 49.01
}

averageD3CritTable = {
    # Calculated with bruteForceMaxFunction.py
    0: 0,
    1: 2.4444444444444446,
    2: 5.086419753086419,
    3: 7.761316872427984,
    4: 10.445968602347202,
    5: 13.133329946315772,
    6: 15.82069129028434,
    7: 18.50692864620281,
    # Calculated thanks to the website https://anydice.com/
    8: 24.87,
    9: 25.81,
    10: 26.56
}


# Calculates the average of an evenly distributed dice
def calculateDiceAverage(diceSize=6):
    return (1 + diceSize) / 2


# Calculating HitCritMiss Functions
# Expected (10, 0, 0): .5, .05, .45
# Expected (0, 0, 0): .95, .05, 0
# Expected (20, 0, 0): 0, .05, .95
# Expected (10, 3, 0): .5, .20, .30
# Expected (0, 3, 0): .80, .25, 0
# Expected (20, 3, 0): 0, .20, .80
# Expected (10, 0, 1): .5, .175, .275
def calculateHitCritChance(evasion=10, hitBonus=0, accuracy=0, invisible=False):
    overallHitChance = 0
    overallCritChance = 0
    overallMissChance = 0

    if accuracy == 0:
        values = calculateD20Percentage(evasion, hitBonus)
        overallHitChance = values[0]
        overallCritChance = values[1]
        overallMissChance = values[2]
    elif accuracy != 0:
        for x in range(1, 7):
            sign = 1 if accuracy > 0 else -1
            accuracyChance = calculateMaxOfD6(x, abs(accuracy))
            values = calculateD20Percentage(evasion, hitBonus + (x * sign))
            overallHitChance += values[0] * accuracyChance
            overallCritChance += values[1] * accuracyChance
            overallMissChance += values[2] * accuracyChance

    if invisible:
        overallHitChance /= 2
        overallCritChance /= 2
        overallMissChance = 1 - overallHitChance - overallCritChance

    return overallHitChance, overallCritChance, overallMissChance


def calculateD20Percentage(evasion=10, hitBonus=0):
    # Returns (hitChance, critChance, missChance)
    # This is the critical hit number
    critNumber = 20
    # Evasion is capped at 20 per rules of lancer
    evasion = 20 if evasion > critNumber else evasion

    # Adjust evasion and number needed on the dice to get a crit by its hit bonus
    evasion -= hitBonus
    critNumber -= hitBonus
    # Calculate based on the range of 1 to 20 if the value would crit, hit, or miss.
    if critNumber > 20:
        critChance = 0
    elif critNumber < 1:
        critChance = 1
    else:
        critChance = (20 - critNumber + 1) / 20

    if evasion < 1:
        hitChance = 1 - critChance
    elif evasion > 20:
        hitChance = 0
    else:
        hitChance = (critNumber - evasion) / 20

    missChance = 1 - hitChance - critChance

    return hitChance, critChance, missChance


def calculateMaxOfD6(expectedValue, accuracy):
    # Takes in a number of d6 and selects the highest 1
    # Takes in a positive value for expected value and accuracy.
    # Return chance
    if expectedValue > 7 or expectedValue < 1:
        return 0
    # Calculate percentage for something
    return (pow(expectedValue, accuracy) - pow(expectedValue - 1, accuracy)) / pow(6, accuracy)


# Damage functions.
# DamageList[numD3, numD6, avgDamage]
# Multiplies the current average damage by 2

# Increases numD6 by addedDice
def addD6Dice(damageList, addedDice=1):
    damageList[1] += addedDice
    return damageList


# Increases numD3 by addedDice
def addD3Dice(damageList, addedDice=1):
    damageList[0] += addedDice
    return damageList


# Adds addedDice d6 damage directly to averageDamage
def addD6Damage(damageList, addedDice=1):
    damageList[2] += addedDice * averageD6
    return damageList


# Adds addedDice d3 damage directly to averageDamage
def addD3Damage(damageList, addedDice=1):
    damageList[2] += addedDice * averageD3
    return damageList


# Multiplies numD3 by Dice Multiplier
def multD3Dice(damageList, diceMultiplier=2):
    damageList[0] *= diceMultiplier
    return damageList


# Multiplies numD6 by Dice Multiplier
def multD6Dice(damageList, diceMultiplier=2):
    damageList[1] *= diceMultiplier
    return damageList


# Converts the numDice to averageDamage based on the normal function.
def calculateStandardDamage(damageList, otherParam=0):
    # Converts any dice into their damage

    # Convert the d3 into damage
    damageList[2] += averageD3 * damageList[0]
    damageList[0] = 0

    # Convert the d6 into damage
    damageList[2] += averageD6 * damageList[1]
    damageList[1] = 0

    return damageList


# Functions meant specifically for crits

# Multiplies the damage by the multiplier
def critMultiplier(damageList, multiplier=2):
    damageList[2] *= multiplier
    return damageList


# Converts the numDice to averageDamage based on the max function.
def calculateMaxFunction(damageList, otherParam=0):
    # takes the current number of dice and converts it to damage by rolling twice the number of dice and taking
    # the highest combination. Afterword it resets num dice to 0.

    # Calculate the d3 damage
    damageList[2] += averageD3CritTable[damageList[0]]
    damageList[0] = 0

    # Calculate the d6 damage
    damageList[2] += averageD6CritTable[damageList[1]]
    damageList[1] = 0

    return damageList


# A general function that takes in critChance, numDice, diceSize,
# and then you can add general functions with their params
def generalCritFunction(numD3: int, numD6: int, *, functionOrderingList: list, functionParameters: list):
    # Function Ordering List: A list of functions that all take in a list containing
    # numD3, numD6, currentAverageDamage, and a list of ints for function that need them, 0 for null functions.
    # It will then go through each function in order and modify the average damage and number of dice.
    # Each function should return a list with numD3, numD6, and currentAverageDamage.

    avgDamage = 0
    passedList = [numD3, numD6, avgDamage]
    if len(functionOrderingList) != len(functionParameters):
        # Does not work
        return 0

    for x in range(len(functionOrderingList)):
        # Update passed list with function(passedList, extra parameters)
        passedList = functionOrderingList[x](passedList, functionParameters[x])

    return passedList[2]


# Complete Crit Functions. They all take in critChance, numD3, and numD6. They all return averageCritDamage

# The normal player crit damage
def lancerCritAverageDamage(numD3, numD6):
    return generalCritFunction(numD3, numD6, functionOrderingList=[calculateMaxFunction],
                               functionParameters=[0])


# The player crit function with an additional d6 added on crit
def lancerCritCrackshotDamage(numD3, numD6):
    return generalCritFunction(numD3, numD6, functionOrderingList=[addD6Dice, calculateMaxFunction],
                               functionParameters=[1, 0])


# The damage from a crit if its damage is treated like a standard hit
def lancerNoCritDamage(numD3, numD6):
    return generalCritFunction(numD3, numD6, functionOrderingList=[calculateStandardDamage],
                               functionParameters=[0])


# An enemy crit with deadly(added d6)
def lancerDeadlyEnemyCrit(numD3, numD6):
    return generalCritFunction(numD3, numD6, functionOrderingList=[addD6Dice, calculateStandardDamage],
                               functionParameters=[1, 0])


def applyDamageOperations(avgDamage, baseDamage=0, armor=0, isAP=False, resistance=False, exposed=False):
    # Lancer damage operations:
    # Roll Damage,
    # Exposed,
    # Armor,
    # Resistance,
    # Final
    damage = avgDamage + baseDamage
    if exposed:
        damage *= 2
    if not isAP:
        damage -= armor
    if resistance:
        damage /= 2
    return max(0, damage)


def calculateAverageDamage(hitCritValues=(.5, .05, .45), numD3=0, numD6=1, baseDamage=0, reliable=0, armor=0,
                           isAP=False, resistance=False, exposed=False, critFunction=lancerCritAverageDamage):
    # Rolling to hit
    # hitCritValues = [hitChance, critChance, missChance]

    # Rolling Damage
    # Calculate the standard damage
    averageHitDamage = max(calculateStandardDamage([numD3, numD6, 0])[2], reliable)
    averageHitDamage = applyDamageOperations(averageHitDamage, baseDamage, armor, isAP, resistance, exposed)
    averageHitDamage *= hitCritValues[0]

    # Calculate the crit damage
    averageCritDamage = max(critFunction(numD3, numD6), reliable)
    averageCritDamage = applyDamageOperations(averageCritDamage, baseDamage, armor, isAP, resistance, exposed)
    averageCritDamage *= hitCritValues[1]

    # Calculate the miss damage
    averageMissDamage = applyDamageOperations(reliable, baseDamage, armor, isAP, resistance, exposed)
    averageMissDamage *= hitCritValues[2]

    totalAverageDamage = averageCritDamage + averageHitDamage + averageMissDamage
    return totalAverageDamage


"""
def chanceToStructure(hp=10, evasion=10, hitBonus=0, accuracy=0, numD3=0, numD6=1, baseDamage=0, armor=1,
                 critFunction=lancerCritAverageDamage, resistance=False, exposed=False):
    # The result will be P(hit) * P(hp <= damage) + P(crit) * P(hp <= damage)
    hitCritValues = calculateHitCritChance(evasion, hitBonus, accuracy)
    pass
"""


class Target:
    def __init__(self, evasion, armor, resistance=False, exposed=False, invisible=False, hull=0, systems=0,
                 engineering=0, agility=0):
        self.evasion = evasion
        self.armor = armor
        self.resistance = resistance
        self.exposed = exposed
        self.invisible = invisible
        self.hull = hull
        self.agility = agility
        self.systems = systems
        self.engineering = engineering
        self.haseStats = {
            1: self.hull,
            2: self.agility,
            3: self.systems,
            4: self.engineering
        }
        self.currentDifficulty = 0
        self.givenAccuracy = 0

    def forceSaveChance(self, target=10, accuracy=0, hase=1):
        # Hase stands for the 4 stats, 1 - hull, 2 - agi, 3 - sys, and 4 - eng.
        values = calculateHitCritChance(target, self.haseStats[hase], accuracy, self.invisible)
        return values[0] + values[1]


class Attack:
    def __init__(self, hitBonus, accuracy, numD3, numD6, baseDamage, reliable, isAP,
                 critFunction=lancerCritAverageDamage):
        self.hitBonus = hitBonus
        self.accuracy = accuracy
        self.numD3 = numD3
        self.numD6 = numD6
        self.baseDamage = baseDamage
        self.reliable = reliable
        self.isAP = isAP
        self.critFunction = critFunction

    def calculateDamage(self, target: Target, bonusAccuracy=0):
        hitValues = calculateHitCritChance(target.evasion, self.hitBonus, self.accuracy + bonusAccuracy,
                                           target.invisible)
        return calculateAverageDamage(hitValues, self.numD3, self.numD6, self.baseDamage, self.reliable, target.armor,
                                      self.isAP, target.resistance, target.exposed, self.critFunction)


class Effect:
    def __init__(self, effectsHit, effectsCrit, effectsMiss, ):
        pass


class AttackGroup:
    def __init__(self, *attacks: Attack):
        self.attacks = attacks

    def attackTarget(self, target: Target):
        pass


# Formatting and printing information functions
def calcDifferences(values1, values2):
    return values1[0] - values2[0], values1[1] - values2[1], values1[2] - values2[2]


def generateAccuracyRange(evasion=10, hitBonus=0, accuracy=0, invisible=False, accuracyRange=1):
    # Find the ranges to print out accuracy for
    accuracyRangeValues = []

    # Go from the bottom of the accuracy range -x, to the top of the accuracy range x
    for x in range(-1 * accuracyRange, accuracyRange + 1):
        accuracyRangeValues.append(calculateHitCritChance(evasion, hitBonus, accuracy + x, invisible))

    # Returns the list of hitCritValues
    return accuracyRangeValues


def formatWeaponStats(hitCritMissValues, damage=False, whiteSpace=0, percentage=True):
    returnString = ""
    returnString += " " * whiteSpace
    if percentage:
        returnString += f"{hitCritMissValues[0] * 100: 11.2f}%{hitCritMissValues[1] * 100: 11.2f}%{hitCritMissValues[2] * 100: 11.2f}%"
    else:
        returnString += f"{hitCritMissValues[0]: 12.3f}{hitCritMissValues[1]: 12.3f}{hitCritMissValues[2]: 12.3f}"

    if type(damage) == float:
        returnString += f"{damage: 12.3f}"

    return returnString


def printHeader(whiteSpace=15, includeDamage=False):
    returnString = " " * whiteSpace
    returnString += "Hit  Chance, Crit Chance, Miss Chance"
    if includeDamage:
        returnString += ", Average Damage"
    print(returnString)


def printAccuracyRange(accuracyValues: list, attack=None, target=None):
    accuracyRange = int((len(accuracyValues) - 1) / 2)

    if (target is None) or (attack is None):
        includeDamage = False
    else:
        includeDamage = True

    # Print out base values
    printHeader(includeDamage=includeDamage)
    if includeDamage:
        baseDamage = attack.calculateDamage(target)
    else:
        baseDamage = 0
    print(
        f"Base Values:{formatWeaponStats(accuracyValues[accuracyRange], damage=(baseDamage if includeDamage else includeDamage), whiteSpace=3)}")
    print("-" * (67 if includeDamage else 52))

    tracker = len(accuracyValues) - 1
    # start at the accuracy part of the list then go down to the difficulty part of the list
    for x in range(accuracyRange, -1 * accuracyRange - 1, -1):
        finalString = ""
        # If x is greater than 0 it is an accuracy
        if x > 0:
            finalString += f"Accuracy  "
        # if x is less than 0 it is a difficulty
        elif x < 0:
            finalString += f"Difficulty"
        # otherwise it is the bse value
        else:
            finalString += f"Base Value"

        finalString += f" + {abs(x)}:"

        # Tracker starts at the last list value, this is the accuracy values
        # Accuracy range itself should always be the base values
        # Prints Accuracy to Difficulty
        differences = calcDifferences(accuracyValues[tracker], accuracyValues[accuracyRange])
        if includeDamage:
            damageDifference = attack.calculateDamage(target, x) - baseDamage
        else:
            damageDifference = 0
        finalString += formatWeaponStats(differences, damage=(damageDifference if includeDamage else includeDamage))
        tracker -= 1
        print(finalString)


displayDamage = True
currentTarget = Target(evasion=10, armor=0, resistance=False, exposed=False, invisible=True)
currentWeapon = Attack(hitBonus=2, accuracy=1, numD3=1, numD6=0, baseDamage=0, reliable=0, isAP=False,
                       critFunction=lancerCritAverageDamage)

accuracyRanges = generateAccuracyRange(currentTarget.evasion, currentWeapon.hitBonus, currentWeapon.accuracy,
                                       invisible=currentTarget.invisible, accuracyRange=1)

if displayDamage:
    printAccuracyRange(accuracyRanges, currentWeapon, currentTarget)
else:
    printAccuracyRange(accuracyRanges)
