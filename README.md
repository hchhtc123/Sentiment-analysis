# PaddleHub实战：中文微情感分析系统

# 一.项目简介：
本项目主要基于PaddleHub通过预训练模型Erine-tiny在中文7情感分类数据集OCEMOTION上进行微调训练从而实现较为精确的情感7分类任务：sadness、happiness、disgust、anger、like、surprise、fear。

在完成模型部署后，基于PyQt5完成了项目可视化界面的开发，支持支持单条和批量文本细粒度情感分类预测。

同时还完成了该项目前后端分离式的web端部署，所用技术栈：前端：Vue+Element UI；后端：Flask+PaddleHub。

通过微情感分析技术更好地挖掘文本中包含的微情感，具有前沿性和广泛的应用价值。同时还提供完整项目教程，带你玩转一个完整NLP项目开发！

## 总技术路线：

![image](https://github.com/hchhtc123/Sentiment-analysis/blob/main/show_picture/%E6%8A%80%E6%9C%AF%E8%B7%AF%E7%BA%BF.png)

# 二.项目效果演示：

## 2.1 PyQt5 GUI界面：
### 项目演示视频：https://www.bilibili.com/video/BV1944y1C7FQ/

### 单条文本分类预测：
![image](https://github.com/hchhtc123/Sentiment-analysis/blob/main/show_picture/GUI-%E5%8D%95%E6%9D%A1%E9%A2%84%E6%B5%8B.png)

### 批量文本分类预测：
![image](https://github.com/hchhtc123/Sentiment-analysis/blob/main/show_picture/GUI-%E6%89%B9%E9%87%8F%E9%A2%84%E6%B5%8B.png)

## 2.2 前后端分离式Web端：
### 项目演示视频：https://www.bilibili.com/video/BV1R44y1v7Dh/

### 界面演示：
![image](https://github.com/hchhtc123/Sentiment-analysis/blob/main/show_picture/web-%E9%A2%84%E6%B5%8B.png)


# 三.项目运行说明：

项目主目录分为Ernie-model、PyQt5-GUI、webproject三大文件夹。

1.Ernie-model存放训练好的模型参数，训练细节查看https://aistudio.baidu.com/aistudio/projectdetail/2211726。

2.PyQt5-GUI为基于PyQt5构建的可视化界面，该模块运行查看对应目录提供的'项目必读说明.txt'文件。

3.webproject为项目的web端部署，分为FrontEnd和BackEnd即前端界面和后端服务两大模块，该模块运行同样查看对应目录提供的"项目必读说明.txt"文件。

# 四.AI Studio项目地址及教程：

1.PaddleHub实战：基于OCEMOTION的中文微情感分析系统
 
 https://aistudio.baidu.com/aistudio/projectdetail/2211726

 2.前后端分离式NLP微情感分析平台
 
 https://aistudio.baidu.com/aistudio/projectdetail/2507681
 
 # 五.作者简介：
 
> 项目作者：炼丹师233
 
> AI Studio个人主页：https://aistudio.baidu.com/aistudio/personalcenter/thirdview/330406
 
> 飞桨开发者技术专家 PPDE

> 个人荣誉：软件杯国赛三等奖、计算机设计大赛国赛三等奖
 
> 主要方向：搞开发，主攻NLP和数据挖掘比赛或项目


