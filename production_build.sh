#!/bin/bash

mkdir -p ~/storage
mkdir -p ~/applog
# 切换到src目录
cd backend

# 停止并删除现有的Docker容器(如果存在)
docker stop tracker
docker rm tracker

# 删除旧的Docker镜像
docker rmi trackerimg

# 构建新的Docker镜像
docker build -t trackerimg . 

# 运行新的Docker容器
docker run -d \
  --name tracker \
  --network host \
  --privileged \
  -v ~/storage:/app/storage \
  -v ~/applog:/app/log \
  -e SUPERUSER=$SUPERUSER \
  -e SUPERPASS=$SUPERPASS \
  -e SUPEREMAIL=$SUPEREMAIL \
  -e SMTP_HOST=$SMTP_HOST \
  -e SMTP_USER=$SMTP_USER \
  -e SMTP_PASSWORD=$SMTP_PASSWORD \
  -e SMTP_PORT=$SMTP_PORT \
  -e EMAILS_FROM_EMAIL=$EMAILS_FROM_EMAIL \
  -e JWT_SECRET_KEY=$JWT_SECRET_KEY \
  -e DEBUG=false \
  -e APP_NAME=Tracker \
  -e APP_DESC=Tracker \
  -p 8000:8000 \
  trackerimg