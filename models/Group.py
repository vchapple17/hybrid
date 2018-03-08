from protorpc import messages
import random

class Group(messages.Enum):
    STAFF = 0
    CLASS_2018 = 2018
    CLASS_2019 = 2019
    CLASS_2020 = 2020
    CLASS_2021 = 2021



def randomGroupEnum():
    random.seed(0);
    v = random.randrange(2017, 2021)
    if v == 2017:
        return Group.STAFF
    elif v == 2018:
        return Group.CLASS_2018
    elif v == 2019:
        return Group.CLASS_2019
    elif v == 2020:
        return Group.CLASS_2020
    elif v == 2021:
        return Group.CLASS_2021

def randomGroupEnumString():
    return getGroupStringFromEnum(randomGroupEnum())


def getGroupStringFromEnum( group ):
    return str(group)

def getGroupEnumFromString( group_str ):
    if group_str == "STAFF":
        return Group.STAFF
    elif group_str == "CLASS_2018":
        return Group.CLASS_2018
    elif group_str == "CLASS_2019":
        return Group.CLASS_2019
    elif group_str == "CLASS_2020":
        return Group.CLASS_2020
    elif group_str == "CLASS_2021":
        return Group.CLASS_2021
    else:
        return None
