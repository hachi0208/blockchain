# blockchain

環境変数なども全てこのリポジトリに含めています。

# 目的 

bitcoinのblockchainの仕組みを可視化しようとしたもの。
8000、8001、8002portで立ち上げることでbitcoinの動作を反映させれる。



# 立ち上げ方



python ver 3.9.13

```
cd bitcoin-backend

python -m venv venv

. venv/bin/activate

pip install -r requirements.txt

python manage.py runserver
```



node ver 18.14.0

```
cd bitcoin-frontend

yarn install --immutable

yarn start
```

## ホーム画面

<img width="700" alt="スクリーンショット 2024-02-09 23 23 58" src="https://github.com/hachi0208/blockchain/assets/114277057/b9a87709-c3f4-4e50-b906-b7f383526564">



## MyWallet

<img width="700" alt="スクリーンショット 2024-02-09 23 24 05" src="https://github.com/hachi0208/blockchain/assets/114277057/1dfd550f-29d9-4b1a-80b1-661a9a688782">


## BlockChain

<img width="700" alt="スクリーンショット 2024-02-09 23 25 05" src="https://github.com/hachi0208/blockchain/assets/114277057/069e83cb-6a75-45cd-a0d8-1542f1d14ffa">



## Mining

<img width="700" alt="スクリーンショット 2024-02-09 23 25 16" src="https://github.com/hachi0208/blockchain/assets/114277057/5b4645be-0b67-49fc-b6b2-3c06f6d6c124">


## 取引所

<img width="700" alt="スクリーンショット 2024-02-09 23 25 24" src="https://github.com/hachi0208/blockchain/assets/114277057/e6639114-da03-45ad-a9a0-6b5a5ec38be5">

