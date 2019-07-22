const path = require('path');
const utils = require('./utils');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: [
        utils.root('src/webapp/index.js')
    ],
    resolve: {
        extensions: [".js", ".jsx", ".css"]
    },
    output: {
        filename: 'main.js',
        path: utils.root('dist')
    },
    devServer: {
        contentBase: './dist',
        hot: true
    },
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ],
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: "babel-loader"
            },
            {
                test: /\.svg$/,
                loader: 'babel-loader'
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: utils.root("public/index.html"),
            filename: "./index.html"
        })
    ]
};
