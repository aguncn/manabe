FROM alpine:3.7
COPY . /target-dir
WORKDIR /target-dir

RUN sed -i 's/dl-cdn.alpinelinux.org/mirror.tuna.tsinghua.edu.cn/g' /etc/apk/repositories &&\
    apk add --update-cache --virtual=build-dependencies \
    mariadb-dev\
    g++ \
    build-base libffi-dev python3-dev \
    libffi openssl ca-certificates \
    jpeg-dev zlib-dev freetype-dev \
    lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    linux-headers pcre-dev &&\
    apk add --no-cache pcre mailcap libuuid libffi py3-lxml py3-pillow python3  && \
    pip3 install --upgrade pip \
		--no-cache-dir -i http://mirrors.aliyun.com/pypi/simple/ \
		--trusted-host mirrors.aliyun.com &&\
    pip3 install -r /target-dir/requirements.txt \
	--no-cache-dir -i http://mirrors.aliyun.com/pypi/simple/ \
	--trusted-host mirrors.aliyun.com &&\
    apk del --purge build-dependencies && \
    rm -rf /var/cache/apk/* && \
    rm -rf /var/lib/apk/* && \
    rm -rf /etc/apk/cache/* && \
    rm -rf ~/.cache/ && \
    rm -rf /root/.cache /tmp/*

CMD ["/bin/sh"]