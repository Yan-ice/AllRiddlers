# 全员追忆 智能剧本生成器

一款可以快速爬取官方网站最新角色数据并生成智能全员追忆剧本(HTML)的项目。

**为什么要做这样一个东西？**

网上的全追剧本够不清晰X

网上的全追剧本不是最新的X

网上的全追剧本新手看了一脸蒙X

对，就是这样

## 项目结构
`config/` 存有剧本的基本设置。

`data/` 从官网爬取的所有角色数据（缓存）。

`htmls/` 存有所有剧本html的辅助功能，会被python脚本整合成一个大html。

`output/` 将保存生成的剧本。

`pysrc/` 存有所有主要python代码。

`util/` 存有一些乱七八糟但有用的东西，和项目本身关系不大）

`main.py` 生成器主程序，通过main.py执行各种功能。


## 快速上手

请确保你安装了python3.8以上，并建议在Ubuntu20.04环境运行。

1. Python 环境配置

```
pip install requests beautifulsoup4
```

2. 更新官方角色数据（如果需要）

```
python3 main.py fetch
```

为了不给服务器造成太大压力，爬取数据设置了2秒一条。

（请不要恶意爬虫哦）

3. 生成html剧本和对应json剧本

```
python3 main.py gen
```

然后就可以在项目目录下看到生成的**全员追忆.html**和**AllRidders.json**文件了。

## 待办清单

1. 从json文件fetch角色信息
2. 顺便也变成一个剧本生成器吧，不一定针对全追

## 参与维护/联系我们

(不是鱼子酱)邮箱：yan2364728692@gmail.com

欢迎给项目提交PR或共同成为维护者
