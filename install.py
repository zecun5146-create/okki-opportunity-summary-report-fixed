#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""安装 okki-opportunity-summary-report-fixed 技能到当前 Accio 账号（跨平台）。

用法（二选一）：
  1. 双击 安装-Windows双击我.bat / 安装-苹果Mac双击我.command
  2. 把本文件发给 Accio Work 智能体执行：python install.py
"""
import json
import os
import shutil
import sys

SKILL_NAME = "okki-opportunity-summary-report-fixed"
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_SRC = os.path.join(PKG_DIR, SKILL_NAME)


def find_accio_root():
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".accio", "state", "current-space.json"),
        os.path.join(home, "Library", "Application Support", "accio", "state", "current-space.json"),
        os.path.join(home, "Library", "Application Support", "Accio", "state", "current-space.json"),
        os.path.join(home, "Library", "Application Support", "Accio Work", "state", "current-space.json"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    for root, _dirs, files in os.walk(home):
        if "current-space.json" in files and ".accio" in root:
            return os.path.join(root, "current-space.json")
    return None


def find_skills_dir(account_id):
    base = os.path.join(os.path.expanduser("~"), ".accio", "accounts")
    if not os.path.isdir(base):
        return None
    found = []
    for acc in os.listdir(base):
        if account_id and not acc.startswith(account_id):
            continue
        agents_root = os.path.join(base, acc, "agents")
        if not os.path.isdir(agents_root):
            continue
        for agent in os.listdir(agents_root):
            sdir = os.path.join(agents_root, agent, "agent-core", "skills")
            if os.path.isdir(sdir):
                try:
                    mtime = os.path.getmtime(sdir)
                except OSError:
                    mtime = 0
                found.append((mtime, sdir))
    if not found:
        return None
    found.sort(key=lambda x: -x[0])
    return found[0][1]


def register(skills_dir, install_path):
    reg = os.path.join(skills_dir, "skills.jsonc")
    entry = {
        "id": SKILL_NAME,
        "name": SKILL_NAME,
        "version": "",
        "enabled": True,
        "kind": "directory",
        "entryName": SKILL_NAME,
        "description": "OKKI/小满CRM商机全量盘点与固定格式总结报告技能（左侧目录+图表+筛选+跳转，管理/业务双视角）。",
        "installPath": install_path,
    }
    data = {}
    if os.path.isfile(reg):
        try:
            data = json.load(open(reg, encoding="utf-8-sig"))
        except Exception:
            data = {}
    skills = data.get("skills", [])
    ids = {s.get("id") for s in skills}
    if SKILL_NAME not in ids:
        skills.append(entry)
        data["skills"] = skills
        with open(reg, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("[OK] 已注册到 skills.jsonc")
    else:
        print("[OK] skills.jsonc 已存在该技能，跳过注册")


def main():
    if not os.path.isdir(SKILL_SRC):
        print("[ERROR] 未找到技能目录 %s" % SKILL_SRC)
        sys.exit(1)
    accio_root = find_accio_root()
    if not accio_root:
        print("[ERROR] 未找到 Accio 登录状态文件 current-space.json，请确认已安装并登录 Accio Work")
        sys.exit(1)
    try:
        cs = json.load(open(accio_root, encoding="utf-8-sig"))
        account_id = str(cs.get("accountId", "") or "")
    except Exception as e:
        print("[ERROR] 读取 %s 失败：%s" % (accio_root, e))
        sys.exit(1)
    skills_dir = find_skills_dir(account_id)
    if not skills_dir:
        print("[ERROR] 未找到 agent-core/skills 目录，请确认已创建智能体")
        sys.exit(1)
    dest = os.path.join(skills_dir, SKILL_NAME)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(SKILL_SRC, dest)
    register(skills_dir, dest)
    print("")
    print("========================================")
    print("[完成] 技能已安装到：")
    print("  %s" % dest)
    print("")
    print("下一步：完全退出 Accio Work 后重新打开（不是最小化），即可使用该技能。")
    print("========================================")


if __name__ == "__main__":
    main()
