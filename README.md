# connpass イベントを Slack に通知する

## Slack

Incoming Webhook の用意をしておきましょう。

## AWS Lambda

AWS コンソールにログインします。

Lambda を選択し、Lambda 関数の作成を選択します。

一から作成を選び、
* 名前: connpass2slack
* ランタイム: Python 3.6
* ロール:

Lambda 関数の設定ページで環境変数の設定

* SLACK_URL:
* CONNPASS_SERIESES: カンマ区切り (スペースなし)

### 参照する環境変数

  * ``SLACK_URL``: Slack の Incoming Webhook URL
  * ``SLACK_CHANNEL``: Slack の投稿先チャネル名
  * ``SLACK_MESSAGE_PREFIX``: 投稿メッセージの冒頭部分
  * ``COMPASS_SERIESES``: compass で検索したいグループ ID

## Travis-CI

Github と連携させ、リポジトリのビルドを有効に。


## References

* https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
