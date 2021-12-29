#!/usr/bin/python
import platform
import sys


def isLinux():
    sys = platform.system()
    return sys == 'Linux'


def isWindow():
    sys = platform.system()
    return sys == 'Windows'


def loadConfig():
    path = './conf/config.properties'
    print('load')
    if (sys.version_info > (3, 0)):
        import configparser
        config = configparser.ConfigParser()
        config.read(path)
        return config
    else:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config
