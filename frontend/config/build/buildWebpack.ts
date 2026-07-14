import webpack from 'webpack'
import { Configuration } from 'webpack-dev-server'
import { buildPlugins } from './buildPlugins'
import { buildLoaders } from './buildLoaders'
import { buildDevServer } from './buildDevServer'
import type { EnvVariables } from '../../webpack.config'
import { platform } from 'node:os'

interface Options extends EnvVariables {
    isDev: boolean
    Paths: {
        entry: string,
        output: string,
        html: string,
        src: string
    }
}

export function buildWebpack(options: Options): webpack.Configuration {
    const {mode, PORT, platform, isDev, Paths} = options
    return {
        mode: mode ?? 'development',
        entry: Paths.entry,
        output: {
            path: Paths.output,
            filename: 'bundle.[contenthash].js',
            clean: true
        },
        plugins: buildPlugins(Paths.html, platform, isDev),
        module: {
            rules: buildLoaders(isDev),
        },
        resolve: {
            extensions: ['.tsx', '.ts', '.js'],
            alias: {
                '@': options.Paths.src,
             },
        },
        devtool: isDev ? 'inline-source-map' : false,
        devServer: buildDevServer({PORT}),
    }
}