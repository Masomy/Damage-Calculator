from __future__ import annotations

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
    """
    :param diceSize: Size of the dice
    :return: Returns the average value rolled on the dice
    """
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
    """
    Calculate the chance of each of the three outcomes, hit, crit, miss
    :param evasion: The number to exceed to have the effect hit
    :param hitBonus: What is added to the roll
    :param accuracy: How much accuracy the roll is being made with
    :param invisible: If the target is invisible. Reduces hit and crit chance in half.
    :return: Hit Chance[0], Crit Chance[1], Miss Chance[0]
    """
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
    """
    :param evasion: The number to exceed
    :param hitBonus: How much is added to the d20 roll
    :return: (hitChance, critChance, missChance)
    """
    # This is the number you need to roll equal to or above on the dice to crit
    critNumber = 20
    # This is the number you need to roll equal to or above to hit, but below the crit number.
    # Evasion is capped at 20 per rules of lancer
    evasion = 20 if evasion > critNumber else evasion

    # Adjust evasion and number needed on the dice to get a crit by its hit bonus
    evasion -= hitBonus
    critNumber -= hitBonus

    # Calculate based on the range of 1 to 20 if the value would crit, hit, or miss.
    # Checks for if it's possible to crit at all, or always crits, otherwise it calculates the normal crit range
    if critNumber > 20:
        critChance = 0
    elif critNumber < 1:
        critChance = 1
    else:
        critChance = (20 - critNumber + 1) / 20

    # Works through to calculate the hit chance
    if evasion < 1:
        hitChance = 1 - critChance
    elif evasion > 20:
        hitChance = 0
    else:
        hitChance = (critNumber - evasion) / 20

    #
    missChance = 1 - hitChance - critChance

    return hitChance, critChance, missChance


def calculateMaxOfD6(expectedValue: int, accuracy: int):
    """
    Rolls a number of d6 equal to the accuracy and takes the highest dice.
    :param expectedValue: The value to find the number of ways to calculate it
    :param accuracy: How many dice are being rolled
    :return: The probability of expectedValue occurring given accuracy d6 dice are rolled.
    """
    # Takes in a number of d6 and selects the highest 1
    # Takes in a positive value for expected value and accuracy.
    # Return chance
    if expectedValue > 7 or expectedValue < 1:
        return 0
    # Calculate percentage for something
    return (pow(expectedValue, accuracy) - pow(expectedValue - 1, accuracy)) / pow(6, accuracy)


# Damage functions.
# DamageList[numD3, numD6, avgDamage]

def addD6Dice(damageList: list, addedDice=1):
    """
    Adds d6 dice to the number of d6 dice
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param addedDice: The number of d6 dice being added
    :return: The updated damageList
    """
    damageList[1] += addedDice
    return damageList


def addD3Dice(damageList: list, addedDice=1):
    """
    Adds 1 d3 dice to the number of d3 dice
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param addedDice: The number of d3 dice being added
    :return: The updated damageList

    """
    damageList[0] += addedDice
    return damageList


def addD6Damage(damageList: list, addedDice=1):
    """
    Adds 1 d6 worth of damage to average damage
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param addedDice: The number of d6 dice worth of damage being added
    :return: The updated damageList
    """
    damageList[2] += addedDice * averageD6
    return damageList


def addD3Damage(damageList: list, addedDice=1):
    """
    Adds 1 d3 worth of damage to average damage
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param addedDice: The number of d3 dice worth of damage being added
    :return: The updated damageList
    """
    damageList[2] += addedDice * averageD3
    return damageList


def multD3Dice(damageList: list, diceMultiplier=2):
    """
    Multiplies the number of d3 dice by diceMultiplier
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param diceMultiplier: The number to multiply numD3 by
    :return: The updated damageList
    """
    damageList[0] *= diceMultiplier
    return damageList


def multD6Dice(damageList: list, diceMultiplier=2):
    """
    Multiplies the number of d6 dice by diceMultiplier
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param diceMultiplier: The number to multiply numD6 by
    :return: The updated damageList
    """
    damageList[1] *= diceMultiplier
    return damageList


