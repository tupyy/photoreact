const webpack = require('webpack');
const { BaseHrefWebpackPlugin } = require('base-href-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');
const path = require('path');

const utils = require('./utils.js');

const getTsLoaderRule = env => {
    const rules = [
        {
            loader: 'cache-loader',
            options: {
                cacheDirectory: path.resolve('target/cache-loader')
            }
        },
        {
            loader: 'thread-loader',
            options: {
                // There should be 1 cpu for the fork-ts-checker-webpack-plugin.
                // The value may need to be adjusted (e.g. to 1) in some CI environments,
                // as cpus() may report more cores than what are available to the build.
                workers: require('os').cpus().length - 1
            }
        },
        {
            loader: 'ts-loader',
            options: {
                transpileOnly: true,
                happyPackMode: true
            }
        }
    ];
    if (env === 'development') {
        rules.unshift({
            loader: 'react-hot-loader/webpack'
        });
    }
    return rules;
};

module.exports = options => ({
    cache: options.env !== 'production',
    resolve: {
        extensions: [
            '.js', '.jsx', '.ts', '.tsx', '.json'
        ],
        modules: ['node_modules'],
        alias: {
            app: utils.root('src')
        }
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: getTsLoaderRule(options.env),
                include: [utils.root('./src')],
                exclude: [utils.root('node_modules')]
            },
            {
                test: /\.(jpe?g|png|gif|svg|woff2?|ttf|eot)$/i,
                loader: 'file-loader',
                options: {
                    digest: 'hex',
                    hash: 'sha512',
                    name: 'content/[hash].[ext]'
                }
            },
            {
                enforce: 'pre',
                test: /\.jsx?$/,
                loader: 'source-map-loader'
            },
            {
                test: /\.tsx?$/,
                enforce: 'pre',
                loader: 'tslint-loader',
                exclude: [utils.root('node_modules')]
            }
        ]
    },
    stats: {
        children: false
    },
    optimization: {
        splitChunks: {
            cacheGroups: {
                commons: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    chunks: 'all'
                }
            }
        }
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: `'${options.env}'`,
                VERSION: `'${utils.parseVersion()}'`,
                DEBUG_INFO_ENABLED: options.env === 'development',
                SERVER_API_URL: `''`
            }
        }),
        new HtmlWebpackPlugin({
            template: "./src/index.html",
            'chunksSortMode': 'dependency',
            inject: 'body'
        }),
        new ForkTsCheckerWebpackPlugin({ tslint: true }),
        new CopyWebpackPlugin([
            { from: './static/', to: 'content' },
//      { from: './src/main/webapp/manifest.webapp', to: 'manifest.webapp' },
        ])
    ]
});
