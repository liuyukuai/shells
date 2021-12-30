import utils

s_file = './libs/pm2.tar.gz'
dest = '/pm2'


def mkdirs(config):
    s_dir = config.get('pm2', 'dir')
    if s_dir is None:
        s_dir = '/opt/pm2'
    utils.mkdirs(s_dir)
    return s_dir


def install():
    config = utils.loadConfig()
    s_dir = mkdirs(config)
    # tar -zxvf
    utils.unTar(s_file, s_dir)

    # config


install()
