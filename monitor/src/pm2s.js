const exec = require('child_process').exec;
const pm2s = {
  // 启动项目
  start: function (options) {
    exec("pm2 start ", function (error, stdout, stderr) {
      // 获取命令执行的输出
    });


    return new Promise(function (resolve, reject) {
      pm2.start(options, err => {
        if (err) {
          console.log(err);
          process.exit(0);
        }
        resolve();
      });
    });
  },
  // 保存
  dump: function () {
    return new Promise(function (resolve, reject) {
      pm2.dump(err => {
        if (err) {
          console.log(err);
          process.exit(0);
        }
        resolve();
      });
    });
  },
  // 开机启动
  startup: function () {
    return new Promise(function (resolve, reject) {
      pm2.connect(process.platform, err => {
        if (err) {
          console.log(err);
          process.exit(0);
        }
        resolve();
      });
    });
  }
};
module.exports = pm2s;
