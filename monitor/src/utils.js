const fs = require('fs');
const path = require('path');
const ini = require('ini');
const pm2s = require('./pm2s');

const utils = {

  isNull: function (v) {
    return v === null || v === undefined || v === '';
  },

  isEmpty: function (v) {
    return this.isNull(v) || v.length === 0;
  },

  parentDir: function () {
    return path.resolve(__dirname, "..");
  },

  jarDir: function () {
    return path.join(__dirname, "../libs");
  },

  configPath: function () {
    return path.join(__dirname, "../conf/app.ini");
  },


  findJar: function () {
    const files = fs.readdirSync(this.jarDir())
        .filter(e => {
          return e.endsWith('.war') || e.endsWith(".jar")
        });

    if (this.isEmpty(files)) {
      return null;
    }

    if (files.length > 1) {
      throw  new Error(" ");
    }

    return files[0];
  },

  getName: function (config, jar) {
    const index = jar.lastIndexOf("-");
    const name = jar.substring(0, index);
    return this.getValue(config, "core", "name", name)
  },


  loadConfig: function () {
    return ini.parse(fs.readFileSync(this.configPath(), 'utf-8'));
  },

  loadJavaOptions: function (config, jar) {
    const name = this.getName(config, jar);
    // jvm options
    const jvm_options = this.getValue(config, "core", "jvm.options", '-Xms2g -Xmx2g -Duser.timezone=GMT+8');
    // env
    const r_env = '-Denv=' + this.getValue(config, "core", "env", 'uat');
    // max_restart
    const max_restart = this.getValue(config, "core", "max_restart", '5');
    // min_uptime
    const min_uptime = this.getValue(config, "core", "min_uptime", '60s');
    const options = {
      "name": name,
      "script": "java",
      "args": [
        "-jar"
      ],
      "max_restarts": max_restart,
      "min_uptime": min_uptime,
      "exec_mode": "fork",
      "error_file": path.join(this.parentDir(), "logs/" + name + "-error.log"),
      "out_file": path.join(this.parentDir(), "logs/" + name + "-info.log")
    };

    if (!this.isEmpty(jvm_options)) {
      const opts = jvm_options.split(" ");
      opts.forEach(opt => {
        options.args.push(opt);
      })
    }

    // meta
    let meta = this.getValue(config, "apollo", "meta", '');
    if (!this.isNull(meta)) {
      meta = '-Dapollo.meta=' + meta;
      options.args.push(meta);
    }

    // namespace
    let namespaces = this.getValue(config, "apollo", "bootstrap.namespaces", '');
    if (!this.isNull(namespaces)) {
      namespaces = '-Dapollo.bootstrap.namespaces=' + namespaces;
      options.args.push(namespaces);
    }
    options.args.push(r_env);

    const jarPath = path.join(this.jarDir(), jar);
    options.args.push(jarPath);
    return options;
  },

  getValue: function (config, section, name, defaultValue) {

    if (this.isNull(config)) {
      return defaultValue;
    }
    const sectionValue = config[section];

    if (this.isNull(sectionValue)) {
      return defaultValue;
    }
    const value = sectionValue[name];

    if (this.isNull(value)) {
      return defaultValue;
    }
    return value;
  },
  start: function (config) {
    const jar = this.findJar();
    if (this.isEmpty(jar)) {
      console.log('No any jar or war package files were found in ' + this.findJar() + '.');
      return;
    }
    const options = this.loadJavaOptions(config, jar);
    pm2s.start(options)
        .then(() => {
          pm2s.dump()
              .then(() => {
                pm2s.startup();
              });
        });
  }
};

module.exports = utils;



