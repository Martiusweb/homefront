'use strict'

const path = require('path')
const resolve = require('rollup-plugin-node-resolve')

// List of ignored/external dependencies (not to be added in the final js)
const external = []  // ex: ["popper.js"]
const globals = {}  // ex: {"popper.js": "Popper"}

const plugins = [
  // resolve imports from node_modules
  resolve({
      browser: true
  })
]

module.exports = {
  input: path.resolve(__dirname, 'theme/default/js/main.js'),
  output: {
    name: 'main',
    file: path.resolve(__dirname, 'output/theme/js/main.js'),
    format: 'umd',
    globals
  },
  external,
  plugins
}
