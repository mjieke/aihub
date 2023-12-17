# readme

常用 AI 网站收集站

## 网页操作

1. 添加新链接步骤，例如添加 www.example.com，在 toolkits/aibot/aibot_1_url.json 中添加

```json
   "https://www.example.com/": {},
```

2. 运行代码，截取网页首页，提取标题

```shell
cd toolkits/
python process.py
```

3. 运行代码，按照模板生成新网页

```shell
python generate.py
```

4. 可以在 toolkits/aibot/aibot_1_url.json 中手动添加网页信息，类别信息
