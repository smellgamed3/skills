#!/usr/bin/env python3
# /// script
# dependencies = ["requests"]
# ///
"""
Outline CLI — 通过命令行调用 Outline 知识库 API。

用法：
    uv run scripts/outline.py <接口名> [<JSON 参数>]

示例：
    uv run scripts/outline.py collections.list '{}'
    uv run scripts/outline.py documents.search '{"query": "部署流程"}'
    uv run scripts/outline.py documents.info '{"id": "DOC_UUID"}'

配置文件：~/.config/outline.json
    {
        "base_url": "https://app.getoutline.com",
        "api_key": "ol_api_..."
    }

更多接口示例参见 examples.md，完整参数说明参见 reference.md。
"""

import json
import pathlib
import sys

import requests


CONFIG_PATH = pathlib.Path("~/.config/outline.json").expanduser()


def load_config() -> dict:
    """读取 ~/.config/outline.json 配置文件。"""
    if not CONFIG_PATH.exists():
        print(
            f"错误：配置文件不存在 {CONFIG_PATH}\n"
            "请创建配置文件：\n"
            "  mkdir -p ~/.config\n"
            '  echo \'{"base_url": "https://app.getoutline.com", "api_key": "ol_api_..."}\''
            f" > {CONFIG_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误：配置文件格式无效 —— {e}", file=sys.stderr)
        sys.exit(1)


def call_api(base_url: str, api_key: str, method: str, data: dict) -> dict:
    """向 Outline API 发送 POST 请求并返回响应。"""
    url = f"{base_url.rstrip('/')}/api/{method}"
    try:
        resp = requests.post(
            url,
            json=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30,
        )
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f"错误：无法连接到 {base_url}，请检查 base_url 配置及网络连接。", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("错误：请求超时（30 秒），请稍后重试。", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        # 尝试解析错误响应体，给出更详细的提示
        try:
            err_body = e.response.json()
            print(
                f"HTTP {e.response.status_code} 错误：{err_body.get('error', '')} — "
                f"{err_body.get('message', '')}",
                file=sys.stderr,
            )
        except Exception:
            print(f"HTTP 错误：{e}", file=sys.stderr)
        sys.exit(1)

    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "用法：uv run scripts/outline.py <接口名> [<JSON 参数>]\n"
            "示例：uv run scripts/outline.py collections.list '{}'\n"
            "      uv run scripts/outline.py documents.search '{\"query\": \"部署\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    method = sys.argv[1]

    # 解析可选的 JSON 参数
    data: dict = {}
    if len(sys.argv) > 2:
        try:
            data = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"错误：JSON 参数解析失败 —— {e}", file=sys.stderr)
            sys.exit(1)

    config = load_config()
    base_url = config.get("base_url", "").strip()
    api_key = config.get("api_key", "").strip()

    if not base_url:
        print("错误：配置文件中缺少 base_url", file=sys.stderr)
        sys.exit(1)
    if not api_key:
        print("错误：配置文件中缺少 api_key", file=sys.stderr)
        sys.exit(1)

    result = call_api(base_url, api_key, method, data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