def calculateStandardDamage(damageList: list, otherParam=0):
    """
    Converts all the current dice into average damage.
    Sets all the dice to 0 and calculates the damage based on its average damage
    :param damageList: The list of numD3, numD6, avgDamage being passed around in the crit functions
    :param otherParam: Param which does nothing to fit the generalCritFunctionArchetype
    :return: returns the updated damage list with 0, 0, avgDamage
    """
    # Converts any dice into their damage

    # Convert the d3 into damage
    damageList[2] += averageD3 * damageList[0]
    damageList[0] = 0

    # Convert the d6 into damage
    damageList[2] += averageD6 * damageList[1]
    damageList[1] = 0

    return damageList


# Functions meant specifically for critical hits

# Multiplies the damage by the multiplier
def critMultiplier(damageList: list, multiplier=2):
    """
    Multiplies avgDamage by the multiplier
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param multiplier: The number to multiply avgDamage by
    :return: The updated damageList
    """
    damageList[2] *= multiplier
    return damageList


# Converts the numDice to averageDamage based on the max function.
def calculateMaxFunction(damageList: list, otherParam=0):
    """
    Converts the number of dice into average damage by lancer's crit system
    Aka roll 2 times the number of dice and take the highest combination of dice.
    Ex: If an attack normally rolls 2d6, on a crit you would roll 4d6 and take the highest 2 dice.
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param otherParam: Param which does nothing to fit the generalCritFunctionArchetype
    :return: The updated damage list. 0, 0, avgDamage
    """
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
    """
    A general crit function that can take in any number of functions to apply to a crit function and goes through
    each of them calculating the avgDamage as it goes
    :param numD3: The number of D3 in the roll
    :param numD6: The number of D6 in the roll
    :param functionOrderingList: The list of functions to go through in order
    :param functionParameters: The parameters for the functions in the functionOrderingList
    :return: The average damage of the crit given the functions provided
    """
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


# Complete Crit Functions. They all take in numD3, and numD6. They all return averageCritDamage

# The normal player crit damage
def lancerCritAverageDamage(numD3: int, numD6: int):
    """
    The standard Lancer Crit function. Roll 2 times the dice and take highest.
    :param numD3: Number of D3 dice in the attack
    :param numD6: Number of D6 dice in the attack
    :return: The average crit damage
    """
    return generalCritFunction(numD3, numD6, functionOrderingList=[calculateMaxFunction],
                               functionParameters=[0])


# The player crit function with an additional d6 added on crit
def lancerCritCrackShotDamage(numD3: int, numD6: int):
    """
    A standard lancer crit but you add a d6 bonus damage before rolling damage
    :param numD3: Number of D3 in the attack
    :param numD6: Number of D6 in the attack
    :return: The average crit damage
    """
    return generalCritFunction(numD3, numD6, functionOrderingList=[addD6Dice, calculateMaxFunction],
                               functionParameters=[1, 0])


# The damage from a crit if its damage is treated like a standard hit
def lancerNoCritDamage(numD3: int, numD6: int):
    """
    Treats the crit damage like normal damage
    :param numD3: Number of D3 in the attack
    :param numD6: Number of D6 in the attack
    :return: The average hit damage
    """
    return generalCritFunction(numD3, numD6, functionOrderingList=[calculateStandardDamage],
                               functionParameters=[0])


# An enemy crit with deadly(added d6)
def lancerDeadlyEnemyCrit(numD3: int, numD6: int):
    """
    An enemy crit with deadly. You treat all damage like standard damage with an extra d6 bonus damage
    :param numD3: The number of D3 in the base attack
    :param numD6: The number of D6 in the base attack
    :return: The average damage
    """
    return generalCritFunction(numD3, numD6, functionOrderingList=[addD6Dice, calculateStandardDamage],
                               functionParameters=[1, 0])


