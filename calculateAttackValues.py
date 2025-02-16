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
    if evasion <= 1:
        hitChance = 1 - critChance
    elif evasion > 20:
        hitChance = 0
    else:
        hitChance = (min(critNumber, 21) - evasion) / 20


    missChance = 1 - hitChance - critChance
    # print(f"Hit Chance: {hitChance}\tCrit Chance: {critChance}\tMiss Chance: {missChance}")
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
