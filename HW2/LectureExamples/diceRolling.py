import random
import math
def rollDie():
    return random.choice([1, 2, 3, 4, 5, 6])

def testRoll(n=10):
    result = ''
    for i in range(n):
        result+=str(rollDie())
    print(result)

def runSim(goal, numTrials, txt):
    total = 0
    for i in range(numTrials):
        result = ''
        for j in range(len(goal)):
            result += str(rollDie())
        if result == goal:
            total += 1
    print('Actual probability of', txt, '=',
          round(1/(6**len(goal)), 8))
    estProbability = round(total/numTrials, 8)
    print('Estimated probability of', txt, '=',
          round(estProbability, 8))

def sameDate(numPeople, numSame):
    possibleDates = range(366)
    birthdays = [0]*366
    for p in range(numPeople):
        birthDate = random.choice(possibleDates)
        birthdays[birthDate]+=1
    return max(birthdays) >= numSame

def birthdayProb(numPeople, numSame, numTrials):
    numHits = 0
    for t in range(numTrials):
        if sameDate(numPeople, numSame):
            numHits+=1
    return numHits/numTrials

for numPeople in [10, 20, 40, 100]:
    print('For', numPeople, 'est. prob of a shared birthday is',
          birthdayProb(numPeople, 2, 10000))
    numerator = math.factorial(366)
    denom = (366**numPeople)*math.factorial(366-numPeople)
    print('Actual prob for N =', numPeople, '=', 1 - numerator/denom)