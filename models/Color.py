from protorpc import messages
import random

class Color(messages.Enum):
    SILVER = 0
    SPACE_GRAY = 1
    GOLD = 2
    ROSE_GOLD = 3

def randomColorEnum():
    random.seed(0);
    v = random.randrange(0, 3)
    if v == 0:
        return Color.SILVER
    elif v == 1:
        return Color.SPACE_GRAY
    elif v == 2:
        return Color.GOLD
    elif v == 3:
        return Color.ROSE_GOLD

def randomColorEnumString():
    return getColorStringFromEnum(randomColorEnum())


def getColorStringFromEnum( color ):
    return str(color)

def getColorEnumFromString( color_str ):
    if color_str == str(Color.SILVER):
        return Color.SILVER
    elif color_str == str(Color.SPACE_GRAY):
        return Color.SPACE_GRAY
    elif color_str == str(Color.GOLD):
        return Color.GOLD
    elif color_str == str(Color.ROSE_GOLD):
        return Color.ROSE_GOLD
    else:
        return None
