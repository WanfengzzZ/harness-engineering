#!/usr/bin/env python3
"""
文档验证脚本 v2.0

功能：
1. 检查文档年龄（是否过时）
2. 检测断链（引用不存在的文件）
3. 检查文档结构完整性
4. 支持 git blame 集成（可选）
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


STALE_WARN_DAYS = 30
STALE_ERROR_DAYS = 90


def find_doc_files(docs_dir: str) -> list:
    """查找所有文档文件"""
    doc_files = []
    if not os.path.exists(docs_dir):
        return doc_files
    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith('.md'):
                doc_files.append(os.path.join(root, f))
    return doc_files


def check_doc_age(file_path: str) -> tuple:
    """检查文档年龄"""
    mtime = os.path.getmtime(file_path)
    age = (datetime.now() - datetime.fromtimestamp(mtime)).days
    if age > STALE_ERROR_DAYS:
        return 'error', age
    elif age > STALE_WARN_DAYS:
        return 'warn', age
    return 'ok', age


def check_doc_age_git(file_path: str, root_dir: str) -> tuple:
    """使用 git log 检查文档最后修改时间（更精确）"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ct', '--', file_path],
            capture_output=True, text=True, cwd=root_dir, timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            ts = int(result.stdout.strip())
            age = (datetime.now() - datetime.fromtimestamp(ts)).days
            if age > STALE_ERROR_DAYS:
                return 'error', age
            elif age > STALE_WARN_DAYS:
                return 'warn', age
            return 'ok', age
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass
    return check_doc_age(file_path)


def extract_links(file_path: str) -> list:
    """提取文档中的内部链接"""
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        patterns = [
            r'\[([^\]]*)\]\(([^)]+)\)',
            r'`([^`]*\.md)`',
            r'`([^`]*/[^`]+)`',
        ]
        for pat in patterns:
            for match in re.finditer(pat, content):
                link = match.group(2) if match.lastindex >= 2 else match.group(1)
                if link and not link.startswith('http') and not link.startswith('#'):
                    links.append(link)
    except (UnicodeDecodeError, IOError):
        pass
    return links


def check_broken_links(file_path: str, root_dir: str) -> list:
    """检测断链"""
    broken = []
    doc_dir = os.path.dirname(file_path)
    for link in extract_links(file_path):
        clean_link = link.split('#')[0].split('?')[0]
        if not clean_link:
            continue
        if os.path.isabs(clean_link):
            target = os.path.join(root_dir, clean_link.lstrip('/'))
        else:
            target = os.path.join(doc_dir, clean_link)
        target = os.path.normpath(target)
        if not os.path.exists(target):
            broken.append({'link': link, 'target': target})
    return broken


def check_required_files(root_dir: str) -> list:
    """检查必需文件是否存在"""
    missing = []
    required = [
        ('AGENTS.md', '项目根目录'),
        ('docs/', '文档目录'),
    ]
    recommended = [
        ('ARCHITECTURE.md', '架构文档'),
        ('docs/design-docs/', '设计文档目录'),
        ('docs/exec-plans/', '执行计划目录'),
        ('docs/references/', '参考文档目录'),
    ]
    for path, desc in required:
        full = os.path.join(root_dir, path)
        if not os.path.exists(full):
            missing.append({'path': path, 'desc': desc, 'level': 'error'})
    for path, desc in recommended:
        full = os.path.join(root_dir, path)
        if not os.path.exists(full):
            missing.append({'path': path, 'desc': desc, 'level': 'warn'})
    return missing


def validate_docs(root_dir: str):
    """验证文档"""
    docs_dir = os.path.join(root_dir, 'docs')
    doc_files = find_doc_files(docs_dir)
    agents_md = os.path.join(root_dir, 'AGENTS.md')
    if os.path.exists(agents_md):
        doc_files.append(agents_md)

    use_git = os.path.isdir(os.path.join(root_dir, '.git'))

    print("=" * 60)
    print("文档验证报告 v2.0")
    print("=" * 60)
    print(f"扫描文件数：{len(doc_files)}")
    print(f"Git 集成：{'是' if use_git else '否'}")
    print("")

    errors = 0

    # 1. 检查必需文件
    missing = check_required_files(root_dir)
    if missing:
        print("📋 文件结构检查:")
        print("-" * 40)
        for m in missing:
            icon = '❌' if m['level'] == 'error' else '⚠️'
            print(f"  {icon} 缺少 {m['path']} ({m['desc']})")
            if m['level'] == 'error':
                errors += 1
        print("")

    # 2. 检查文档年龄
    stale = []
    for doc in doc_files:
        if use_git:
            status, age = check_doc_age_git(doc, root_dir)
        else:
            status, age = check_doc_age(doc)
        if status != 'ok':
            stale.append((doc, age, status))
            if status == 'error':
                errors += 1

    if stale:
        print("📅 文档年龄检查:")
        print("-" * 40)
        for doc, age, status in sorted(stale, key=lambda x: -x[1])[:15]:
            icon = '❌' if status == 'error' else '⚠️'
            rel = os.path.relpath(doc, root_dir)
            print(f"  {icon} {rel} ({age}天未更新)")
        print("")

    # 3. 检测断链
    all_broken = []
    for doc in doc_files:
        broken = check_broken_links(doc, root_dir)
        if broken:
            all_broken.extend([(doc, b) for b in broken])
            errors += len(broken)

    if all_broken:
        print("🔗 断链检测:")
        print("-" * 40)
        for doc, b in all_broken[:15]:
            rel = os.path.relpath(doc, root_dir)
            print(f"  ❌ {rel}")
            print(f"     链接: {b['link']}")
            print(f"     目标不存在: {b['target']}")
        print("")

    # 总结
    print("=" * 60)
    if errors > 0:
        print(f"发现 {errors} 个问题需要修复")
        print("\n建议：")
        print("1. 更新过时文档或标记为已归档")
        print("2. 修复断链引用")
        print("3. 创建缺失的必需文件")
        return 1
    else:
        print("✅ 所有文档检查通过")
        return 0


if __name__ == '__main__':
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    sys.exit(validate_docs(root_dir))
