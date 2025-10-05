# 公式のPython Dev Containerイメージをベースにする
# これにはgitや共通ツールがプリインストールされている
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# non-interactiveに設定し、apt-get実行時のプロンプトを抑制
ENV DEBIAN_FRONTEND=noninteractive

# システムパッケージの更新と、必要に応じた追加ライブラリのインストール
# (この例では追加は不要だが、必要であればここに追記)
RUN apt-get update && apt-get -y install --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# uvをシステム全体にインストール
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    mv /root/.local/bin/uvx /usr/local/bin/uvx && \
    chmod +x /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uvx

# VS Codeが使用する非rootユーザー'vscode'に切り替える
# remoteUserと一致させる
USER vscode