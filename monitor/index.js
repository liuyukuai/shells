axios = require('./axios');
address = process.argv.splice(2);
exec = require('child_process').exec;
cmd = 'pm2 jlist';

function timer() {
  console.log(address);
  if (address) {
    exec(cmd, function (error, stdout, stderr) {
      if (error) {
        console.log(error);
        return;
      }

      if (stderr) {
        console.log(stderr);
        return;
      }
      axios.post(address)
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(err);
          });
    });
  }
}

function getIp() {
  const interfaces = os.networkInterfaces();
  for (const devName in interfaces) {
    const iface = interfaces[devName];
    for (let i = 0; i < iface.length; i++) {
      const alias = iface[i];
      if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
        return alias.address;
      }
    }
  }
}

// 5秒执行一次
setInterval(timer, 5000);
