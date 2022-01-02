#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os.path
import platform
import subprocess
import sys
import json

# execute dir
execute_dir = os.path.dirname(os.getcwd())

jar_dir = os.path.join(execute_dir, 'libs')
conf_dir = os.path.join(execute_dir, 'conf')
conf_file = os.path.join(conf_dir, 'app.ini')


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


def execute(command, std):
    if std:
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        return pipe.communicate()
    else:
        subprocess.call(command, shell=True)


def loadConfig():
    if isPy3():
        import configparser
        config = configparser.ConfigParser()
        config.read(conf_file)
        return config
    else:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(conf_file)
        return config


def getValue(config, selection, name, value):
    if config is None:
        return value
    if isPy3():
        import configparser
        try:
            return config.get(selection, name)
        except configparser.NoSectionError:
            return value
        except configparser.NoOptionError:
            return value
    if isPy2():
        import ConfigParser
        try:
            return config.get(selection, name)
        except ConfigParser.NoSectionError:
            return value
        except ConfigParser.NoOptionError:
            return value


def findJar():
    accepted_extensions = ["jar", "war"]
    files = [fn for fn in os.listdir(jar_dir) if fn.split(".")[-1] in accepted_extensions]
    if len(files) == 0:
        print('No any jar or war package files were found in ' + jar_dir + '.')
        sys.exit()
    else:
        return files[0]


def checkArgs(name, argv):
    size = len(argv)
    if size == 0:
        print("Usage: " + name + " {start|stop|status|restart}")
        sys.exit()


def checkCmd():
    pipe = subprocess.Popen("node -v", shell=True, stdout=subprocess.PIPE)
    ret = pipe.wait()
    if ret != 0:
        print('please install nodejs first.')
    pipe = subprocess.Popen("node -v", shell=True, stdout=subprocess.PIPE)
    ret = pipe.wait()
    if ret != 0:
        print('please install pm2 first. eg: npm install - g pm2')


def getName(config, jar):
    # app name
    last = jar.rindex("-")
    return getValue(config, "core", "name", jar[0:last])


def initJson(config, jar):
    # app name
    name = getName(config, jar)
    # jar path
    jar = os.path.join(jar_dir, findJar())
    # jvm options
    jvm_options = getValue(config, "core", "jvm.options", '-Xms2g -Xmx2g -Duser.timezone=GMT+8')
    # env
    r_env = '-Denv=' + getValue(config, "core", "env", 'uat')
    # max_restart
    max_restart = getValue(config, "core", "max_restart", '5')
    # min_uptime
    min_uptime = getValue(config, "core", "min_uptime", '60s')

    dict_json = {
        "name": name,
        "script": "java",
        "args": [
            "-jar"
        ],
        "max_restarts": max_restart,
        "min_uptime": min_uptime,
        "exec_mode": "fork",
        "error_file": os.path.join(execute_dir, 'error.log'),
        "out_file": os.path.join(execute_dir, 'info.log')
    }

    if len(jvm_options) != 0:
        options = jvm_options.split(" ")
        for opt in options:
            dict_json["args"].append(opt)

    # meta
    meta = getValue(config, "apollo", "meta", '')
    if len(meta) != 0:
        meta = '-Dapollo.meta=' + meta
        dict_json["args"].append(meta)

    # namespace
    namespaces = getValue(config, "apollo", "bootstrap.namespaces", '')
    if len(namespaces) != 0:
        namespaces = '-Dapollo.bootstrap.namespaces=' + namespaces
        dict_json["args"].append(namespaces)

    dict_json["args"].append(r_env)
    dict_json["args"].append(jar)
    json_file = os.path.join(conf_dir, name + '.json')

    with open(json_file, "w") as f:
        json.dump(dict_json, f)
    return json_file


def out(pipe):
    if pipe is not None:
        std, err = pipe
        if err is not None:
            print(str(err))
        if std is not None:
            print(str(std))


def _delete(name):
    del_command = "pm2 del " + name
    execute(del_command, True)


def _save():
    save_command = "pm2 save "
    execute(save_command, True)


def _start(json_file):
    start_command = "pm2 start " + json_file
    communicate = execute(start_command, False)
    out(communicate)


def _restart(name):
    start_command = "pm2 restart " + name
    communicate = execute(start_command, False)
    out(communicate)


def _status(name):
    status_command = "pm2 status " + name
    execute(status_command, False)


def _startup():
    if isLinux():
        startup_command = "pm2 startup"
        msg = execute(startup_command, True)[0].decode('utf-8')
        values = msg.split("\n")
        command = values[2].replace("sudo", "")
        execute(command, False)

    if isWindow():
        startup_command = "pm2-startup install "
        pipe = subprocess.Popen(startup_command, shell=True, stdout=subprocess.PIPE)
        ret = pipe.wait()
        if ret != 0:
            print('npm install pm2-windows-startup -g')
            print('pm2-startup install')


def _stop(name):
    stop_command = "pm2 stop " + name
    communicate = execute(stop_command, False)
    out(communicate)


def start(config, jar):
    name = getName(config, jar)
    _delete(name)
    json_file = initJson(config, jar)
    _start(json_file)
    _save()
    _startup()


def stop(config, jar):
    name = getName(config, jar)
    _stop(name)


def restart(config, jar):
    name = getName(config, jar)
    _restart(name)


def status(config, jar):
    name = getName(config, jar)
    _status(name)


def main(name, argv):
    checkCmd()
    checkArgs(name, argv)
    # jar
    jar = findJar()
    # load config
    config = loadConfig()
    action = argv[0]
    if action == 'start':
        start(config, jar)
    elif action == 'restart':
        restart(config, jar)
    elif action == 'stop':
        stop(config, jar)
    elif action == 'status':
        status(config, jar)
    else:
        print("Usage: " + name + " {start|stop|status|restart}")
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
