#!/bin/bash

# ユーザーにポート番号を尋ねる
echo "Which port do you want to use for the Django server?"
read port

# 環境変数を設定（オプショナル、必要に応じて）
export DJANGO_SERVER_PORT=$port

# Djangoサーバーをユーザーが指定したポートで起動
python manage.py runserver 127.0.0.1:$port