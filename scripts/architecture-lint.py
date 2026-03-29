#!/usr/bin/env python3
"""
架构依赖检查脚本

验证代码是否遵循分层依赖规则：
Types → Config → Repo → Service → Runtime → UI
         ↓          ↓         ↓         ↓
      Providers（横切关注点）
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# 定义层顺序（数字越小越底层）
LAYER_ORDER = {
    'types': 0,
    'config': 1,
    'repo': 2,
    'service': 3,
    'runtime': 4,
    'ui': 5,
}

# 允许的反向依赖（Providers 等横切关注点）
ALLOWED_REVERSE_DEPS = {
    'providers',
    'utils',
    'shared',
}

# 文件路径到层的映射规则
LAYER_PATTERNS = {
    r'/types/': 'types',
    r'/type/': 'types',
    r'/interfaces/': 'types',
    r'/config/': 'config',
    r'/configuration/': 'config',
    r'/repo/': 'repo',
    r'/repository/': 'repo',
    r'/dal/': 'repo',
    r'/service/': 'service',
    r'/services/': 'service',
    r'/runtime/': 'runtime',
    r'/ui/': 'ui',
    r'/components/': 'ui',
    r'/pages/': 'ui',
    r'/providers/': 'providers',
    r'/utils/': 'utils',
    r'/shared/': 'shared',
}


def get_layer_from_path(file_path: str) -> str:
    """从文件路径推断所属层"""
    path_lower = file_path.lower()
    
    for pattern, layer in LAYER_PATTERNS.items():
        if re.search(pattern, path_lower):
            return layer
    
    return 'unknown'


def extract_imports(file_path: str) -> List[str]:
    """从文件中提取 import 语句"""
    imports = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 匹配各种 import 语句
        import_patterns = [
            r'import\s+.*?\s+from\s+['"]([^'"]+)['"]',  # ES6 import
            r'require\(['"]([^'"]+)['"]\)',  # CommonJS require
            r'from\s+([^\s]+)\s+import',  # Python import
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return imports


def check_import_validity(
    source_file: str,
    source_layer: str,
    import_path: str
) -> Tuple[bool, str]:
    """检查 import 是否违反分层规则"""
    
    # 跳过外部依赖
    if not import_path.startswith('.') and not import_path.startswith('/'):
        return True, "外部依赖"
    
    # 跳过允许的横切关注点
    for allowed in ALLOWED_REVERSE_DEPS:
        if allowed in import_path.lower():
            return True, f"允许的横切依赖：{allowed}"
    
    # 推断目标层
    target_layer = get_layer_from_path(import_path)
    
    # 未知层跳过检查
    if target_layer == 'unknown':
        return True, "未知层（跳过检查）"
    
    # 检查依赖方向
    source_level = LAYER_ORDER.get(source_layer, -1)
    target_level = LAYER_ORDER.get(target_layer, -1)
    
    if source_level == -1 or target_level == -1:
        return True, "层级别未定义"
    
    # 允许同层依赖和向前依赖
    if target_level >= source_level:
        return True, f"合法依赖：{source_layer} → {target_layer}"
    
    # 反向依赖 - 违规
    return False, f"违规依赖：{source_layer} 不能依赖 {target_layer}"


def check_file(file_path: str) -> List[Dict]:
    """检查单个文件的依赖"""
    violations = []
    
    source_layer = get_layer_from_path(file_path)
    if source_layer == 'unknown':
        return violations
    
    imports = extract_imports(file_path)
    
    for import_path in imports:
        is_valid, reason = check_import_validity(
            file_path, source_layer, import_path
        )
        
        if not is_valid:
            violations.append({
                'file': file_path,
                'import': import_path,
                'reason': reason,
                'source_layer': source_layer,
            })
    
    return violations


def check_project(root_dir: str) -> Dict:
    """检查整个项目"""
    results = {
        'total_files': 0,
        'checked_files': 0,
        'violations': [],
        'by_layer': {},
    }
    
    # 遍历项目文件
    for root, dirs, files in os.walk(root_dir):
        # 跳过 node_modules 等目录
        dirs[:] = [d for d in dirs if d not in [
            'node_modules', 
            '.git', 
            '__pycache__',
            'dist',
            'build',
        ]]
        
        for file in files:
            if not file.endswith(('.ts', '.tsx', '.js', '.jsx', '.py')):
                continue
            
            file_path = os.path.join(root, file)
            results['total_files'] += 1
            
            violations = check_file(file_path)
            if violations:
                results['violations'].extend(violations)
                
                # 按层统计
                for v in violations:
                    layer = v['source_layer']
                    results['by_layer'][layer] = results['by_layer'].get(layer, 0) + 1
            
            results['checked_files'] += 1
    
    return results


def format_report(results: Dict) -> str:
    """格式化检查报告"""
    report = []
    report.append("=" * 60)
    report.append("架构依赖检查报告")
    report.append("=" * 60)
    report.append(f"总文件数：{results['total_files']}")
    report.append(f"已检查：{results['checked_files']}")
    report.append(f"发现违规：{len(results['violations'])}")
    report.append("")
    
    if results['violations']:
        report.append("违规详情:")
        report.append("-" * 60)
        
        for v in results['violations'][:20]:  # 只显示前 20 个
            report.append(f"文件：{v['file']}")
            report.append(f"  依赖：{v['import']}")
            report.append(f"  原因：{v['reason']}")
            report.append("")
        
        if len(results['violations']) > 20:
            report.append(f"... 还有 {len(results['violations']) - 20} 个违规")
    
    if results['by_layer']:
        report.append("")
        report.append("按层统计:")
        for layer, count in sorted(results['by_layer'].items()):
            report.append(f"  {layer}: {count} 个违规")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    """主函数"""
    import sys
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"开始检查项目架构依赖...")
    print(f"根目录：{root_dir}")
    print("")
    
    results = check_project(root_dir)
    report = format_report(results)
    
    print(report)
    
    # 如果有违规，返回非零退出码
    if results['violations']:
        sys.exit(1)
    else:
        print("✅ 未发现架构依赖违规")
        sys.exit(0)


if __name__ == '__main__':
    main()
