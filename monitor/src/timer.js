const exec = require('child_process').exec;
const axios = require('axios');
address = process.argv.splice(2);

function timer() {
  if (address.length <= 0) {
    console.error("please config monitor address.")
    return
  }

  exec("pms jlist", function (error, stdout, stderr) {
    if (error) {
      console.log(error);
      return;
    }

    if (stderr) {
      console.log(stderr);
      return;
    }
    axios.post(address[0])
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          console.log(err);
        });
  });
}

// 5秒执行一次
setInterval(timer, 5000);
