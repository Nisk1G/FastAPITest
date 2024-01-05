# バックエンド進捗

## 現状報告 (2024/1/5 18:00時点)
- 頂いたレポジトリの環境でmakeが通らない  
⇒自分だとなんもわからん状態だったので黒川さんにお手すきの際に修正してもらうようにお願いした.  
⇒⇒ 本レポジトリでAPIのテスト環境を作成してAPIだけ作ってしまうことを優先して作業

## 各API
### bus
[Google Sheets API](https://developers.google.com/sheets/api/guides/concepts?hl=ja) を用いて, マスターデータ(ゲーム開発ではこう言うけどWebではなんていえばいいか分からんでした, db?)を書いた[スプレッドシート](https://docs.google.com/spreadsheets/d/1-O0RRZyd_xCGoj1cwoHYrigngggZx1g_Yzw0zMPwBDs/edit#gid=0)からjson形式で出力する形式  
出力するjsonは[ここ](output_data/bus_output.json)

### mozu_food, sugi_food
[Places API](https://developers.google.com/maps/documentation/javascript/places?hl=ja)を叩いて、なかもずキャンパス, 杉本キャンパスの半径500mにある飲食店の情報を取得, また画像もいるかなと思ったので画像もパスを作成して返す感じ.だいぶ整形する必要があるかも

出力するjsonは[中百舌鳥ver](output_data/mozu_food_output.json), [杉本ver](output_data/sugi_food_output.json)

## 課題点
- Places API の引きが悪い  
飲食店の情報を検索するときにkeywordで指定する必要があるが、レストランとかフードを指定しても中百舌鳥で歴史を刻めが引けてないとか少し甘い部分がある。  
いっそバスみたいに仮データみたいな形でデータ置いてやったほうが楽そう

- API叩く時のkeyが丸見え  
隠した方が良い気がするけどお作法がわかんね～
