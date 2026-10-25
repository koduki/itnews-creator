# Gemini Tasks → PowerPoint Claude引き継ぎ

Gemini Tasksが制作したbase.pptx、ユーザー承認済みplot.json、素材の出典と撮影状態のassets-manifest.jsonを受け取る。

責任分界：ニュース選定・プロット・追加調査・記事画面キャプチャ・写真の取得・PPTXの初期生成はGemini Tasks。既存PPTXの仕上げ、スライドの読める大きさ、写真クロップ、編集可能な模式図の改善、表やノートの体裁はCopilot in PowerPointのClaude。

不変条件：ページ数・順・見出し・story_id・layout_id・引用と事実関係・画像の選択/出典を承認プロットから勝手に変えない。追加取材が必要な場合はGeminiへ戻す。

PowerPointのカスタムスキルZIPはPNG/PPTXなどのバイナリが非対応なので、固定テンプレートや画像はGitから別添か、生成PPTXへ埋め込んだ形で渡す。

PowerPoint編集モードのモデル選択から使えるClaude 5.5を選ぶ。Claude Sonnet 5.5やOpus 5.5が表示されない場合は使えるモデルを明示して必要な対応を確認する。