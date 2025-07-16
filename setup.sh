#!/bin/bash
# uv（https://github.com/astral-sh/uv）によるセットアップスクリプト
set -e

# uvが未インストールの場合はインストール
if ! command -v uv &> /dev/null; then
    echo "uvが見つかりません。インストールします。"
    pip install --upgrade pip
    pip install uv
fi

# 仮想環境作成（.venv ディレクトリ）
uv venv .venv

# 仮想環境有効化
source .venv/bin/activate

# 依存パッケージ一括インストール
uv pip install -r requirements.txt

echo "セットアップ完了: .venv を有効化して作業してください。"
