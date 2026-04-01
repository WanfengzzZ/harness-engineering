#!/usr/bin/env python3
"""
Agent 记忆清理和维护脚本

功能：
1. 扫描 .codebuddy/memory/ 目录中的记忆文件
2. 检测过时、重复、低价值的记忆
3. 建议归档或删除
4. 将高价值经验迁移到 docs/
"""

import os
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict


# 记忆文件的典型位置
MEMORY_DIRS = [
    '.codebuddy/memory',
    '.cursor/memory',
    '.claude/memory',
]

# 过时阈值
STALE_DAYS = 60
ARCHIVE_DAYS = 90


def find_memory_files(root_dir: str) -> List[str]:
    """查找所有记忆文件"""
    memory_files = []
    for mem_dir in MEMORY_DIRS:
        full_path = os.path.join(root_dir, mem_dir)
        if not os.path.exists(full_path):
            continue
        for root, dirs, files in os.walk(full_path):
            for f in files:
                if f.endswith(('.md', '.json', '.yaml', '.yml', '.txt')):
                    memory_files.append(os.path.join(root, f))
    return memory_files


def check_memory_age(file_path: str) -> Tuple[str, int]:
    """检查记忆年龄"""
    mtime = os.path.getmtime(file_path)
    age = (datetime.now() - datetime.fromtimestamp(mtime)).days

    if age > ARCHIVE_DAYS:
        return 'archive', age
    elif age > STALE_DAYS:
        return 'stale', age
    else:
        return 'fresh', age


def get_content_hash(file_path: str) -> str:
    """获取文件内容哈希（用于检测重复）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().lower()
            # 移除日期和时间戳，只比较核心内容
            content = re.sub(r'\d{4}-\d{2}-\d{2}', '', content)
            content = re.sub(r'\d{2}:\d{2}(:\d{2})?', '', content)
            return hashlib.md5(content.encode()).hexdigest()
    except Exception:
        return ''


def find_duplicates(memory_files: List[str]) -> List[List[str]]:
    """检测重复记忆"""
    hash_map = defaultdict(list)
    for f in memory_files:
        h = get_content_hash(f)
        if h:
            hash_map[h].append(f)
    return [files for files in hash_map.values() if len(files) > 1]


def estimate_value(file_path: str) -> Tuple[str, str]:
    """估算记忆价值"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 高价值标识
        high_value_patterns = [
            r'(架构|architecture|设计决策|design decision)',
            r'(教训|lesson|经验|experience|复盘)',
            r'(约定|convention|规范|standard)',
            r'(坑|pitfall|注意|warning|avoid)',
        ]

        # 低价值标识
        low_value_patterns = [
            r'(临时|temp|todo|fixme)',
            r'(测试|test|debug|调试)',
        ]

        for pat in high_value_patterns:
            if re.search(pat, content, re.IGNORECASE):
                return 'high', '包含架构决策/经验教训'

        for pat in low_value_patterns:
            if re.search(pat, content, re.IGNORECASE):
                return 'low', '临时/调试类记忆'

        # 按内容长度估算
        if len(content) < 50:
            return 'low', '内容过短'
        elif len(content) > 500:
            return 'high', '内容丰富'
        else:
            return 'medium', '一般记忆'

    except Exception:
        return 'unknown', '无法读取'


def format_report(results: Dict) -> str:
    """格式化报告"""
    report = []
    report.append("=" * 60)
    report.append("Agent 记忆维护报告")
    report.append("=" * 60)
    report.append(f"扫描文件数：{results['total']}")
    report.append(f"新鲜记忆：{results['fresh']}")
    report.append(f"过时记忆：{results['stale']}")
    report.append(f"待归档：{results['archive']}")
    report.append(f"重复组数：{results['duplicate_groups']}")
    report.append(f"高价值：{results['high_value']}")
    report.append(f"低价值：{results['low_value']}")
    report.append("")

    if results['stale_files']:
        report.append("⚠️  过时记忆（建议审查）:")
        report.append("-" * 40)
        for f, age in results['stale_files'][:10]:
            report.append(f"  {f} ({age}天)")
        report.append("")

    if results['archive_files']:
        report.append("📦 待归档记忆（建议迁移到 docs/ 或删除）:")
        report.append("-" * 40)
        for f, age in results['archive_files'][:10]:
            report.append(f"  {f} ({age}天)")
        report.append("")

    if results['duplicates']:
        report.append("🔄 重复记忆（建议合并）:")
        report.append("-" * 40)
        for group in results['duplicates'][:5]:
            report.append(f"  重复组：")
            for f in group:
                report.append(f"    - {f}")
        report.append("")

    if results['high_value_files']:
        report.append("⭐ 高价值记忆（建议迁移到 docs/）:")
        report.append("-" * 40)
        for f, reason in results['high_value_files'][:10]:
            report.append(f"  {f} - {reason}")
        report.append("")

    report.append("=" * 60)

    if results['stale'] + results['archive'] + results['duplicate_groups'] > 0:
        report.append("")
        report.append("建议操作：")
        report.append("1. 审查过时记忆，决定更新或删除")
        report.append("2. 将高价值经验迁移到 docs/ 目录")
        report.append("3. 合并重复记忆")
        report.append("4. 删除低价值过时记忆")

    return "\n".join(report)


def main():
    """主函数"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

    print("开始扫描 Agent 记忆文件...")
    print(f"根目录：{root_dir}")
    print("")

    memory_files = find_memory_files(root_dir)

    if not memory_files:
        print("未找到记忆文件。检查的目录：")
        for d in MEMORY_DIRS:
            print(f"  {os.path.join(root_dir, d)}")
        return

    results = {
        'total': len(memory_files),
        'fresh': 0, 'stale': 0, 'archive': 0,
        'stale_files': [], 'archive_files': [],
        'duplicate_groups': 0, 'duplicates': [],
        'high_value': 0, 'low_value': 0,
        'high_value_files': [], 'low_value_files': [],
    }

    for f in memory_files:
        status, age = check_memory_age(f)
        if status == 'fresh':
            results['fresh'] += 1
        elif status == 'stale':
            results['stale'] += 1
            results['stale_files'].append((f, age))
        elif status == 'archive':
            results['archive'] += 1
            results['archive_files'].append((f, age))

        value, reason = estimate_value(f)
        if value == 'high':
            results['high_value'] += 1
            results['high_value_files'].append((f, reason))
        elif value == 'low':
            results['low_value'] += 1
            results['low_value_files'].append((f, reason))

    duplicates = find_duplicates(memory_files)
    results['duplicate_groups'] = len(duplicates)
    results['duplicates'] = duplicates

    report = format_report(results)
    print(report)

    if results['stale'] + results['archive'] > 0:
        sys.exit(1)
    else:
        print("\n✅ 所有记忆状态良好")
        sys.exit(0)


if __name__ == '__main__':
    main()