def applyDamageOperations(avgDamage: float, baseDamage=0, armor=0, isAP=False, resistance=False, exposed=False):
    """
    Applies the standard lancer damage operations to the damage.
    :param avgDamage: The avgDamage of the dice
    :param baseDamage: The damage not tied to dice of the attack
    :param armor: The armor of the target
    :param isAP: If the attack ignores armor
    :param resistance: If the target is resistant
    :param exposed: If the target is exposed
    :return: The expected damage of the attack after damage operations
    """
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
    """
    Calculates the average damage given the conditions. Including which critFunction it wants to use
    :param hitCritValues: The hit, crit, and miss chance in a tuple
    :param numD3: The number of D3 in the attack
    :param numD6: The number of D6 in the attack
    :param baseDamage: The damage not tied to the dice roll of an attack
    :param reliable: The minimum damage of the attack even if it misses
    :param armor: How much armor the target has
    :param isAP: If the attack ignores armor
    :param resistance: If the target is resistant to the damage
    :param exposed: If the target is exposed
    :param critFunction: What type of crit the attack performs
    :return: The average damage given all of those conditions
    """
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
    averageMissDamage = 0
    averageMissDamage = applyDamageOperations(averageMissDamage, reliable, armor, isAP, resistance, exposed)
    averageMissDamage *= hitCritValues[2]

    totalAverageDamage = averageCritDamage + averageHitDamage + averageMissDamage
    # print(f"Total: {totalAverageDamage}\nHit: {averageHitDamage}
    # \nCrit: {averageCritDamage}\nMiss: {averageMissDamage}")
    return totalAverageDamage


"""
def chanceToStructure(hp=10, evasion=10, hitBonus=0, accuracy=0, numD3=0, numD6=1, baseDamage=0, armor=1,
                 critFunction=lancerCritAverageDamage, resistance=False, exposed=False):
    # The result will be P(hit) * P(hp <= damage) + P(crit) * P(hp <= damage)
    hitCritValues = calculateHitCritChance(evasion, hitBonus, accuracy)
    pass
"""


