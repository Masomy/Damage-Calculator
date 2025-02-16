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


# Functions that modify the damage list
# DamageList[numD3, numD6, avgDamage]

# Normal Damage Functions
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


# Crit Damage Functions

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


def critMultiplier(damageList: list, multiplier=2):
    """
    Multiplies avgDamage by the multiplier
    :param damageList: numD3, numD6, avgDamage. This is the list being passed around by damage functions
    :param multiplier: The number to multiply avgDamage by
    :return: The updated damageList
    """
    damageList[2] *= multiplier
    return damageList


# Functions which convert dice into damage from the damageList

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


# Specific crit damage functions
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


# Applies the damage operations
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
    return max(0.0, damage)


def calculateHitCritMissDamage(numD3=0, numD6=1, baseDamage=0, reliable=0, armor=0,
                               isAP=False, resistance=False, exposed=False, critFunction=lancerCritAverageDamage):
    """
        Calculates the average damage given the conditions. Including which critFunction it wants to use
        :param numD3: The number of D3 in the attack
        :param numD6: The number of D6 in the attack
        :param baseDamage: The damage not tied to the dice roll of an attack
        :param reliable: The minimum damage of the attack even if it misses
        :param armor: How much armor the target has
        :param isAP: If the attack ignores armor
        :param resistance: If the target is resistant to the damage
        :param exposed: If the target is exposed
        :param critFunction: What type of crit the attack performs
        :return:
        """
    # Rolling Damage
    # Calculate the standard damage
    averageHitDamage = max(calculateStandardDamage([numD3, numD6, 0])[2], reliable)
    averageHitDamage = applyDamageOperations(averageHitDamage, baseDamage, armor, isAP, resistance, exposed)

    # Calculate the crit damage
    averageCritDamage = max(critFunction(numD3, numD6), reliable)
    averageCritDamage = applyDamageOperations(averageCritDamage, baseDamage, armor, isAP, resistance, exposed)

    # Calculate the miss damage
    averageMissDamage = 0
    averageMissDamage = applyDamageOperations(averageMissDamage, reliable, armor, isAP, resistance, exposed)

    return averageHitDamage, averageCritDamage, averageMissDamage


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
    damageValues = calculateHitCritMissDamage(numD3, numD6, baseDamage, reliable, armor, isAP, resistance, exposed,
                                              critFunction)

    # Bring all the damage together
    totalAverageDamage = damageValues[0] * hitCritValues[0]
    totalAverageDamage += damageValues[1] * hitCritValues[1]
    totalAverageDamage += damageValues[2] * hitCritValues[2]
    return totalAverageDamage
