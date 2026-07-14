import { Configuration, DefinePlugin } from 'webpack'

import HtmlWebpackPlugin from'html-webpack-plugin'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import ForkTsCheckerWebpackPlugin from 'fork-ts-checker-webpack-plugin'
import ReactRefreshWebpackPlugin from '@pmmmwh/react-refresh-webpack-plugin'

export function buildPlugins(html: string, platform: 'desktop' | 'mobile' = 'desktop', isDev: boolean):Configuration['plugins'] {
    return [
            new HtmlWebpackPlugin({template: html}),
            new MiniCssExtractPlugin({
                filename: 'css/[name].[contenthash:8].css',
                chunkFilename: 'css/[name].[contenthash:8].css',
            }),
            new DefinePlugin({
                __PLATFORM__: JSON.stringify(platform)
            }), isDev ? new ForkTsCheckerWebpackPlugin() : undefined,
            isDev ? new ReactRefreshWebpackPlugin() : undefined
        ]
}