# Weekly IT News — Gemini生成／PowerPoint仕上げ

| 項目 | Gemini Tasks | Copilot in PowerPoint／Claude |
| --- | --- | --- |
| ニュース調査、対話・編集プロット、ユーザー承認 | 担当 | 再構成しない |
| DOCXから画像・リンクの抽出 | 担当 | 対象外 |
| Google Sheets→GAS→Driveで記事画像撮影 | 担当。保存したPNGを検品 | 対象外 |
| 固定テンプレートからPPTX生成 | python-pptxで決定論的に制作 | 既存PPTXを局所修正 |
| QA | LibreOffice/PDF/PNGで全ページを確認 | 投影品質とPowerPoint実表示を確認 |
| 図・表・文字・クロップ | 初期生成 | 仕上げ |

## 正本と引き継ぎ

- 8レイアウトの正本：`assets/templates/weekly-it-news-design-template.pptx`。ハッシュ値は`assets/templates/template-manifest.json`。
- 原本表紙：`assets/cover/weekly-it-news-cover-20260315.pptx`、`avatar-20260315.jpg`。
- 企画：承認済み`plot.json`と`plot.md`。
- 画像：`assets-manifest.json`（実バイト、出典、取得日時、権利、目視承認）。
- Gemini成果物：`base.pptx`、`qa/preflight.json`、レンダリング画像。
- PowerPoint成果物：レイアウト調整済み`final.pptx`と検品報告。

GeminiのVMではGitHub rawのPPTX直接取得やブラウザ画面のPNG保存を前提にしません。テンプレートはDrive／添付から取得し、画像はGAS中継や添付DOCXから回収します。GASの`captured`と、画像内容が妥当と判定された`approved`は別状態です。撮影中継は既存の9列キューのまま、`notes`の機械可読メタデータで実行開始・再試行・クールダウン等を扱います。実機GASへの更新は手作業が必要です（[運用ガイド](gas-relay.md)）。

## デザイン

`COVER`→`AGENDA`→各ニュース先頭の`NEWS_TITLE`（青いニュース番号、濃紺見出し、淡青番号）→`NEWS`、`SOURCE_IMAGE`、`TECH_DIAGRAM`、`COMPARE`、`TWO_SOURCES`。同じニュースは連続させ、章扉の自動追加を承認時のスライド枚数に含めます。PowerPoint側で章扉やニュース順序を勝手に変更しません。

完成用PPTXでは`--strict-assets`を使います。画像ファイルが存在してもスクショにCloudflare/Cookie画面が含まれないことをコード単独で証明できないため、実画像・レンダリング画像の目視検品を要求します。

## 配布

`VERSION`をスキルの配布バージョンとし、GitHub ActionsはGemini用とPowerPoint用の**2 ZIPだけ**を作成。バイナリPPTX/JPEG/PNG、GAS`.gs`ファイルはスキルZIPに含めません。テンプレートを変更したときはDrive側にも同期してください。
