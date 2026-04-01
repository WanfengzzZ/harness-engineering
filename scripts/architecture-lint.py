#!/usr/bin/env python3
"""
架构依赖检查脚本 v2.0

功能：
1. 验证分层依赖规则：Types → Config → Repo → Service → Runtime → UI
2. 检测循环依赖（层间）
3. Python 文件使用 AST 精确解析 import
4. TS/JS 文件使用增强正则匹配（含 dynamic import、re-export）
5. 生成违规报告，包含修复指导
"""

import os
import re
import ast
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

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
    'providers', 'utils', 'shared', 'common', 'lib', 'helpers',
}

# 文件路径到层的映射规则
LAYER_PATTERNS = {
    r'/types/': 'types',
    r'/type/': 'types',
    r'/interfaces/': 'types',
    r'/models/': 'types',
    r'/schemas/': 'types',
    r'/config/': 'config',
    r'/configuration/': 'config',
    r'/settings/': 'config',
    r'/repo/': 'repo',
    r'/repository/': 'repo',
    r'/repositories/': 'repo',
    r'/dal/': 'repo',
    r'/service/': 'service',
    r'/services/': 'service',
    r'/usecases/': 'service',
    r'/runtime/': 'runtime',
    r'/server/': 'runtime',
    r'/ui/': 'ui',
    r'/components/': 'ui',
    r'/pages/': 'ui',
    r'/views/': 'ui',
    r'/screens/': 'ui',
    r'/providers/': 'providers',
    r'/utils/': 'utils',
    r'/shared/': 'shared',
    r'/common/': 'common',
    r'/lib/': 'lib',
    r'/helpers/': 'helpers',
}

SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', 'dist', 'build',
    '.next', '.nuxt', 'coverage', '.venv', 'venv', 'env',
}

CODE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.py', '.mjs', '.cjs'}


def get_layer_from_path(file_path: str) -> str:
    """从文件路径推断所属层"""
    path_lower = file_path.lower().replace('\\', '/')
    for pattern, layer in LAYER_PATTERNS.items():
        if re.search(pattern, path_lower):
            return layer
    return 'unknown'


def extract_imports_python_ast(file_path: str) -> List[str]:
    """使用 AST 精确解析 Python import"""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except (SyntaxError, UnicodeDecodeError):
        pass
    return imports


