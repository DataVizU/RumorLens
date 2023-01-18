const merge = require("webpack-merge");
const path = require("path");
const baseConfig = require("./webpack.base.conf");

module.exports = merge(baseConfig, {
	mode: "development",
	devtool: "inline-source-map",
	module: {
		rules: [  // 自己拓展着玩呀
			// {
			// 	test: /\.css$/,
			// 	use: ["vue-style-loader", "css-loader", "postcss-loader"],
			// },
		],
	},
	devServer: {
		contentBase: path.resolve(__dirname, "src"),
		open: true,
    hot: true,
    // port: 3050,
    //use agency to get or post from other site
    proxy: {
            '/root': {
                target: 'http://backend.datavis.top:3000',
                pathRewrite: {
                    '^/root': ''
                }
            }
        }
	},
});
