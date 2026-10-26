# Weekly IT News v0.9.2 — 実機検証に合わせたアーキテクチャ

## 採用する構成

```text
Gemini Tasks ── 対話・出典検証・添付DOCXの画像/リンク抽出
      │
      ├──→ 編集プロット（plot.json, plot.md）←── 発表者の承認
      │                       │
      ├──→ Sheetsの撮影キュー（9列、pending）
      │             └──→ GAS (PageSpeed → 任意の外部API → Thum.io)
      │                           └──→ Drive itnews-assets（captured）
      ├──→ Drive APIから画像をVMへダウンロード → view_fileで目視検品
      ├──→ Driveの固定PPTXをVMへダウンロード → SHA-256で検証
      ├──→ python-pptx / Pillow → 編集可能なbase.pptx
      └──→ LibreOffice / pypdfium2 → 全ページレンダリングQA
                         │
Copilot in PowerPoint ── Claude 5.5（利用可能なモデル）→ final.pptx
```

## 1. Geminiの実行環境と素材取得

Gemini TasksのVMには現行の実機検証で`python-pptx`、`Pillow`、`libreoffice`、`pypdfium2` が入っていた。**それでもVMの外部通信（curl/requests）は遮断される**。ブラウザ検索ツールの閲覧結果も画像バイナリとしてVM内に直接取得できない。この制約を回避する正本の経路は次の2つ。

- **Drive取得**：テンプレートやGASが生成した画像を `drive:search_files` → `drive:download_file_content` でVMへ。Google Driveへ接続されていない場合の初回フォールバックはユーザー添付 `user_uploaded_files/`。一旦配置済みなら毎回GitHub rawアクセスは行わない。取得したファイルをZIP/PPTXとして開けるかとハッシュで検証する。
- **添付DOCX解体**：添付の `.docx` はWordprocessingMLのZIP。`word/media/*` の画像と `word/_rels/document.xml.rels` のリンクターゲットを機械的に抽出。リンクは取得しただけで検証済み出典とは扱わない。PDF等は形式に適した別の抽出方法を使う。

GitHub (`assets/templates/weekly-it-news-design-template.pptx`) は**更新・バージョン管理用正本**。Tasksの実行時データ取得先はDriveまたはアップロードであり、GitHub rawへの直接取得は標準ルートではない。

## 2. GASスクリーンショット中継

GAS実装：`skills/weekly-it-news-gemini/scripts/screenshot_relay.js`（Gemini ZIPへの格納は**必ず `.js`**。`.gs` はZIP MIME検査でapplication/octet-streamとして拒否された）。GAS自体はGoogle Sheetにバインドして設置する。

シート：`itnews-screenshot-queue` / タブ `queue`。列順は `asset_id, slide_id, url, status, file_name, drive_file_id, drive_view_url, captured_at, notes`。Geminiが画像が必要なページの行を`pending`登録。GASは時間主導型トリガーまたはメニュー手動実行で処理し、完成PNGを`itnews-assets`に保存、ファイルID/URL/時刻を書き戻す。

撮影手段：**PageSpeed Insights API v5**を第一優先。HTTP429などで失敗すると、構成済みの場合は認証付きScreenshot APIを利用し、さらに**Thum.io**（デフォルト1280px幅/クロップ853px）へフォールバック。スクリーンショット作成者と取得方式を`notes`/画像マニフェストに記録する。

GASの`captured`は**画像ファイルが保存されたこと**の意味であり、「ニュース記事が読める」「Cookie画面がない」の意味ではない。Geminiは`drive:download_file_content`と`view_file`で画像を必ず目視確認し、Cloudflare検証、Cookieモーダル、404、空白画面などで本文を隠している画像は除外、原因を`assets-manifest.json`に記録して再撮影または適切な代替ソースを手配。撮影対象URLは公開記事に限定し、第三者APIへ秘密のURLを送らない。

取得できなかった画像は`unavailable`/`needs_review`のまま。虚偽の画像を生成しない。著作権と転載条件を別途チェックする。実機では5画像を回収・PPTX埋め込みまで成功したが、一般サイトでの100%成功を保証するものではない。

## 3. プロットと固定デザイン

`plot.json`にslide_id、story_id、layout_id、タイトル、見せる内容、source_urls、asset_ids、発表者ノートを記録し、**承認後は構成とページ順を固定**。ニュースを途中で切って別ニュースの後で再登場させない。`SOURCE_IMAGE`は原則1ページ1スクショ。見出しはニュース番組調、直訳語「アンビエントAI」は原則「常駐型AIエージェント」などに言い換える。

3つの型：**新プロダクト・OSS潮流**、**重大脆弱性と社会的反応**、**クラウド侵害・信頼境界・対策の総括**。詳細は`skills/weekly-it-news-gemini/references/plot-and-layout.md`。

`python-pptx`で7スライドの編集可能テンプレートからプロット各ページに対応するレイアウトを複製し、日付/本文/画像/図形を書き換える。複製時に元アバター等の画像リレーションを消さないこと。**オブジェクトのdeepcopyだけでは画像の関連付けが保存される保証はない**ので、実際のPPTXの`ppt/media`とrelsもチェックする。スライド元テンプレート7枚は出力時に削除し、プロットのページ数に一致させる。

図形/座標は`plot-and-layout.md`で規定。LibreOffice経由のPDF→PNG全ページQAで日本語が豆腐にならないよう、必要に応じて全`<a:rPr>`/`<a:defRPr>`の`<a:ea typeface="Yu Gothic"/>`とフォントを指定し、実際の表示結果でチェックする。文字サイズ自動調整・下端6.55インチ以内などの規定を使用する。

注意：受領したv0.9.2 ZIPにはGAS実行コードとレイアウト/複製手順・テストが含まれるが、**その実機で利用したフル版`python-pptx`生成器のソースは同梱されていない**。このためGitHub内の手順だけで同一の生成PPTXを再現できるとはまだ保証しない。必要に応じてGemini Tasks側の稼働コードを別途取り込む。

## 4. PowerPoint側

Geminiが完成させた`base.pptx`と承認プロット、画像マニフェストをPowerPointに引き継ぐ。Copilot in PowerPointの**実際に選択可能なClaude 5.5モデル**で余白/切り抜き/フォント/図/表/ノートを磨く。内容、ページ順、記事画像と出典を勝手に選び直さない。

## 5. 実行時検証とCIの区別

- ローカル/GitHub CI：ZIP構造、テンプレートのハッシュ、7レイアウト、GASスクリプト同梱、`.gs`混入禁止、文書とスキルの参照整合性。
- 実機：DriveからのPPTX/PNG取得、GASの撮影と目視検査、PowerPointの完全な図形/画像リレーション、LibreOfficeの描画、PowerPoint Claudeの最終編集。CIが通っても実機での動作を意味しない。