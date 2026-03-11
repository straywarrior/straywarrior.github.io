#!/usr/bin/env python3
"""遍历当前目录下的.md文件，检查title:前一行是否有layout: post，如果没有则添加
同时检查date:字段，如果只有日期则添加时间 08:00:00 +0800"""

import os
import re

# 匹配只有日期（无时间）的 date 字段
DATE_ONLY_PATTERN = re.compile(r'^date:\s*(\d{4}-\d{2}-\d{2})(\s*)$', re.MULTILINE)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找 front matter 的位置
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        print(f"  [跳过] 无 front matter: {filepath}")
        return False

    # 找到第二个 --- 的位置
    first_dash_index = 0
    second_dash_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            second_dash_index = i
            break

    if second_dash_index is None:
        print(f"  [跳过] front matter 未闭合: {filepath}")
        return False

    modified = False

    # 处理 date: 字段
    new_content, date_changed = process_date_field(content, second_dash_index)
    if date_changed:
        content = new_content
        modified = True

    # 重新读取 lines 用于后续处理
    lines = content.split('\n')

    # 在 front matter 内部查找 title:
    title_index = None
    for i in range(1, second_dash_index):
        if lines[i].startswith('title:'):
            title_index = i
            break

    if title_index is None:
        print(f"  [跳过] 未找到 title: {filepath}")
        return False

    # 检查 title: 前一行是否是 layout: post
    if title_index > 1 and lines[title_index - 1].strip() == 'layout: post':
        print(f"  [无需修改] 已有 layout: post: {filepath}")
        return modified

    # 插入 layout: post
    layout_line = 'layout: post\n'
    lines.insert(title_index, layout_line)
    modified = True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"  [已添加] layout: post: {filepath}")
    return modified


def process_date_field(content, second_dash_index):
    """检查并修改 date: 字段，如果只有日期则添加时间"""
    # 查找 front matter 中的 date: 行
    front_matter = '\n'.join(content.split('\n')[:second_dash_index + 1])

    # 匹配只有日期没有时间的 date: 字段
    match = DATE_ONLY_PATTERN.search(front_matter)
    if match:
        date_str = match.group(1)
        new_date_line = f"date: {date_str} 08:00:00 +0800"
        old_line = f"date: {date_str}"
        new_content = content.replace(old_line, new_date_line, 1)
        print(f"  [已修改] date: {date_str} -> {date_str} 08:00:00 +0800")
        return new_content, True

    return content, False

def main():
    md_files = [f for f in os.listdir('.') if f.endswith('.md')]

    if not md_files:
        print("当前目录下没有 .md 文件")
        return

    print(f"找到 {len(md_files)} 个 .md 文件，开始处理...\n")

    modified_count = 0
    for md_file in md_files:
        if process_file(md_file):
            modified_count += 1

    print(f"\n处理完成，共修改 {modified_count} 个文件")

if __name__ == '__main__':
    main()