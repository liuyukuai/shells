// axios = require('axios');
// address = process.argv.splice(2);
// const pm2 = require('pm2');
//
// function timer() {
//   // if (address.length <= 0) {
//   //   console.error("please config monitor address.")
//   //   return
//   // }
//
//   const data = pm2.list(err => {
//   });
//
//   console.log(data);
//
//   // exec(cmd, function (error, stdout, stderr) {
//   //   if (error) {
//   //     console.log(error);
//   //     return;
//   //   }
//   //
//   //   if (stderr) {
//   //     console.log(stderr);
//   //     return;
//   //   }
//   //   axios.post(address[0])
//   //   .then(res => {
//   //     console.log(res)
//   //   })
//   //   .catch(err => {
//   //     console.log(err);
//   //   });
//   // });
// }
//
// function getIp() {
//   const interfaces = os.networkInterfaces();
//   for (const devName in interfaces) {
//     const iface = interfaces[devName];
//     for (let i = 0; i < iface.length; i++) {
//       const alias = iface[i];
//       if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
//         return alias.address;
//       }
//     }
//   }
// }
//
// // 5秒执行一次
// setInterval(timer, 5000);
