#!/bin/bash
# 標準出力と標準エラーを完全にファイルにリダイレクト
exec > /tmp/hakoniwa_mcp.log 2>&1

# 環境変数を設定
export PDU_CONFIG_PATH=/home/enpit/hakoniwa/hakoniwa-drone-core/config/pdudef/webavatar.json
export SERVICE_CONFIG_PATH=/home/enpit/hakoniwa/hakoniwa-drone-core/config/launcher/drone_service.json
export HAKO_BINARY_PATH=/usr/share/hakoniwa/offset
export PYTHONUNBUFFERED=1

# デバッグ情報をログに記録
echo "=== MCP Server Start: $(date) ==="
echo "PDU_CONFIG_PATH=$PDU_CONFIG_PATH"
echo "SERVICE_CONFIG_PATH=$SERVICE_CONFIG_PATH"
echo "HAKO_BINARY_PATH=$HAKO_BINARY_PATH"

# MCPサーバーを起動(stdoutをファイルに、stderrも同じ場所に)
/home/enpit/.pyenv/shims/python -u -m hakoniwa_pdu.apps.mcp.server 2>&1 | tee -a /tmp/hakoniwa_mcp_detail.log | grep -v '^\[INFO\]' | grep -v '^\[DEBUG\]' | grep -v '^Client '
