# manaba bot
これは**manaba**を利用する学生に向けて作成したプロジェクトです。  
講義ごとの未提出課題・レポート情報をLINEから確認できます。

このプロジェクトを使用する際にはプロジェクトのルートに以下のような.envファイルを作成する必要があります。  

```:.env
ACCESSTOKEN= ...
WEB_HOOK_URL = ...

POSTGRES_DB = ...
POSTGRES_USER = ...
POSTGRES_PASSWORD = ...
```

現段階ではngrokを使用してデプロイしています。
環境に合わせて適宜変更する必要があることに注意してください。
