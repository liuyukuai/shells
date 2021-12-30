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


def exists(s_file):
    return os.path.exists(s_file)


def mkdirs(s_file):
    if not exists(s_file):
        os.makedirs(s_file)


def execute(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout.readlines())
    for line in p.stdout.readlines():
        print(line),
    return p.wait()


def unTar(s_file, s_dir):
    execute("tar -zxvf " + s_file + " -C " + s_dir)


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
