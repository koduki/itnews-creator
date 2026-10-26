# itnews-creator — Weekly IT News v0.9.2

[MIT License](LICENSE) · [実装アーキテクチャ](docs/architecture-gemini-claude.md)

**Gemini Tasks + Google Apps Script (GAS) + Google Drive + python-pptxで制作し、Copilot in PowerPoint（利用可能なClaude 5.5）で最終調整する**、Weekly IT News用のワークフローです。

以前の「Gemini TasksがGitHub rawからPPTXバイナリを直接取得」「ブラウザ閲覧結果をPNGとしてVMへ直接保存」という**動作しなかった前提は、標準フローから外しました**。ここではユーザーが実機検証したGoogle Drive中継・添付DOCX解体・GAS撮影を標準とします。

## 制作フロー

| 工程 | 担当 | 成果物 |
| --- | --- | --- |
| 資料準備 | Gemini Tasks | 添付DOCXの `word/media/*` と `word/_rels/document.xml.rels` から画像・出典リンクを抽出 |
| ニュース調査・編集会議 | Gemini Tasks＋発表者 | 見せたいニュース、解説、見出し、ページ単位 `plot.md` / `plot.json` |
| Web画面撮影 | Google Sheet `itnews-screenshot-queue` → GAS → Drive `itnews-assets` | 撮影ジョブとPNG、取得状況・出典・日時 |
| 素材回収・品質確認 | Gemini Tasks | `drive:search_files` → `drive:download_file_content` → ローカルで画像を `view_file` して検品 |
| **承認済みプロットから制作** | Gemini Tasks の `python-pptx` / Pillow | 固定テンプレートを使った、実素材入りの編集可能な `base.pptx` |
| レンダリングQA | LibreOffice + PDF/PNG変換 + `pypdfium2` | 全ページの文字化け・画像・はみ出しチェック |
| 最終仕上げ | Copilot in PowerPoint のClaudeモデル | 内容・ページ順を保持して配置・図形・表・ノートを修正した `final.pptx` |

## 最初に準備するもの

1. [固定7レイアウトPPTX](assets/templates/weekly-it-news-design-template.pptx) を**Google Driveに1回配置**し、Gemini Tasksから `drive:search_files` と `drive:download_file_content` でダウンロードします。あるいはチャット添付ファイル `user_uploaded_files/` を読みます。
2. [template-manifest.json](assets/templates/template-manifest.json) のSHA-256（`f343a4fee2d802ce7ce36290d951a4a09526a451ccb16e9d41d0cb62f5ddee73`）と7スライド・表紙の元アバターを検証します。GitHubは**テンプレートの正本・バージョン管理先**であり、Gemini VMのバイナリ取得口ではありません。
3. Googleスプレッドシート `itnews-screenshot-queue`（タブ `queue`）を用意し、9列 `asset_id, slide_id, url, status, file_name, drive_file_id, drive_view_url, captured_at, notes` を配置します。
4. シートにバインドしたGoogle Apps Scriptへ [`screenshot_relay.js`](skills/weekly-it-news-gemini/scripts/screenshot_relay.js) の内容を貼り付けます。GAS側は `.gs` として管理されても、**GeminiスキルZIPに入れるファイルは `.js`** です。権限承認後、GASメニューから定期監視トリガーを設定します。Driveの出力先 `itnews-assets` のフォルダID、必要ならAPIキー等を設定してください。運用環境を変えるときはGASの `CONFIG.FOLDER_ID` を更新します。
5. ZIPから [Geminiスキル](skills/weekly-it-news-gemini/SKILL.md) を登録し、出力PPTXはPowerPoint側の [仕上げスキル](skills/itnews-powerpoint-polish/SKILL.md) に渡します。

## 画面撮影と検品

