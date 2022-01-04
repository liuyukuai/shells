const utils = require('./utils');

function startup() {
  // 加载配置文件
  const config = utils.loadConfig();
  utils.start(config);
  utils.startMonitor();
}

startup();

