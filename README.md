<!--
 * @Author: anzaikk 599957546@qq.com
 * @Date: 2023-05-06 20:53:08
 * @LastEditors: anzaikk 599957546@qq.com
 * @LastEditTime: 2023-05-09 14:45:04
 * @FilePath: /hypertasy-search/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# hypertasy-search
## 简介
This is a hypertasy search.
## 程序运行
### 命令行运行
```
python main.py
```
### 开发工具推荐
开发工具推荐使用[vscode](https://code.visualstudio.com/)，对应的VScode的Debug配置
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
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