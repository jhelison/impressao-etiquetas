def numToMoney(value):
    returnValue = ""
    valueSeparated = value.split(".")
    if len(valueSeparated) == 1:
        returnValue = "R$ " + valueSeparated[0] + ".00"
    else:
        if len(list(valueSeparated[1])) == 1:
            returnValue = "R$ " + valueSeparated[0] + "." + valueSeparated[1] + "0"
        else:
            returnValue = "R$ " + valueSeparated[0] + "." + valueSeparated[1]
    
    return returnValue
    
    
xs = ["20", "21.3", "24.55"]

for x in xs:
    print(numToMoney(x))