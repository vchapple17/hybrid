from protorpc import messages
import random

class DeviceModel(messages.Enum):
    LENOVO = 0
    IPAD_4TH = 1
    IPAD_AIR = 2
    IPAD_AIR2 = 3

def randomDeviceModelEnum():
    random.seed(0);
    v = random.randrange(0, 3)
    if v == 0:
        return DeviceModel.LENOVO
    elif v == 1:
        return DeviceModel.IPAD_4TH
    elif v == 2:
        return DeviceModel.IPAD_AIR
    elif v == 3:
        return DeviceModel.IPAD_AIR2

def randomDeviceModelEnumString():
    return getDeviceModelStringFromEnum(randomDeviceModelEnum())


def getDeviceModelStringFromEnum( item ):
    return str(item)

def getDeviceModelEnumFromString( _str ):
    if _str == str(DeviceModel.LENOVO):
        return DeviceModel.LENOVO
    elif _str == str(DeviceModel.IPAD_4TH):
        return DeviceModel.IPAD_4TH
    elif _str == str(DeviceModel.IPAD_AIR):
        return DeviceModel.IPAD_AIR
    elif _str == str(DeviceModel.IPAD_AIR2):
        return DeviceModel.IPAD_AIR2
    else:
        return None
