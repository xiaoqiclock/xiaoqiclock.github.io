#!/usr/bin/env python3
"""
GitHub Actions 用索引页生成脚本
遍历指定目录，生成一个包含文件列表的 index.html
"""

import os
import sys
from pathlib import Path

# 获取命令行参数，如果没有则默认为当前目录
target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
output_file = target_dir / "index.html"

# 要忽略的文件和文件夹列表
ignore_list = {'.git', '.github', 'index.html', '.nojekyll'}

print(f"正在为目录 {target_dir} 生成索引...")
print(f"输出文件: {output_file}")

# 收集文件和文件夹
items = []
for item in target_dir.iterdir():
    if item.name in ignore_list:
        continue
    items.append({
        'name': item.name,
        'path': str(item.relative_to(target_dir)),
        'is_dir': item.is_dir()
    })

# 按名称排序，文件夹在前
items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))

# 生成 HTML 内容
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index of {target_dir}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.5; margin: 2rem; }}
        h1 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 0.5rem 0; }}
        a {{ text-decoration: none; color: #0366d6; }}
        a:hover {{ text-decoration: underline; }}
        .size {{ color: #666; font-size: 0.9em; margin-left: 1rem; }}
    </style>
</head>
<body>
    <h1>Index of {target_dir}</h1>
    <ul>
        <li><a href="../">../</a></li>
"""

for item in items:
    slash = "/" if item['is_dir'] else ""
    # 这里可以添加获取文件大小的代码，但需要更多处理，本例暂略
    file_size = "" # 例如: f"<span class='size'>({size})</span>"
    html_content += f"        <li><a href=\"{item['path']}\">{item['name']}{slash}</a>{file_size}</li>\n"

html_content += """    </ul>
</body>
</html>"""

# 写入 index.html 文件
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"成功生成 {output_file}")
