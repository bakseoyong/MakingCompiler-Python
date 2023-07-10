def getValueOfArray(object, index):
    #i = toNumber(index)
    #if i >= 0 and i < len(toArray(object).values):
    #    return toArray(object).values[i]
    #return NULL
    return object[index]

def getValueOfMap(object, index):
    return object[index]

def setValueOfArray(object, index, value):
    object[index] = value
    return object[index]

def setValueOfMap(object, key, value):
    object[key] = value
    return object[key]