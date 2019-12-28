import os
import platform
import json
from os.path import expanduser


def setUserConfig(userid, email, password):
    if platform.system()=='Linux':
        configFilePath = expanduser('~')+'/.config/configstore/'
        f = open(configFilePath+'info.json','w')
        data = {
            'userid':userid,
            'email':email,
            'password':password
        }
        data2 = json.dumps(data)
        f.write(data2)
        f.close()
def get(value):
    print(value)