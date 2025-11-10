#!/usr/bin/env python3
import os
import sys
import subprocess
import threading

def is_jsonrpc_line(s: str) -> bool:
    """JSON-RPCメッセージまたはContent-Lengthヘッダかチェック"""
    t = s.lstrip()
    return t.startswith("{") or t.startswith("[") or t.startswith("Content-Length:")

def handle_stdout(proc):
    """標準出力を処理: JSON行のみ転送、それ以外はログに"""
    try:
        for line in proc.stdout:
            if is_jsonrpc_line(line):
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                # INFOログなどはstderrに
                sys.stderr.write(f"[FILTERED] {line}")
                sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[ERROR] stdout handler: {e}\n")
        sys.stderr.flush()

def handle_stderr(proc):
    """標準エラーを処理"""
    try:
        for line in proc.stderr:
            sys.stderr.write(line)
            sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[ERROR] stderr handler: {e}\n")
        sys.stderr.flush()

def main():
    # Python実行ファイルのパス
    py = os.environ.get("PYTHON_BIN", "/home/enpit/.pyenv/shims/python")
    cmd = [py, "-u", "-m", "hakoniwa_pdu.apps.mcp.server"]

    # 環境変数を設定
    env = os.environ.copy()
    env.setdefault("PDU_CONFIG_PATH", "/home/enpit/hakoniwa/hakoniwa-drone-core/config/pdudef/webavatar.json")
    env.setdefault("SERVICE_CONFIG_PATH", "/home/enpit/hakoniwa/hakoniwa-drone-core/config/launcher/drone_service.json")
    env.setdefault("HAKO_BINARY_PATH", "/usr/share/hakoniwa/offset")
    env["PYTHONUNBUFFERED"] = "1"
    
    # LD_LIBRARY_PATHを設定
    ld_path = env.get("LD_LIBRARY_PATH", "")
    if ld_path:
        env["LD_LIBRARY_PATH"] = f"/usr/local/lib/hakoniwa:{ld_path}"
    else:
        env["LD_LIBRARY_PATH"] = "/usr/local/lib/hakoniwa"

    sys.stderr.write(f"[WRAPPER] Starting MCP server...\n")
    sys.stderr.flush()

    # MCPサーバーを起動
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
        bufsize=1
    )
    
    # 標準出力と標準エラーを別スレッドで処理
    stdout_thread = threading.Thread(target=handle_stdout, args=(p,), daemon=True)
    stderr_thread = threading.Thread(target=handle_stderr, args=(p,), daemon=True)
    
    stdout_thread.start()
    stderr_thread.start()
    
    # プロセスの終了を待つ
    returncode = p.wait()
    
    # スレッドの終了を待つ
    stdout_thread.join(timeout=1)
    stderr_thread.join(timeout=1)
    
    sys.stderr.write(f"[WRAPPER] MCP server exited with code {returncode}\n")
    sys.stderr.flush()
    
    sys.exit(returncode)

if __name__ == "__main__":
    main()
