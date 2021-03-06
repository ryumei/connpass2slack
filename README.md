# connpass イベントを Slack に通知する

一週間後までの [connpass](https://connpass.com) のイベントを検索して、
Slack へ投稿する AWS Lambda 関数のサンプルです。

お手元の環境でスタンドアロンで実行もできます。


# Launch to  AWS Lambda

## Slack

Incoming Webhook の用意をしておきましょう。

## AWS S3

Lambda 関数パッケージをアップロードするためのバケツを用意します。

* 名前とリージョン
  * バケット名: 任意
  * リージョン: Lambda 関数を置くのと同じリージョン
* プロパティ
  * バージョニング: 無効
  * サーバーアクセスログの記録: 無効
  * オブジェクトレベルのログ記録:!無効
  * デフォルト暗号化: なし
* アクセス権限
  * ユーザー: 本人のみ
  * パブリックアクセス許可: 無効
  * システムのアクセス許可: 無効

### AWS IAM Role

上記のバケツに Travis-CI から書き込みができるユーザの作成。

IAM からポリシーの作成

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::BUCKET_NAME/*"
        }
    ]
}
```


IAM からユーザの作成

ユーザー名: 任意
アクセスの種類
  * プログラムによるアクセス: チェック
  * AWS マネジメントコンソールへのアクセス: チェックなし
アクセス権限
  上記のポリシーを選択

アクセスキーとシークレットアクセスキーが作成されるので、
``travis`` コマンドで、.travis.yml へ暗号化して追加。

```
$ travis encrypt --add deploy.secret_access_key MY_AWS_SECRET_ACCESS_KEY
```
https://docs.travis-ci.com/user/deployment/s3/

AWS_ACCESS_KEY_ID, AWS_BUCKET, AWS_BUCKET_REGION
Travis-CI 上の環境変数として設定することにする。

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

関数コード

* コードエントリタイプを S3 から読み込みに変更し、
  lambda.zip の URL を指定します。
* ハンドラ: ``src.my_handler`` に変更します。

### 参照する環境変数

  * ``SLACK_URL``: Slack の Incoming Webhook URL
  * ``SLACK_CHANNEL``: Slack の投稿先チャネル名
  * ``SLACK_MESSAGE_PREFIX``: 投稿メッセージの冒頭部分
  * ``COMPASS_SERIESES``: compass で検索したいグループ ID

## Travis-CI

Github と連携させ、リポジトリのビルドを有効に。

環境変数

* ``AWS_ACCESS_KEY_ID``
* ``AWS_BUCKET``
* ``AWS_BUCKET_REGION``

## References

* https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
