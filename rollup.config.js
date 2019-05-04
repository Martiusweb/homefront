'use strict'
// vim: ts=2 sw=2 et :

const path = require('path')
const resolve = require('rollup-plugin-node-resolve')

import { terser } from 'rollup-plugin-terser';

// List of ignored/external dependencies (not to be added in the final js)
const external = []  // ex: ["popper.js"]
const globals = {}  // ex: {"popper.js": "Popper"}


module.exports = {
  input: path.resolve(__dirname, 'theme/default/js/main.js'),
  output: {
    name: 'main',
    file: path.resolve(__dirname, 'output/theme/js/main.js'),
    format: 'umd',
    globals
  },
  external,
  plugins: [
    resolve({
      browser: true
    }),
    terser({
      sourcemap: true,
      compress: true,
      mangle: true
    }),
  ]
}