class Target:
    """
    A class representing a target to attack.

    Has an evasion, armor, if its resistant, exposed, or invisible
    As well as its HASE stats for the purposes of making saves
    """

    def __init__(self, evasion: int, armor: int, resistance=False, exposed=False, invisible=False, hull=0, systems=0,
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
        """
        Calculates the chance of an effect happening
        :param target: The number the target has to exceed to succeed the save
        :param accuracy: The number of accuracy rolled with the save
        :param hase: The stat the effect targets. 1 = hull, 2 = agi, 3 = sys, 4 = eng
        :return : The chance of an effect happening, aka the chance the target fails the save
        """
        # Hase stands for the 4 stats, 1 - hull, 2 - agi, 3 - sys, and 4 - eng.
        values = calculateHitCritChance(target, self.haseStats[hase], accuracy, self.invisible)
        return values[2]

    def compareAttacks(self, attack1: Attack, attack2: Attack):
        pass


class Attack:
    """
    An attack that can be performed

    It has a hitBonus added to the d20 in addition to a number of accuracy
    It has potential damage it can do in the form of D3, D6, base damage, and reliable
    It also has if the attack ignores armor, and what type of crit function it follows.
    """

    def __init__(self, hitBonus: int, accuracy: int, numD3: int, numD6: int, baseDamage: int, reliable: int,
                 isAP: False, critFunction=lancerCritAverageDamage):
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

    def accuracyRangeAgainstTarget(self, target: Target, accuracyRange=1):
        accuracyRanges = generateAccuracyRange(target.evasion, self.hitBonus, self.accuracy, target.invisible, accuracyRange)
        printAccuracyRange(accuracyRanges, self, target)


class Effect:
    """
    A class which represents an effect that can happen to a target.
    It has the chance of an effect happening depending on what is rolled.
    Additionally, it has an effect that will modify the target if it happens.
    """

    def __init__(self, effectsHit=False, effectsCrit=True, effectsMiss=False, ):
        self.hitChance = 1 if effectsHit else 0
        self.critChance = 1 if effectsCrit else 0
        self.missChance = 1 if effectsMiss else 0


class AttackGroup:
    """
    A group of attacks that happen one after the other
    """

    def __init__(self, *attacks: Attack):
        self.attacks = attacks

    def attackTarget(self, target: Target):
        pass


# Formatting and printing information functions
def calcDifferences(values1: list, values2: list):
    """
    Calculates the difference between two sets of 3 values
    :param values1: a list of 3 values
    :param values2: a list of 3 values to be subtracted from values1
    :return: A list with values1 - values2 for each item in the lists.
    """
    return values1[0] - values2[0], values1[1] - values2[1], values1[2] - values2[2]


def generateAccuracyRange(evasion=10, hitBonus=0, accuracy=0, invisible=False, accuracyRange=1):
    """
    Creates a range of hit values + or - difficulty/accuracy from the base accuracy level
    :param evasion: The target number to beat to hit
    :param hitBonus: The number added to the d20
    :param accuracy: The base accuracy of the attack
    :param invisible: If the target is invisible
    :param accuracyRange: How many difficulty and accuracy to go away from the base accuracy
    :return: A range of hit values from least accurate to most accurate
    """
    # Find the ranges to print out accuracy for
    accuracyRangeValues = []

    # Go from the bottom of the accuracy range -x, to the top of the accuracy range x
    for x in range(-1 * accuracyRange, accuracyRange + 1):
        accuracyRangeValues.append(calculateHitCritChance(evasion, hitBonus, accuracy + x, invisible))

    # Returns the list of hitCritValues
    return accuracyRangeValues


def formatWeaponStats(hitCritMissValues: list, damage=False, whiteSpace=0, percentage=True):
    """
    Formats hit crit miss values and damage into a nice looking format
    :param hitCritMissValues: The values representing hit chance, crit chance, miss chance
    :param damage: If it's an int it will add damage into its output
    :param whiteSpace: How much white space to put before the whole string of information
    :param percentage: To include it in percentage format or decimal format
    :return: A nicely formatted string with hit, crit, miss, and damage values
    """
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
    """
    Prints a header with hit, crit, and miss chance, and damage if included
    :param whiteSpace: How much white space to put before the header
    :param includeDamage: Weather to include damage in the header
    :return: None
    """
    returnString = " " * whiteSpace
    returnString += "Hit  Chance, Crit Chance, Miss Chance"
    if includeDamage:
        returnString += ", Average Damage"
    print(returnString)


def printAccuracyRange(accuracyValues: list, attack=None, target=None):
    """
    Takes in a list of hit crit miss values representing values from an accuracy range and prints them nicely
    :param accuracyValues: The list of hit crit miss values
    :param attack: An attack that is paired with the hit crit miss values
    :param target: A target to be attacked.
    :return: None
    """
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


# Main Code
displayDamage = True
currentTarget = Target(evasion=11, armor=1, resistance=False, exposed=False, invisible=False,
                       hull=4, agility=2, systems=0, engineering=0)

averageTier1Target = Target(evasion=9, armor=1, resistance=False, exposed=False, invisible=False,
                            hull=0, agility=0, systems=1, engineering=1)
averageTier2Target = Target(evasion=11, armor=1, resistance=False, exposed=False, invisible=False,
                            hull=1, agility=1, systems=2, engineering=2)
averageTier3Target = Target(evasion=12, armor=1, resistance=False, exposed=False, invisible=False,
                            hull=1, agility=2, systems=2, engineering=2)

currentWeapon = Attack(hitBonus=2, accuracy=0, numD3=0, numD6=0, baseDamage=9, reliable=0, isAP=False,
                       critFunction=lancerCritAverageDamage)

accuracyRanges = generateAccuracyRange(currentTarget.evasion, currentWeapon.hitBonus, currentWeapon.accuracy,
                                       invisible=currentTarget.invisible, accuracyRange=2)


currentWeapon.accuracyRangeAgainstTarget(averageTier2Target, 2)
stunChance = currentTarget.forceSaveChance(13, 0, 1)
print(f"Chance to fail the save: {stunChance*100: .3f}%\nOverall Chance to Stun: {stunChance * (1-accuracyRanges[1][2]) * 100: .3f}%")
