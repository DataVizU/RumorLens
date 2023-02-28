# RumorLens: Interactive Analysis and Validation of Suspected Rumors on Social Media

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