def extract_imports_ts_js(file_path: str) -> List[str]:
    """使用增强正则解析 TS/JS import（含 dynamic import、re-export）"""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        patterns = [
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s*\([\'"]([^\'"]+)[\'"]\)',
            r'require\s*\([\'"]([^\'"]+)[\'"]\)',
            r'export\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
    except (UnicodeDecodeError, IOError):
        pass
    return imports


def extract_imports(file_path: str) -> List[str]:
    """根据文件类型选择解析方式"""
    ext = Path(file_path).suffix
    if ext == '.py':
        return extract_imports_python_ast(file_path)
    elif ext in {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs'}:
        return extract_imports_ts_js(file_path)
    return []


def check_import_validity(
    source_file: str,
    source_layer: str,
    import_path: str
) -> Tuple[bool, str]:
    """检查 import 是否违反分层规则"""
    
    # 跳过外部依赖（不以 . / @ 开头的都是外部包）
    if not import_path.startswith('.') and not import_path.startswith('/') and not import_path.startswith('@/'):
        return True, "外部依赖"
    
    # 跳过允许的横切关注点
    for allowed in ALLOWED_REVERSE_DEPS:
        if allowed in import_path.lower():
            return True, f"允许的横切依赖：{allowed}"
    
    target_layer = get_layer_from_path(import_path)
    if target_layer == 'unknown':
        return True, "未知层（跳过检查）"
    
    source_level = LAYER_ORDER.get(source_layer, -1)
    target_level = LAYER_ORDER.get(target_layer, -1)
    
    if source_level == -1 or target_level == -1:
        return True, "层级别未定义"
    
    if target_level >= source_level:
        return True, f"合法依赖：{source_layer} → {target_layer}"
    
    return False, f"违规依赖：{source_layer} 不能依赖 {target_layer}"


def check_file(file_path: str) -> List[Dict]:
    """检查单个文件的依赖"""
    violations = []
    source_layer = get_layer_from_path(file_path)
    if source_layer == 'unknown':
        return violations
    
    imports = extract_imports(file_path)
    for import_path in imports:
        is_valid, reason = check_import_validity(file_path, source_layer, import_path)
        if not is_valid:
            violations.append({
                'file': file_path,
                'import': import_path,
                'reason': reason,
                'source_layer': source_layer,
                'fix': '将依赖通过 Providers 注入，或移动代码到正确的层',
            })
    return violations


def build_layer_graph(root_dir: str) -> Dict[str, Set[str]]:
    """构建层级依赖图（用于循环依赖检测）"""
    graph = defaultdict(set)
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if Path(f).suffix not in CODE_EXTENSIONS:
                continue
            file_path = os.path.join(root, f)
            source_layer = get_layer_from_path(file_path)
            if source_layer == 'unknown' or source_layer in ALLOWED_REVERSE_DEPS:
                continue
            for imp in extract_imports(file_path):
                target_layer = get_layer_from_path(imp)
                if target_layer != 'unknown' and target_layer != source_layer and target_layer not in ALLOWED_REVERSE_DEPS:
                    graph[source_layer].add(target_layer)
    return dict(graph)


def detect_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """检测层间循环依赖"""
    cycles = []
    visited = set()

    def dfs(node, path, path_set):
        if node in path_set:
            idx = path.index(node)
            cycles.append(path[idx:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        path_set.add(node)
        for nb in graph.get(node, set()):
            dfs(nb, path, path_set)
        path.pop()
        path_set.discard(node)

    for node in graph:
        dfs(node, [], set())
    return cycles


def check_project(root_dir: str) -> Dict:
    """检查整个项目"""
    results = {
        'total_files': 0,
        'checked_files': 0,
        'violations': [],
        'by_layer': {},
        'cycles': [],
    }
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            if Path(file).suffix not in CODE_EXTENSIONS:
                continue
            file_path = os.path.join(root, file)
            results['total_files'] += 1
            violations = check_file(file_path)
            if violations:
                results['violations'].extend(violations)
                for v in violations:
                    layer = v['source_layer']
                    results['by_layer'][layer] = results['by_layer'].get(layer, 0) + 1
            results['checked_files'] += 1
    
    # 检测循环依赖
    graph = build_layer_graph(root_dir)
    results['cycles'] = detect_cycles(graph)
    return results


def format_report(results: Dict) -> str:
    """格式化检查报告"""
    report = []
    report.append("=" * 60)
    report.append("架构依赖检查报告 v2.0")
    report.append("=" * 60)
    report.append(f"总文件数：{results['total_files']}")
    report.append(f"已检查：{results['checked_files']}")
    report.append(f"违规数：{len(results['violations'])}")
    report.append(f"循环依赖：{len(results['cycles'])}")
    report.append("")
    
    if results['cycles']:
        report.append("🔄 循环依赖（严重）:")
        report.append("-" * 40)
        for cycle in results['cycles']:
            report.append(f"  {' → '.join(cycle)}")
        report.append("")
    
    if results['violations']:
        report.append("⚠️  分层违规:")
        report.append("-" * 60)
        for v in results['violations'][:20]:
            report.append(f"文件：{v['file']}")
            report.append(f"  依赖：{v['import']}")
            report.append(f"  原因：{v['reason']}")
            report.append(f"  修复：{v['fix']}")
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
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    print(f"开始检查项目架构依赖...")
    print(f"根目录：{root_dir}")
    print("")
    results = check_project(root_dir)
    report = format_report(results)
    print(report)
    if results['violations'] or results['cycles']:
        sys.exit(1)
    else:
        print("✅ 未发现架构依赖违规")
        sys.exit(0)


if __name__ == '__main__':
    main()
