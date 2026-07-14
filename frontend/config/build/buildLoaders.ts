import ReactRefreshTypeScript from 'react-refresh-typescript'
import MiniCssExtractPlugin from "mini-css-extract-plugin"
import { ModuleOptions } from "webpack"
export function buildLoaders(isDev: boolean):ModuleOptions['rules'] {
    return [
        {
            test:/\.module.s[ac]ss$/i,
            use: [
                MiniCssExtractPlugin.loader,
                    {
                    loader: 'css-loader',
                    options: {
                        modules: {
                            localIdentName: '[name]__[local]--[hash:base64:5]',
                            exportLocalsConvention: 'camelCase',
                            namedExport: false,
                        },
                        esModule: true
                    }
                    },
                'sass-loader'
            ],
        },
        {
            test:/\.css$/i,
            use:[MiniCssExtractPlugin.loader, 'css-loader']
        },
        {
            test: /\.tsx?$/,
            use: {
                loader: 'ts-loader',
                options: {
                    transpileOnly: true,
                    getCustomTransformers: () => ({
                        before: [isDev && ReactRefreshTypeScript()].filter(Boolean)
                    })
                }
            },
            exclude: /node_modules/,
        },
        {
            test: /\.(png|jpg|jpeg|gif)$/i,
            type: 'asset/resource',
        },
        {
            test: /\.svg$/i,
            use: [
                {
                    loader: '@svgr/webpack', options: {
                        icon: true,
                        dimensions: false,
                        svgoConfig: {
                            name: 'convertColors',
                            params: {
                                currentColor: true
                            }
                        }
                    }
                }
            ],
        }
    ]
}