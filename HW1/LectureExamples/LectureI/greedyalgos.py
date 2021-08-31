import value as value


class Food(object):
    def __init__(self, n, v, w):
        #initializes name, value, and calorie variables
        self.name = n
        self.value = v
        self.calories = w

    def getValue(self):
        #returns value variable
        return self.value

    def getCost(self):
        #returns calories variable
        return self.calories

    def density(self):
        #returns density--value/calories
        return self.getValue()/self.getCost()

    def __str__(self):
        #prints different elements
        return self.name + ': <' + str(self.value)\
            + ', ' + str(self.calories)

def buildMenu(names, values, calories):
    #initalizes empty menu
    menu = []
    #iterates through each item in food
    for i in range(len(values)):
        #adds each food name, value, and calories to the menu list
        menu.append(Food(names[i], values[i], calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    #sorts food menu by passed in key function
    itemsCopy = sorted(items, key = keyFunction, reverse=True)
    #initalizes result array as well as total value and cost variables
    result = []
    totalValue, totalCost = 0.0, 0.0
    #iterates through each item in the food menu
    for i in range(len(itemsCopy)):
        #if there is space for the food item it is added to the result list
        if (totalCost + itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            #total cost and value are adjusted to reflect the newly added item
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    #call to greedy function returning list of taken items and their combined value
    taken, val = greedy(items, constraint, keyFunction)
    #prints results of the function call
    print('Total value f items taken=', val)
    for item in taken:
        print('  ', item)

def testGreedys(foods, maxUnits):
    #test the greedy algorithm function on greedy by value, by cost, and by density using different key functions.
    print('Use greedy by value to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, lambda x: 1/Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.density)

names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories=[123,154,258,354,365,150,95,195]
foods = buildMenu(names, values, calories)
testGreedys(foods, 750)