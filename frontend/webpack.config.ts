import webpack from 'webpack'
import HtmlWebpackPlugin from'html-webpack-plugin'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import path from 'path'
import { buildWebpack } from './config/build/buildWebpack'

export interface EnvVariables{
    mode: Mode
    PORT: number
    platform: 'desktop' | 'mobile'
}

type Mode = 'production' | 'development'

const Paths = {
    entry: path.resolve(__dirname, 'src', 'index.tsx'),
    output: path.resolve(__dirname, 'build'),
    html: path.resolve(__dirname, 'public', 'index.html'),
    src: path.resolve(__dirname, 'src')
}

export default (env: EnvVariables) => {
    const {mode, PORT, platform} = env
    const isDev = mode === 'development'
    const config: webpack.Configuration = buildWebpack({ mode, PORT, platform, isDev, Paths })
    
    return config;
}