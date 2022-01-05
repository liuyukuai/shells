const exec = require('child_process').exec;
const axios = require('axios');
address = process.argv.splice(2);


const utils = {

  isNull: function (v) {
    return v === null || v === undefined || v === '';
  },

  isEmpty: function (v) {
    return this.isNull(v) || v.length === 0;
  }
};


function timer() {
  if (utils.isEmpty(address)) {
    console.error("please config monitor address.");
    return
  }

  exec("pm2 jlist", function (error, stdout, stderr) {
    if (error) {
      console.log(error);
      return;
    }

    if (stderr) {
      console.log(stderr);
      return;
    }
    axios.post(address[0], stdout)
        .then(res => {
          console.log(res.data)
        })
        .catch(err => {
          console.log(err);
        });
  });
}

// 5秒执行一次
setInterval(timer, 5000);

