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
        hot: true,
        port: 7070
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
                use: [
                    {
                        loader: 'file-loader',
                    },
                ]
            },
            {
                test: /\.(gif|png|jpe?g)$/i,
                use: [
                    'file-loader',
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            bypassOnDebug: true, // webpack@1.x
                            disable: true, // webpack@2.x and newer
                        },
                    },
                ],
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
