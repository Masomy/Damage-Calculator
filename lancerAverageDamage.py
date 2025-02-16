from __future__ import annotations
from calculateAttackValues import calculateHitCritChance, generateAccuracyRange
from calculateDamage import *


# Calculates the average of an evenly distributed dice
def calculateDiceAverage(diceSize=6):
    """
    :param diceSize: Size of the dice
    :return: Returns the average value rolled on the dice
    """
    return (1 + diceSize) / 2


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
    Takes in 2 lists of ints of the same length and gives the differences between values1 and values2
    :param values1: a list of ints
    :param values2: a list of ints to be subtracted from values1
    :return: A list with values1 - values2 for each item in the lists.
    """
    if len(values1) != len(values2):
        return

    outputList = []
    for x in range(len(values1)):
        outputList.append(values1[x] - values2[x])

    return outputList


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

    for value in hitCritMissValues:
        if percentage:
            returnString += f"{value * 100: 11.2f}%"
        else:
            returnString += f"{value: 12.3f}"

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


def printDamageAccuracyRange():
    pass


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
