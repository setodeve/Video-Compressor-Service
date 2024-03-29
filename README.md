# Video-Compressor-Service

## 概要
このプロジェクトは動画処理サービスです。
ユーザーは動画ファイルをサーバーにアップロードし、動画を加工することができます。
TCPを用いてクライアントとサーバー間の通信を行います。


## 機能
- **動画の圧縮**: 動画を自動的に圧縮し、サイズを削減しつつ高画質を維持。
- **動画の解像度変更**: ユーザーが選択した解像度に動画を変換。
- **動画のアスペクト比変更**: ユーザーが指定したアスペクト比に動画を変換。
- **動画からの音声変換**: 動画から音声を抽出し、MP3ファイルを生成。
- **特定時間範囲のGIF/WEBM作成**: ユーザーが指定した時間範囲の動画をGIFまたはWEBMに変換。

## 動作環境
- Python 3.10.9
- FFMPEG

## 使用方法
サーバーとクライアントのスクリプトをそれぞれ別ターミナルで実行します。

```bash
# ffmpegを使用するため事前にインストールが必要
brew install ffmpeg

# サーバーの実行
python3 server.py

# クライアントの実行
python3 client.py
```

## デモ
1. 別ターミナルでサーバー側とクライアント側を実行
2. 編集したい動画を同ディレクトリに配置(今回はcat.mp4を配置)
3. クライアント側で編集したい動画のファイル名を入力
4. クライアント側でどういった編集をしたいか選択(今回はgifに編集するを選択)
5. クライアント側でどこからどこまでgifにするか必要情報を入力
6. サーバーへファイルのアップロードが開始
7. アップロードされたファイルはInputフォルダに格納
8. アップロードが完了したら編集開始
9. 編集後のファイルはOutputフォルダに格納
10. 編集が完了したこととどこに編集後のファイルが格納されているかクライアントに通知

<img src="https://github.com/setodeve/Video-Compressor-Service/assets/83833293/5d518b46-2982-4412-adf7-07522b4f6449" width="1000">
