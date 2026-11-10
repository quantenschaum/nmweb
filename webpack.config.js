const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
// const {GenerateSW} = require('workbox-webpack-plugin');
const fs = require("fs");

module.exports = (env, argv) => {
  const prod = argv.mode === "production";

  return {
    entry: "./src/main.js",
    resolve: {
      alias: {
        // svelte: path.resolve(__dirname, "node_modules", "svelte/src"),
        svelte: path.dirname(require.resolve("svelte/package.json")),
      },
      extensions: [".mjs", ".js", ".svelte"],
      mainFields: ["svelte", "browser", "module", "main"],
      // conditionNames: ["svelte", "browser", "module", "main"],
    },
    devtool: "source-map",
    output: {
      path: path.resolve(__dirname, "dist"),
      filename: "bundle.js",
      // filename: prod ? 'bundle.[contenthash].js' : 'bundle.js',
      clean: true,
    },
    module: {
      rules: [
        // {test: /\.css$/, use: ['style-loader', 'css-loader']},
        // {test: /\.css$/, use: [MiniCssExtractPlugin.loader, 'css-loader']},
        {
          test: /\.less$/,
          use: [MiniCssExtractPlugin.loader, "css-loader", "less-loader"],
        },
        {
          test: /\.scss/,
          use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
        },
        {
          test: /\.css$/,
          use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
        },
        {
          test: /\.(json|png|jpe?g|gif|webp|svg|ico)$/,
          type: "asset/resource",
          generator: { filename: "[name][ext]" },
        },
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options: { presets: ["@babel/preset-env"] },
          },
        },
        {
          test: /\.svelte/,
          use: {
            loader: "svelte-loader",
            // options: {
            // compilerOptions: { dev: !prod },
            // emitCss: prod,
            // hotReload: !prod,
            // },
          },
        },
      ],
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: "./src/index.html",
        filename: "index.html",
      }),
      new MiniCssExtractPlugin({
        filename: "style.css",
        // filename: prod ? 'style.[contenthash].css' : 'style.css',
      }),
      // new GenerateSW({
      //   mode: prod ? 'production' : 'development',
      //   clientsClaim: true,
      //   skipWaiting: true,
      //   navigateFallback: '/index.html',
      //   navigateFallbackAllowlist: [/^\/$/],
      //   ignoreURLParametersMatching: [/.*/],
      //   maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
      //   runtimeCaching: [],
      // }),
    ],
    optimization: {
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            compress: { drop_console: prod },
          },
        }),
        new CssMinimizerPlugin(),
      ],
    },
    watchOptions: {
      ignored: /node_modules|dist/,
      poll: 1000,
    },
    devServer: {
      // server: 'spdy', // http2+TLS
      headers: {
        "Cache-Control": "no-cache, no-store, must-revalidate",
      },
      proxy: [
        {
          context: ["/influx"],
          // target: 'http://localhost:8086',
          target: "https://hexa8.de/-/influx2",
          changeOrigin: true,
          pathRewrite: (path, req) => {
            return path.replace(/^\/influx/, "");
          },
        },
        {
          context: ["/api/live"],
          target: "http://localhost:3000",
          // ws: true,
          changeOrigin: true,
          // pathRewrite: (path, req) => {
          //   return path.replace(/^\/influx/, '');
          // },
        },
      ],
    },
  };
};
