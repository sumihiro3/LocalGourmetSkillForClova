# LocalGourmetSkillForClova

Clova Extension Kit SDK for Python を使ったスキルのサンプルです。

## どんなスキル？
各都道府県にあるご当地グルメ情報を教えてくれるスキルです。
このスキルでできることは次の2種類です。

* 都道府県名からご当地グルメを調べる
    * 例：北海道のご当地グルメは？
* 個別のご当地グルメの詳細を調べる
    * 例：ザンギのことを教えて

### デモ動画

[こちらのツイート](https://twitter.com/sumihiro3/status/1028098363739103232) をご確認ください。


## スキル開発の解説は
スキル開発の解説は、下記のQiita へ投稿していますので、こちらを御覧ください。

* [前編：30分くらいでClova Extension Kit SDK for Python を使ったClova スキルを作る！（前編：スキル設定編）](https://qiita.com/sumihiro3/items/3ca0a2f849a116b509ff)
* [後編：30分くらいでClova Extension Kit SDK for Python を使ったClova スキルを作る！（後編：実装編）](https://qiita.com/sumihiro3/private/9e24170cad4ad384f453)

## 開発環境・実行環境について

このスキルを開発・実行する上で必要な環境です。

### 開発環境

* Mac OS X / Windows 10
* ブラウザ
* [Clova Developer Center](https://clova-developers.line.me/)
* [LINE Developers](https://developers.line.me/ja/)
* [python 3.6.5](https://www.python.org/downloads/release/python-365/)
    * 実行環境であるAWS Lambda のランタイムと同じバージョン
* [Clova Extension Kit SDK for Python](https://github.com/line/clova-cek-sdk-python)
* [Zappa](https://github.com/Miserlou/Zappa)
* [Flask](http://flask.pocoo.org/)



### 実行環境

* [AWS](https://aws.amazon.com/jp/)
    * Lambda
    * DynamoDB
    * API Gateway


# スキル開発の準備

上記のQiita への投稿では省略しましたが、開発までの準備作業をこちらに記録しておきます。
なお、このスキルを題材にしたスキル開発ハンズオンを開催予定です。

## 開発環境の準備

### python のインストール

#### Python 3.6.5 をダウンロードしてインストールしてください

https://www.python.org/downloads/release/python-365/

* Windowsの人はPATHの設定を行ってください。
    * Install の際に「Add Python 3.6 to PATH」にチェックを入れると自動的に設定されます
    * PATH の設定は下記のサイトを参考にしてください
        * https://www.pythonweb.jp/tutorial/install/index3.html
* 注意
    * Anaconda を利用されている場合、解説記事と動作が異なる場合があります。
    * 自己解決出来ない場合は上記方法でインストールしてください

### エディターの準備
基本的にお好きなエディターをお使いください。
筆者は[Visual Studio Code](https://code.visualstudio.com/) を利用しています。

### virtualenv のインストール

```shell
$ pip install --upgrade virtualenv
```

## AWS でのアカウント登録
実行環境としてAWS（Lambda、DynamoDB、API Gateway）を利用するので、AWS のアカウント登録をしてください。
登録後1年は多くのサービスを基本無料で利用できます。
なお、クレジットカード情報登録が必要です。

参考サイトはこちら

* [AWS アカウント作成の流れ](https://aws.amazon.com/jp/register-flow/)
* [AWSの無料アカウントを作成する(Amazon Web Services)](https://www.ritolab.com/entry/9)

## AWS CLI の準備

Zappa でAWSを操作するためにAWS CLI が必要となります。
下記のサイトを参考にして、AWS CLI のインストールと設定をしてください。

### Mac OS X の場合

[macOS で AWS Command Line Interface をインストールする](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-install-macos.html)

### Windows の場合

[Microsoft Windows で AWS Command Line Interface をインストールする](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/awscli-install-windows.html)

### AWS CLI の設定

[AWS-CLIの初期設定のメモ](https://qiita.com/reflet/items/e4225435fe692663b705)

## Clova Developer Center とLINE Developers の設定

下記のサイトを参考にして、Clova Developer Center とLINE Developers への登録とプロバイダーの設定を済ませておいてください。

* [Clova Developer Centerの使い方 - 誰でも簡単にできる！ LINE Clovaスキルの作り方](https://codezine.jp/article/detail/10927?p=2)
* [本日リリース！LINE Clovaのスキル開発の始め方〜申請編〜](https://dotstud.io/blog/line-clova-skill-tutorial/)

