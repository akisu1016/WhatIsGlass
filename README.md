# what-is-grass

what はくさ。

## what is what is grass

言葉の Wikipedia を作ろうとしてる。 こちらはバックエンド

## 始め方

```
$ git clone https://github.com/akisu1016/WhatIsGrass.git
```
Docker使っているのでインストールして欲しい 以下brew

```
$ brew install docker
$ docker --version
Docker version 20.10.5, build 55c4c88
```

Docker起動した後 ビルドして起動
```
$ docker-compose up -d
```

コンテナ起動後コンテナに入りサーバーを立ち上げる
```
# コンテナに入る
$ docker exec -it whatisgrass-api bash

# サーバーを起動
root@61a05da8539e:/app# python app.py 
```
http://localhost:8080/api/[api名]　でリクエスト送ってね
