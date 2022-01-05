const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './src/main.js',
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist')
  },
  target: 'node',
  // plugins: [
  //   new webpack.IgnorePlugin({resourceRegExp: /pty.js/, contextRegExp: /blessed\/lib\/widgets$/}),
  //   new webpack.IgnorePlugin({resourceRegExp: /term.js/, contextRegExp: /blessed\/lib\/widgets$/})
  // ],
  // module: {
  //   noParse: [path.join(__dirname, '/node_modules/pm2-deploy/deploy'),
  //     path.join(__dirname, '/node_modules/fsevents/fsevents.node'),
  //     path.join(__dirname, '/node_modules/terser/dist/bundle.min.js')
  //   ]
  // },
  // externals: {
  //   "blessed": "blessed"
  // },
};
