#!/usr/bin/python
import platform
import sys
import os.path
import subprocess


def isPy2():
    return sys.version_info.major == 2


def isPy3():
    return sys.version_info.major == 3


def isLinux():
    name = platform.system()
    return name == 'Linux'


def isWindow():
    name = platform.system()
    return name == 'Windows'


def exists(file):
    return os.path.exists(file)


def mkdirs(file):
    if not exists(file):
        os.makedirs(file)


def execute(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout.readlines())
    for line in p.stdout.readlines():
        print(line),
    return p.wait()


def unTar(file, dir):
    execute("tar -zxvf " + file + " -C " + dir)


def cd(dir):
    execute("cd " + dir)


def setup(dest):
    execute('python ' + dest + '/setup.py install')


def loadConfig():
    # config path
    path = './conf/config.ini'
    if isPy3():
        import configparser
        config = configparser.ConfigParser()
        config.read(path)
        return config
    else:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config
