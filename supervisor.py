import utils

file = './libs/supervisor-4.2.3.tar.gz'
dest = '/supervisor-4.2.3'


def mkdirs(config):
    dir = config.get('supervisor', 'dir')
    if dir is None:
        dir = '/opt/supervisor'
    utils.mkdirs(dir)
    return dir;


def install():
    config = utils.loadConfig()
    dir = mkdirs(config)
    # tar -zxvf
    utils.unTar(file, dir)
    # install
    utils.setup(dir + dest)


install()
