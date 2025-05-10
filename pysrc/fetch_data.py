# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from urllib.request import urlretrieve
import time
import json

def fetch_url(url):
    # 获取网页内容
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

jinxes = []

def code_team(x):
    if x.startswith('镇民'):
        return 'townsfolk'
    if x.startswith('外来者'):
        return 'outsider'
    if x.startswith('爪牙'):
        return 'minion'
    if x.startswith('恶魔'):
        return 'demon'
    if x.startswith('旅行者'):
        return 'traveller'
    if x.startswith('传奇角色'):
        return 'fabled'
    return 'unknown'

def fetch_character(name):
    root_dir = f"data/{name}"
    metadata = f"data/{name}/meta.json"
    remind = f"data/{name}/remind.json"

    if os.path.exists(metadata):
        ability_text = ''
        with open(metadata, "r", encoding="utf-8") as f:
            ability_text = f.readline()

    print(f"{metadata} not exist, fetching from official-site...")
    os.makedirs(root_dir, exist_ok=True)

    url = f"https://clocktower-wiki.gstonegames.com/index.php?title={name}"
    soup = fetch_url(url)

    alltext = soup.get_text().split('\n')

    ability_text = ''
    type_text = ''
    tag_text = ''
    story_text = ''
    mark = 0
    mark_xk = 0
    for check in alltext:
        if mark == 1:
            if len(check) > 1:
                ability_text = ability_text + check
            else:
                mark = -1
        if mark_xk == 1:
            if '：' in check:
                name2 = check.split("：")[0]
                jrule = check.split("：")[1]
                jinxes.append((name,name2,jrule))
            else:
                mark_xk = -1
        
        if '本页面目前没有内容' in check:
            print("Invalid: ", name)
            break
        if mark == 0 and check.startswith('角色能力'):
            mark = 1
        if check.startswith('角色类型：'):
            type_text = check[5:]
        if check.startswith('角色能力类型：'):
            tag_text = check[7:]
        if check.startswith('所属剧本：'):
            story_text = check[5:]

        if check.startswith('相克规则：'):
            mark_xk = 1

    img_url = ''

    img_tags = soup.find_all("img")
    for i, img in enumerate(img_tags):
        img_url = img.get("src")
        if not img_url or not img_url.startswith("/images/"):
            continue
        img_url = urljoin(url, img_url)  # 拼接完整 URL

        # with open(f"data/{name}/url.txt", "w", encoding="utf-8") as f:
        #     f.write(img_url)
        #     f.write('\n')
        #     f.write(url)

        try:
            urlretrieve(img_url, f'data/{name}/icon.png')
            # img_url = f'data/{name}/icon.png'
            break
        except Exception as e:
            print(f"下载失败：{img_url}，原因：{e}")
    
    meta = {
        'ability': ability_text,
        'team': code_team(type_text),
        'script': story_text,
        'tags': tag_text.split('、'),
        'image': img_url
    }

    with open(metadata, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)

    time.sleep(1)


# 手动整理角色列表时用到
# def fetch_character_list():
#     url = f"https://clocktower-wiki.gstonegames.com/index.php?title=恶魔"
#     soup = fetch_url(url)

#     ability_text = soup.get_text()
#     with open(f"character_list.txt", "w", encoding="utf-8") as f:
#         f.write(ability_text)


import time
def fetch_all_character():
    with open(f"list.txt", "r", encoding="utf-8") as f:
        datas = f.readlines()
        for i in datas:
            if not i.isspace() and len(i) != 0:
                fetch_character(i.replace('\n',''))

    with open(f"jinx.json", "w", encoding="utf-8") as f:
        json.dump({'jrule': jinxes}, f, ensure_ascii=False)
        