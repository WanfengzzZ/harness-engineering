#!/usr/bin/env python3
"""
文档验证脚本 - 检查文档是否与代码同步
"""

import os
from pathlib import Path
from datetime import datetime, timedelta


def find_doc_files(docs_dir: str) -> list:
    """查找所有文档文件"""
    doc_files = []
    
    if not os.path.exists(docs_dir):
        return doc_files
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                doc_files.append(os.path.join(root, file))
    
    return doc_files


def check_doc_age(file_path: str) -> tuple:
    """检查文档年龄"""
    mtime = os.path.getmtime(file_path)
    doc_date = datetime.fromtimestamp(mtime)
    age = datetime.now() - doc_date
    
    if age > timedelta(days=90):
        return False, f"超过 90 天未更新（{age.days}天）"
    elif age > timedelta(days=30):
        return True, f"超过 30 天未更新（{age.days}天）"
    else:
        return True, "新鲜"


def validate_docs(root_dir: str):
    """验证文档"""
    docs_dir = os.path.join(root_dir, 'docs')
    doc_files = find_doc_files(docs_dir)
    
    print(f"找到 {len(doc_files)} 个文档文件")
    print("=" * 60)
    
    outdated = []
    for doc_file in doc_files:
        is_fresh, reason = check_doc_age(doc_file)
        if not is_fresh:
            outdated.append({
                'file': doc_file,
                'reason': reason,
            })
            print(f"❌ {doc_file}")
            print(f"   {reason}")
            print()
    
    print("=" * 60)
    print(f"发现 {len(outdated)} 个过时文档")
    
    if outdated:
        print("
建议：")
        print("1. 审查这些文档是否仍然准确")
        print("2. 更新或删除过时内容")
        print("3. 运行 doc-gardening 流程自动修复")
        return 1
    else:
        print("✅ 所有文档都是新鲜的")
        return 0


if __name__ == '__main__':
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    exit(validate_docs(root_dir))