プロット作成中に撮影対象URLを上記シートへ **`status=pending`** で登録。GASがPageSpeed Insights v5 → （任意のカスタムScreenshot API）→ `image.thum.io` にフォールバックし、PNG/JPEG等の画像をGoogle Driveへ保存、`captured` とファイルID・URL・撮影時刻を書き戻します。PageSpeed APIはキーなしではHTTP 429の発生があり得るため、フォールバックを必須とします。

GeminiはDriveからファイルをVMの `downloads/` に回収し、**画像ファイルを必ず目視確認**します。Cloudflareの「Performing security verification」やCookie同意モーダルがニュース本文を隠している場合、撮影が `captured` でも**合格にしません**。`assets-manifest.json` に不備を記録し、出典を明示してImpress WatchやITmedia等の適切な報道へ差し替えるか、要再撮影とします。撮影サービスへURLを送信するため、公開記事以外（非公開URL・認証トークン付きURL・社内サイト）は投入しません。

実機で「5件の撮影・Drive回収・PPTXへの画像埋め込み」が成功した構成をベースにしていますが、他サイト・別テナントでも必ず成功するという意味ではありません。著作権と再利用条件を確認します。

## 編集方針・デザイン

- 3月15日版の表紙（赤黒 `Weekly IT News！`、青い日付枠、元アバター）を維持し、2枚目は現行の簡潔な「今週のトピック」。
- 本文は `NEWS` / `SOURCE_IMAGE` / `TECH_DIAGRAM` / `COMPARE` / `TWO_SOURCES` の固定レイアウト。**原則、1ページ1スクリーンショット**。
- 「ニュース解説→実画面→技術的な面白さ→次のニュース」を基本に、ひとつのトピックを連続した塊として配置。ページ割りは人間が承認したプロットを変更しない。
- 見出しは番組調の具体的なフックにし、難解な直訳語（「アンビエントAI」等）は分かりやすい「常駐型AIエージェント」などへ言い換える。事実・攻撃者主張・考察は混同しない。
- **3つの編集展開パターン**（新プロダクト・重大脆弱性・クラウド侵害と総括）、`python-pptx` の実測座標・Yu Gothic/Meiryo UIを使う文字化け対策は [レイアウト契約](skills/weekly-it-news-gemini/references/plot-and-layout.md) を参照。

## Gemini Tasksへの依頼例

> `weekly-it-news-gemini` スキルを使って、添付調査レポートの画像と出典を抽出し、ニュースを対話的に深掘りしてください。各ページの役割・見出し・画像URL・レイアウトIDをプロットにして、私の承認を得てから生成してください。画像は `itnews-screenshot-queue` → GAS → `itnews-assets` で取得して `view_file` で検品し、Driveの固定テンプレートを検証して `python-pptx` で編集可能なPPTXを出力してください。LibreOfficeで全ページを視覚確認し、取得できなかった画像は明示してください。

## PowerPointでの最終仕上げ

`base.pptx` を開き、利用可能なClaudeモデルを選択して [itnews-powerpoint-polish](skills/itnews-powerpoint-polish/SKILL.md) を適用します。**新しい情報収集や構成変更は行わず、レイアウト・画像のクロップ・編集可能な図表・発表者ノートだけ**を調整します。モデル名はテナント/環境の選択肢に従い記録します。

## 配布・開発

[GitHub Actions](https://github.com/koduki/itnews-creator/actions/workflows/package.yml) の成功RunのArtifactsから外側のZIPを取得すると、`itnews-creator-gemini-task-skill-v0.9.2.zip`、`itnews-creator-powerpoint-polish-skill-v0.9.2.zip`、旧Copilot Chat互換用ZIPとChatGPTプラグイン用ZIPを入手できます。**GASの `.js` はGemini用スキルZIP内**に含まれますが、自動的にGoogle Apps Scriptプロジェクトへデプロイされるわけではありません。Python標準ライブラリの `scripts/build_packages.py` で再現可能にビルドします。

注：ユーザー提供の表紙・アバター、他者のニュース写真や構成図の利用条件はそれぞれの権利者に従い、独自コードのMITライセンスが自動的に適用されるものではありません。