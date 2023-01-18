const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const AutoDllPlugin = require('autodll-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
	entry: {
		bundle: path.resolve(__dirname, '../src/index.js')
	},
	output: {
		path: path.resolve(__dirname, '../dist'),
		filename: '[name].[hash].js'
	},
	resolve: {
		extensions: ['*', '.js', '.json', '.vue'],
		alias: {
			'vue$': 'vue/dist/vue.esm.js',
			'@': path.resolve(__dirname, '../src'),
		}
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				use: 'babel-loader',
				exclude: /node_modules/
			},
			{
				test: /\.css$/,
				use: ['vue-style-loader', 'css-loader']
			},
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,
              esModule: false
            }
          }
          ]
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        use: [{
            loader: 'url-loader',
            options: {
              limit: 10000,
              esModule: false
            }
          }]
      },
      {
				test: /\.vue$/,
				loader: 'vue-loader'
			}
		]
	},
	plugins: [
		new HtmlWebpackPlugin({
			template: path.resolve(__dirname, '../index.html')
		}),
		// Dll 优化，需要的时候可以打开
		// new AutoDllPlugin({
		// 	inject: true, // will inject the DLL bundle to index.html
		// 	debug: true,
		// 	filename: '[name]_[hash].js',
		// 	path: './dll',
		// 	entry: {
		// 	  vendor: ['vue', 'vue-router']
		// 	}
		// }),
		new VueLoaderPlugin(),
		// new webpack.optimize.SplitChunksPlugin()
	]
};
