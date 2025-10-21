<!--
 * @Author: anzaikk 599957546@qq.com
 * @Date: 2023-05-06 20:53:08
 * @LastEditors: anzaikk 599957546@qq.com
 * @LastEditTime: 2023-05-11 13:52:40
 * @FilePath: /hypertasy-search/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# hypertasy-search
## 简介
This is a hypertasy search.

本项目依赖以下两个项目
1. [crawler](https://github.com/Ard-Skelling/crawler) 爬虫模块
2. [nlp-prototype](https://github.com/Ard-Skelling/nlp-prototype) NLP模块

以上两个模块必须再本项目运行之前运行，与以上两个模块通信主要通过HTTP请求
## 程序运行
### 命令行运行
```
python main.py
```
### 开发工具推荐
开发工具推荐使用[vscode](https://code.visualstudio.com/)，对应的VScode的Debug配置
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--host=127.0.0.1", 
                "--port=8003", 
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```
将以上代码替换掉目录.vscode中的**launch.json**文件
### 关联前端
1. [Search-Louis](https://github.com/anzaikk/search-louis)