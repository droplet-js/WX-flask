# # 写在最前面：强烈建议先阅读官方教程[Dockerfile最佳实践]（https://docs.docker.com/develop/develop-images/dockerfile_best-practices/）
# # 选择构建用基础镜像（选择原则：在包含所有用到的依赖前提下尽可能提及小）。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/python?tab=tags)自行选择后替换。

# # 选择基础镜像
# FROM alpine:3.13
# #FROM ubuntu:latest

# # 容器默认时区为UTC，如需使用上海时间请启用以下时区设置命令
# # RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone
# MAINTAINER <mediapipe@google.com>

# # 拷贝当前项目到/app目录下
# COPY . /app

# # 设定当前的工作目录
# WORKDIR /app

# # RUN apt-get update && apt-get install -y --no-install-recommends \
# #         build-essential \
# #         ca-certificates \
# #         curl \
# #         git \
# #         wget \
# #         unzip \
# #         python \
# #         libopencv-core-dev \
# #         libopencv-highgui-dev \
# #         libopencv-imgproc-dev \
# #         libopencv-video-dev \
# #         software-properties-common && \
# #     add-apt-repository -y ppa:openjdk-r/ppa && \
# #     apt-get update && apt-get install -y openjdk-8-jdk && \
# #     apt-get clean && \
# #     rm -rf /var/lib/apt/lists/*

# # RUN pip install --upgrade setuptools
# # RUN pip install future


# # Install bazel
# # ARG BAZEL_VERSION=0.26.1
# # RUN mkdir /bazel && \
# #     wget --no-check-certificate -O /bazel/installer.sh "https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/b\
# # azel-${BAZEL_VERSION}-installer-linux-x86_64.sh" && \
# #     wget --no-check-certificate -O  /bazel/LICENSE.txt "https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE" && \
# #     chmod +x /bazel/installer.sh && \
# #     /bazel/installer.sh  && \
# #     rm -f /bazel/installer.sh


# # 使用 HTTPS 协议访问容器云调用证书安装
# RUN apk add ca-certificates

# # 安装依赖包，如需其他依赖包，请到alpine依赖包管理(https://pkgs.alpinelinux.org/packages?name=php8*imagick*&branch=v3.13)查找。
# # 选用国内镜像源以提高下载速度
# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
# # 安装python3
# && apk add --update --no-cache python3 py3-pip \
# && rm -rf /var/cache/apk/*



# # 安装依赖到指定的/install文件夹
# # 选用国内镜像源以提高下载速度
# #RUN pip install mediapipe-0.8.3.1-cp37-cp37m-manylinux2014_x86_64.whl
# RUN pip install mediapipe
# RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
# && pip config set global.trusted-host mirrors.cloud.tencent.com \
# && pip install --upgrade pip \
# # pip install scipy 等数学包失败，可使用 apk add py3-scipy 进行， 参考安装 https://pkgs.alpinelinux.org/packages?name=py3-scipy&branch=v3.13
# && pip install --user -r requirements.txt

# RUN pip install --no-cache-fir -r requirements.txt

# # 设定对外端口
# EXPOSE 80

# # 设定启动命令
# CMD ["python3", "run.py", "0.0.0.0", "80"]


FROM 3.7.0-slim     
COPY . /app
WORKDIR /app
RUN pip install mediapipe

CMD ["python3", "run.py", "0.0.0.0", "80"]


