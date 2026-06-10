#!/usr/bin/env python3
"""
星微光学调研报告 · 数据同步脚本
用于定期更新光学产品电商数据（Amazon Best Sellers / 天猫 / 京东）
当前版本：v1.0 · 手动更新模式
后续可接入 cronjob 自动刷新
"""
import json
import os
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(REPO_DIR, "data.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    data["generated"] = datetime.now().strftime("%Y-%m-%d")
    data["report_version"] = f"v{data.get('report_version', 'v1.0')}"
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def push_to_github():
    """Push updated data to GitHub"""
    import subprocess
    cmds = [
        f"cd {REPO_DIR} && git add data.json",
        f'cd {REPO_DIR} && git commit -m "data: auto-refresh {datetime.now().strftime("%Y-%m-%d %H:%M")}" || true',
        f"cd {REPO_DIR} && git push origin master"
    ]
    for cmd in cmds:
        subprocess.run(cmd, shell=True, capture_output=True)

if __name__ == "__main__":
    print(f"星微光学数据同步 · {datetime.now().isoformat()}")
    data = load_data()
    print(f"当前 {len(data['categories'])} 个赛道，{sum(len(c['subcategories']) for c in data['categories'])} 个细分品类")
    # TODO: 接入 Amazon API / 天猫商品数据自动采集
    # save_data(data)
    # push_to_github()
