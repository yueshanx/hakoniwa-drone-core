#!/bin/bash
# 標準出力と標準エラーの両方をファイルにリダイレクト
exec > /tmp/hakoniwa_mcp_stdout.log 2>&1

# 環境変数を設定
export PDU_CONFIG_PATH=/home/enpit/hakoniwa/hakoniwa-drone-core/config/pdudef/webavatar.json
export SERVICE_CONFIG_PATH=/home/enpit/hakoniwa/hakoniwa-drone-core/config/launcher/drone_service.json
export HAKO_BINARY_PATH=/usr/share/hakoniwa/offset
export PYTHONUNBUFFERED=1

# Pythonのバッファリングを無効化
export PYTHONDONTWRITEBYTECODE=1

# MCPサーバーを起動
exec /home/enpit/.pyenv/shims/python -u -m hakoniwa_pdu.apps.mcp.server
