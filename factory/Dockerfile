# 前端 Dockerfile - 第一阶段：构建
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
# 使用淘宝源加速
RUN npm config set registry https://registry.npmmirror.com
RUN npm install
COPY . .
RUN npm run build

# 第二阶段：运行 (使用 Nginx 托管静态文件)
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# 为了防止 React 路由刷新 404，我们需要修改一下 nginx 配置
RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]