import path from "path"
import { Configuration } from "webpack-dev-server"

type Params = {
    PORT: number,
}

export function buildDevServer(params: Params):Configuration {
    const {PORT} = params
    return {
            port: PORT || 5000,
            open: true,
            historyApiFallback: true,
            hot: true,

        }
}