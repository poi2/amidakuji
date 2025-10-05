# あみだくじ生成ツール

あみだくじを生成してPDFとして出力するPython製のCLIツールです。

## 機能

- 指定された縦棒数と横棒数範囲に基づいてあみだくじを生成
- 生成したあみだくじをPDFファイルとして保存
- コマンドライン引数による簡単な操作

## 使い方

```bash
python main.py --lines 5 --min-bars 8 --max-bars 15 --output amidakuji.pdf
```

### オプション

- `--lines` / `-l`: 縦棒の本数（必須）
- `--min-bars` / `--min`: 横棒の最小本数（必須）
- `--max-bars` / `--max`: 横棒の最大本数（必須）
- `--output` / `-o`: 出力PDFファイルのパス（必須）

## 開発環境

このプロジェクトは Dev Containers を使用して開発されています。VS Code で `.devcontainer` フォルダが検出されたら、コンテナで再度開くことで開発環境が自動的にセットアップされます。

### 必要なツール

- Docker
- Visual Studio Code
- Dev Containers 拡張機能

## ライセンス

MIT

