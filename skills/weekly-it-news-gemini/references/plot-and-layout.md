# 承認型プロットと固定レイアウト契約

プロットにはedition_date、status(draft/approved)、slides配列を持つ。各ページにslide_id、story_id、layout_id、title、purpose、on_slide、speaker_notes、asset_idsを記録。必要画像は具体的な出典URL、どの部分を撮るか、そのページでの目的も持つ。

COVER：3月版の赤黒タイトル、青い日付枠、右上の元アバターを維持。日付と予告のみ更新。
AGENDA：2ページ目の現在のシンプルな目次。
NEWS：ニュースの概要、技術的な切り口。
SOURCE_IMAGE：実ニュース記事・写真・コード・公式資料を大きく表示。
TECH_DIAGRAM：編集可能な説明用模式図。
COMPARE：数値の単位・比較条件・出典を明示した編集可能な表。
TWO_SOURCES：実画像2点と対応する個別の出典・説明。

ひとつのstory_idは連続した一つのブロック。別のニュースを挟んで同じstory_idへ戻らない。強制的な固定ページ数・画像数・まとめは不要。明示的に承認された横断比較は例外。

テンプレート原本はGit管理。GeminiスキルZIPへバイナリPPTXや画像を同梱するのではなく、タスクに別途アップロードまたはDrive参照する。資料がないのに忠実な再現ができたと主張しない。

## テンプレートファイルの取得元

正本：https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/weekly-it-news-design-template.pptx

manifest： https://raw.githubusercontent.com/koduki/itnews-creator/main/assets/templates/template-manifest.json

スキルのメタデータではなく、タスクのブラウザ/ファイル操作でPPTXの**実体をダウンロードし検証**する。ダウンロードできないときはDriveまたは添付ファイルを使う。レイアウト参考のみなら文章ルールを使ってもよいが、元のテンプレートを使用したと主張してはならない。
