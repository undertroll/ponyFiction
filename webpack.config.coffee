path = require 'path'
webpack = require 'webpack'
{merge, keys} = require 'lodash'
pkginfo = require "./package.json"

debug = process.env.NODE_ENV != 'production'

module.exports =
  context: path.join __dirname, 'ponyFiction', 'frontend'
  cache: true

  entry:
    main: "./main"
    vendor: keys(pkginfo.dependencies)

  output:
    path: path.join __dirname, 'static'
    publicPath: 'static/'
    filename: '[name].bundle.js'

  module:
    loaders: [
      {test: /\.coffee$/, loader: 'coffee-loader'}
      {test: /\.styl$/, loader: "style-loader!css-loader!stylus-loader"}
      {test: /\.css$/, loader: 'style-loader!css-loader'}
    ]

  resolve:
    extensions: ['', '.webpack.js', '.web.js', '.coffee', '.js', '.styl']

  plugins: merge [
    new webpack.optimize.CommonsChunkPlugin name: 'common', chunks: ['main'], minChunks: Infinity
    new webpack.optimize.CommonsChunkPlugin name: 'vendor', minChunks: Infinity
  ], if debug then [] else [new webpack.optimize.UglifyJsPlugin()]