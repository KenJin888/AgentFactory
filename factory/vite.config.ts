import path from 'path';
import {defineConfig, loadEnv} from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
    return {
      base: mode === "production" ? "./" : "/",
      plugins: [vue()],
      build: {
        assetsInlineLimit: 0,
      },
      define: {

      },
      server: {
      host: true,
      port: Number(env.VITE_APP_PORT),
      open: true,
      proxy: {
        // 代理 /dev-api 的请求
        [env.VITE_APP_BASE_API]: {
          target: env.VITE_API_BASE_URL, // 代理目标地址：https://后端地址
          secure: false, // 请求是否https
          changeOrigin: true, // 是否跨域
          // rewrite: (path: string) => path.replace(new RegExp("^" + env.VITE_APP_BASE_API), ""),
        },
      },
    },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, 'src'),
          '@utils': path.resolve(__dirname, 'src/utils'),
        }
      }
    };
});
