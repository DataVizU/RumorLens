# DataVisualization


[[CHI EA '22]](https://dl.acm.org/doi/10.1145/3491101.3519712)
[[arXiv]](https://arxiv.org/abs/2203.03098) 
[[Website]](https://rumorlens.datavizu.app/)


RumorLens integrates natural language processing (NLP) and other data processing techniques with visualization techniques to facilitate interactive analysis and validation of suspected rumors. We propose well-coordinated visualizations to provide users with three levels of details of suspected rumors: an overview displays both spatial distribution and temporal evolution of suspected rumors; a projection view leverages a metaphor-based glyph to represent each suspected rumor and further enable users to gain a quick understanding of their overall characteristics and similarity with each other; a propagation view visualizes the dynamic spreading details of a suspected rumor with a novel circular visualization design, and facilitates interactive analysis and validation of rumors in a compact manner.

## Overview

![](https://user-images.githubusercontent.com/54462604/213134657-d1b84783-bff9-43e2-b150-a6dc79f39b0c.png)

## Setup

```bash
npm install
```
```bash
npm run dev
```

## Participant

### Yifei Zhao([@FrankZH-1](https://github.com/FrankZH-1)): Propagation View, Post Details View

<details>
<summary>Raw repo record</summary>
<img src="https://user-images.githubusercontent.com/54462604/213143546-dfdc51ad-f070-4454-8265-455ae24a85bf.png">
</details>

### Mojie Tang([@morjyooo](https://github.com/morjyooo)): Topic Evolution View, Features Projection View

<details>
<summary>Raw repo record</summary>
<img src="https://user-images.githubusercontent.com/54462604/213143567-88455949-5127-4819-ba51-08215e3b012a.png">
</details>

### Hongxi Tao([@hongxitao](https://github.com/hongxitao)): Location Distribution View, Topic Evolution View

<details>
<summary>Raw repo record</summary>
<img src="https://user-images.githubusercontent.com/54462604/213143580-ba410d6d-fc97-43cf-bbf8-52b1d2bc1454.png">
</details>

### Jingyu Tang([volcano621](https://github.com/volcano621)): Refactor Frontend

### Qianhe Chen([@chenqianhe](https://github.com/chenqianhe)): Backend Part, DevOps

### Kehan Du([@lele1307](https://github.com/lele1307)): System Architecture

## Citation
```
@inproceedings{10.1145/3491101.3519712,
author = {Wang, Ran and Du, Kehan and Chen, Qianhe and Zhao, Yifei and Tang, Mojie and Tao, Hongxi and Wang, Shipan and Li, Yiyao and Wang, Yong},
title = {RumorLens: Interactive Analysis and Validation of Suspected Rumors on Social Media},
year = {2022},
isbn = {9781450391566},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3491101.3519712},
doi = {10.1145/3491101.3519712},
abstract = {With the development of social media, various rumors can be easily spread on the Internet and such rumors can have serious negative effects on society. Thus, it has become a critical task for social media platforms to deal with suspected rumors. However, due to the lack of effective tools, it is often difficult for platform administrators to analyze and validate rumors from a large volume of information on a social media platform efficiently. We have worked closely with social media platform administrators for four months to summarize their requirements of identifying and analyzing rumors, and further proposed an interactive visual analytics system, RumorLens, to help them deal with the rumor efficiently and gain an in-depth understanding of the patterns of rumor spreading. RumorLens integrates natural language processing (NLP) and other data processing techniques with visualization techniques to facilitate interactive analysis and validation of suspected rumors. We propose well-coordinated visualizations to provide users with three levels of details of suspected rumors: an overview displays both spatial distribution and temporal evolution of suspected rumors; a projection view leverages a metaphor-based glyph to represent each suspected rumor and further enable users to gain a quick understanding of their overall characteristics and similarity with each other; a propagation view visualizes the dynamic spreading details of a suspected rumor with a novel circular visualization design, and facilitates interactive analysis and validation of rumors in a compact manner. By using a real-world dataset collected from Sina Weibo, one case study with a domain expert is conducted to evaluate RumorLens. The results demonstrated the usefulness and effectiveness of our approach.},
booktitle = {Extended Abstracts of the 2022 CHI Conference on Human Factors in Computing Systems},
articleno = {232},
numpages = {7},
keywords = {Location Distribution, Human-Computer Collaboration, Social Media, Feature Projection, Visualization Design, Propagation View, Topic Evolution, Circular Design., Suspected Rumor},
location = {New Orleans, LA, USA},
series = {CHI EA '22}
}
```



## 后端

### 安装依赖

```shell
pip install -r requirement.txt
```

### 开发运行

```shell
uvicorn main:app --reload
```

### 格式化代码

```shell
black .
```

## 前端

```shell
cd frontend
```

### 安装依赖

```shell
npm install
```

### 运行

```shell
npm run dev
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Git hook 实现

由于该项目前后端混合在一个仓库，且前端部分在`.git`所在层级的下一级文件夹中，因此无法直接使用`husky`；
并且 Python 部分也没有对应的库来完成 hook 功能。

但是 hook 能力是由`git`提供的，因此我选择自己借助 hook 实现对应功能。

首先修改 git hook 的配置文件夹，将`.git/config`中的`hooksPath`改为`.husky`。

第二步，前端还是正常安装了 `commitlint`，对于只进行前端开发的同学还是借助 `commitlint` 实现校验。

第三步，后端则是使用 Python 实现了 commit msg 的校验，具体见`.husky/check_commit.py`。

```python
#!/usr/bin/env python
"""
Git commit hook:
 .git/hooks/commit-msg
 Check commit message according to angularjs guidelines:
  * https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#
"""
import sys
import re

valid_commit_types = [
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "test",
    "chore",
]

commit_file = sys.argv[1]
help_address = "https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#"
with open(commit_file) as commit:
    lines = commit.readlines()
    if len(lines) == 0:
        sys.stderr.write("\nEmpty commit message\n")
        sys.stderr.write("\n - Refer commit guide: %s\n\n" % help_address)
        sys.exit(1)
    # first line
    line = lines[0]
    m = re.search("^(.*): (.*)$", line)
    if not m or len(m.groups()) != 2:
        sys.stderr.write(
            "\nFirst commit message line (header) does not follow format: type: message\n"
        )
        sys.stderr.write("\n - Refer commit guide: %s\n\n" % help_address)
        sys.exit(1)
    commit_type, commit_message = m.groups()
    if commit_type not in valid_commit_types:
        sys.stderr.write(
            "\nCommit type not in valid ones: %s\n" % ", ".join(valid_commit_types)
        )
        sys.stderr.write("\n - Refer commit guide: %s\n\n" % help_address)
        sys.exit(1)
    if len(lines) > 1 and lines[1].strip():
        sys.stderr.write("\nSecond commit message line must be empty\n")
        sys.stderr.write("\n - Refer commit guide: %s\n\n" % help_address)
        sys.exit(1)
    if len(lines) > 2 and not lines[2].strip():
        sys.stderr.write("\nThird commit message line (body) must not be empty\n")
        sys.stderr.write("\n - Refer commit guide: %s\n\n" % help_address)
        sys.exit(1)
sys.exit(0)
```

第四步，实现`commit-msg`和`pre-commit`两阶段的钩子。

前者实现对msg格式的校验；首先尝试对后端开发情况进行校验，其次尝试对前端开发情况校验，并且保证前后端有一个环境进行了配置就可以完成校验。

```shell
python .husky/check_commit.py "$1" || echo 'Python check commit fail.'
cd frontend || exit
if [ -d 'node_modules' ]; then
  npm run check-commit
fi
```

后者实现代码格式化，同样是先尝试后端代码格式化，再尝试前端代码格式检查和格式化(ESLint)，同样保证前后端仅有一个环境在开发时就可以完成该环境的校验。

```shell
#!/bin/sh

black . || echo 'Python format fail.'
cd frontend || exit
if [ -d 'node_modules' ]; then
    npm run lint
fi
git add .
```

## 常用技术规范

- https://ak2fq2cgz5.feishu.cn/docx/UCMxdEcx6oxMP8xKq7XcDLsFnKb

