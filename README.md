# 「知るべき97のこと」通知スクリプト

知るべき97のことを1つずつChatworkに投稿するスクリプト


## 概要

- コマンド引数で指定したChatworkのチャットグループに以下の記事を1つずつ投稿
  - [プログラマが知るべき97のこと](http://xn--97-273ae6a4irb6e2hsoiozc2g4b8082p.com/)
  - [プロジェクト・マネジャーが知るべき97のこと](http://xn--97-273ae6a4irb6e2h2k6c0ec7tvc3h1e0dwi7lj952k.com/)
  - [ソフトウェアアーキテクトが知るべき97のこと](http://xn--97-273ae6a4irb6e2h2ia0cn0g4a2txf4ah5wo4af612j.com/)
- 記事リストの最後までいったら最初に戻る
- URLはGoogle APIで短縮URL表示する


## 設定ファイル

スクリプトと同じディレクトリに `.env` ファイルを作成し、GoogleのAPIキーとChatworkのTokenを設定する。
.envファイルはバージョン管理の対象に含めないように注意すること。

```
[google]
api_key = AIz....CVU

[chatwork]
token = 6ef....35a
```


## 実行方法

```
% pytyon notify.py chatwork_room_id programmer.csv
% pytyon notify.py chatwork_room_id project_manager.csv
% pytyon notify.py chatwork_room_id software_architect.csv
```


## 通知サンプル

```
[info][title]今日の ソフトウェアアーキテクトが知るべき97のこと＋α[/title]6. 要求仕様の本当の意味を探れ / アイナー・ランドル http://goo.gl/rXD8w3[/info]
```


## その他

スクリプトと同じディレクトリに決まったフォーマットで `.csv` ファイルを置けば定期的な通知が可能。
フォーマットは下記の通り。

```
0,"毎回通知に含まれる全体のタイトル"
1,"1つめの記事のタイトル",1つめの記事のURL
2,"2つめの記事のタイトル",2つめの記事のURL
3,"3つめの記事のタイトル",3つめの記事のURL
  :
```

