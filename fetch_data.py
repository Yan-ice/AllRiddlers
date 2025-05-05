# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from urllib.request import urlretrieve
import time

def fetch_url(url):
    # 获取网页内容
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def fetch_character(name):
    if os.path.isdir(f"data/{name}"):
        ability_text = ''
        with open(f"data/{name}/meta.txt", "r", encoding="utf-8") as f:
            ability_text = f.readline()
        return (ability_text, f'data/{name}/icon.png')

    print(f"data/{name} not exist, fetching from official-site...")
    os.makedirs(f"data/{name}", exist_ok=True)

    url = f"https://clocktower-wiki.gstonegames.com/index.php?title={name}"
    soup = fetch_url(url)

    alltext = soup.get_text().split('\n')

    ability_text = ''
    type_text = ''
    tag_text = ''
    story_text = ''
    mark = 0
    for check in alltext:
        if mark == 1:
            if len(check) > 1:
                ability_text = ability_text + check
            else:
                mark = -1
        if mark == 0 and check.startswith('角色能力'):
            mark = 1
        if check.startswith('角色类型：'):
            type_text = check[5:]
        if check.startswith('角色能力类型：'):
            tag_text = check[7:]
        if check.startswith('所属剧本：'):
            story_text = check[5:]

    with open(f"data/{name}/meta.txt", "w", encoding="utf-8") as f:
        f.write(type_text)
        f.write('\n')
        f.write(ability_text)
        f.write('\n')
        f.write(tag_text)
        f.write('\n')
        f.write(story_text)

    img_url = ''

    img_tags = soup.find_all("img")
    for i, img in enumerate(img_tags):
        img_url = img.get("src")
        if not img_url or not img_url.startswith("/images/"):
            continue
        img_url = urljoin(url, img_url)  # 拼接完整 URL

        with open(f"data/{name}/url.txt", "w", encoding="utf-8") as f:
            f.write(img_url)
            f.write('\n')
            f.write(url)

        try:
            urlretrieve(img_url, f'data/{name}/icon.png')
            img_url = f'data/{name}/icon.png'
            break
        except Exception as e:
            print(f"下载失败：{img_url}，原因：{e}")
    time.sleep(2)
    return (ability_text, img_url)


# 手动整理角色列表时用到
# def fetch_character_list():
#     url = f"https://clocktower-wiki.gstonegames.com/index.php?title=恶魔"
#     soup = fetch_url(url)

#     ability_text = soup.get_text()
#     with open(f"character_list.txt", "w", encoding="utf-8") as f:
#         f.write(ability_text)


import time

with open(f"characters/villager_list.txt", "r", encoding="utf-8") as f:
    datas = f.readline().split(' ')
    for i in datas:
        if not i.isspace() and len(i) != 0:
            ability, icon_url = fetch_character(i)

with open(f"characters/outsider_list.txt", "r", encoding="utf-8") as f:
    datas = f.readline().split(' ')
    for i in datas:
        if not i.isspace() and len(i) != 0:
            ability, icon_url = fetch_character(i)

with open(f"characters/zhuaya_list.txt", "r", encoding="utf-8") as f:
    datas = f.readline().split(' ')
    for i in datas:
        if not i.isspace() and len(i) != 0:
            ability, icon_url = fetch_character(i)

with open(f"characters/daemon_list.txt", "r", encoding="utf-8") as f:
    datas = f.readline().split(' ')
    for i in datas:
        if not i.isspace() and len(i) != 0:
            ability, icon_url = fetch_character(i)