import os
import json
from pysrc.local_cache import *

VERSION = 'v1.1'

REMOTE = True

def sort_func(x):
        if x.startswith('towns'):
            return 1
        if x.startswith('outsid'):
            return 2
        if x.startswith('minion'):
            return 3
        if x.startswith('demon'):
            return 4
        if x.startswith('travel'):
            return 5
        if x.startswith('fable'):
            return 6
        return 7

def generate_html_output():
    root_dir = 'data'
    # 获取所有文件
    data_files = load_character_list

    team_map = {}
    datas = []
    with open("config/team_name.json", "r") as f:
        team_map = json.load(f)

    # 添加每张图片到 HTML 中
    for data_name in data_files:
        data_path = os.path.join(root_dir, data_name).replace("\\", "/")  # 兼容 Windows 路径
        icon_path = os.path.join(data_path, 'icon.png').replace("\\", "/")
        metadata_path = os.path.join(data_path, 'meta.json').replace("\\", "/")
        
        metadata = {}
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            metadata['name'] = data_name

        if not REMOTE:
            metadata['image'] = os.path.join(data_path, 'icon.png').replace("\\", "/")

        datas.append(
            metadata
        )

    datas.sort(key=lambda x: sort_func(x['team'])) 

    # 生成 HTML
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>全员追忆</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                font-family: sans-serif;
                padding: 20px;
                background-color: #f4f4f4;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
                gap: 10px;
            }
            .item {
                background-color: white;
                border-radius: 0px;
                padding: 0px;
                display: flex; /* 横向排列 */
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .item img {
                width: 70px;
                height: 70px;
                object-fit: contain;
            }
            .item p {
                text-align: left;
                margin-right: 20px;
                margin-top: 10px;
                font-size: 12px;
                color: #333;
            }

            /* Collapsible Filter Styling */
            details > summary {
                list-style: none; /* Remove default marker */
                cursor: pointer;
                padding: 10px;
                background-color: #f9fafb; /* Light gray background for summary */
                border-radius: 8px;
                font-weight: 600;
                color: #1f2937; /* Dark gray text */
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            details > summary::-webkit-details-marker {
                display: none; /* Hide marker in Chrome/Safari */
            }
            details > summary::after { /* Custom arrow indicator */
                content: '▼'; /* Down arrow */
                font-size: 0.8em;
                transition: transform 0.2s ease-in-out;
            }
            details[open] > summary::after {
                transform: rotate(180deg); /* Rotate arrow when open */
            }
        </style>
    </head>
    <body>
        <h1 class="text-3xl font-bold mb-6 text-center text-blue-700">全员追忆智能剧本</h1>

    <details class="mb-6 bg-white rounded-lg shadow overflow-hidden">
        <summary class="text-lg">
            <span>筛选与排序选项</span>
            </summary>
        <div class="p-4">
    """
    with open("htmls/util.html", "r", encoding="utf-8") as f:
        html += f.read()

    with open("htmls/choice_group.html", "r", encoding="utf-8") as f:
        html += f.read()

    with open("htmls/sort_method.html", "r", encoding="utf-8") as f:
        html += f.read()
        
    with open("htmls/tag_choose.html", "r", encoding="utf-8") as f:
        html += f.read()
        
    html += """ 
    </div>
    </details>

    <br><hr><div class="grid" id="grid"> 
    """

    # 添加每个图标+文字组合
    for item in datas:
        tag_seri = ''
        for a in item['tags']:
            tag_seri = tag_seri + a + ' '
        html += f"""
            <div class="item" data-name={item['name']} data-team={sort_func(item['team'])} data-tag={tag_seri} >
                <img src="{item['image']}" alt="{item['name']}"> 
                <p> <b>{item['name']}</b> {team_map[item['team']]} <br> {item['ability']}</p>
            </div>
        """

    # 结束 HTML

    html += """
    <script>

    var items_all;

    function init() {
        const grid = document.getElementById('grid');
        items_all = Array.from(grid.getElementsByClassName('item'));
        console.log("初始化逻辑已执行。");
    }

    // 页面 DOM 加载完成后执行 init
    document.addEventListener("DOMContentLoaded", init);

    function update() {
        const grid = document.getElementById('grid');
        
        grid.replaceChildren();
        var items = Array.from(items_all);
        
        // 按 data-name 排序
        items.sort(rule_sort);
        
        items = items.filter(rule_type_filter)

        items = items.filter(rule_tag_filter)

        if (items.length == 0){
            
        }else{
            items.forEach(item => grid.appendChild(item));
        }
        
    }

    </script>
    """
    html += f"""
        </div>
    <hr>
    <p class="text-center text-sm text-gray-500">
    {VERSION} by 不是鱼子酱 & Gemini | 2025.05.06
    </p>
    """

    os.makedirs(f"output", exist_ok=True)

    # 保存为 HTML 文件
    with open(f"output/全员追忆{VERSION}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已生成 output/全员追忆{VERSION}.html 文件，可以用浏览器打开查看效果。")
