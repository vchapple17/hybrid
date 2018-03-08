import random
import string
import calendar
from datetime import datetime

class ValidData():
    def __init__(self):
        random.seed(12)      # use time to change

    def validRandomString(self, max_length=255):
        data = ''.join([random.choice( string.ascii_letters + string.digits + string.punctuation + ' ') for n in xrange(random.randrange(max_length))])
        return data

    def validRandomDateString(self):
        # MM/DD/YY HH:MM
        year = random.randrange(1970,2500);
        month = random.randrange(1,13)
        thirty_days = [9, 4, 6, 11]
        thirty1_days = [1, 3, 5, 7, 8, 10, 12]

        if (calendar.isleap(year) and month == 2):
            day = random.randrange(1,29+1)
        elif (month == 2):
            day = random.randrange(1,28+1)
        elif month in thirty_days:
            day = random.randrange(1,30+1)
        elif month in thirty1_days:
            day = random.randrange(1,31+1)

        hour = random.randrange(0, 24)
        minute = random.randrange(0, 60)
        if (minute < 10):
            min_str = "0" + str(minute)
        else:
            min_str = str(minute)

        data = str(month) + "/" + str(day) + "/" + str(year) + " "
        data += str(hour) + ":" + min_str
        return data

    def validRandomDateTime(self):
        date_str = self.validRandomDateString()
        return datetime.strptime(date_str, "%m/%d/%Y %H:%M")

    def validRandomPositiveNum(self, max_num):
        data = random.randrange(max_num)
        return data


#
# v = ValidData()
#
# for i in range(100):
#     print(v.validRandomDateString())
