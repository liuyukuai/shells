# shells
shells




npm init
npm install webpack webpack-cli --save-dev
增加webpack.config.js文件，配置输入输出，重点制定target 运行环境为node

const path = require('path');

module.exports = {
  entry: './src/main.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  target: 'node' // 这是最关键的
};

"build":"webpack"
