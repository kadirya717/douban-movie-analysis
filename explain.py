# explain.py - 详细解释每一步
import requests
from bs4 import BeautifulSoup

print("=== 第1步：准备工具 ===")
print("requests 工具：用来上网获取数据")
print("BeautifulSoup 工具：用来解析网页结构")
print("")

print("=== 第2步：伪装成浏览器 ===")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
print("headers 就像我们的'身份证'，告诉网站：'我是Chrome浏览器，不是机器人'")
print("")

print("=== 第3步：获取网页 ===")
response = requests.get('https://movie.douban.com/top250', headers=headers)
print("这行代码的意思是：带着身份证去豆瓣网站要数据")
print("")

print("=== 第4步：检查是否成功 ===")
if response.status_code == 200:
    print("状态码200 = '成功拿到数据'")
    print("就像敲门后对方说'请进'")
    print("")
    
    print("=== 第5步：开始解析 ===")
    print("现在 response.text 里面是：")
    print("--- 这是一堆乱七八糟的HTML代码 ---")
    print("<html><head>...</head><body><div>...</div></body></html>")
    print("--- 人类很难直接阅读 ---")
    print("")
    
    print("=== 第6步：使用BeautifulSoup整理 ===")
    soup = BeautifulSoup(response.text, 'html.parser')
    print("BeautifulSoup 开始工作了...")
    print("它正在：")
    print("1. 找到所有的 <div>、<span> 标签")
    print("2. 理清它们之间的父子关系") 
    print("3. 把乱糟糟的代码变成整齐的树状结构")
    print("")
    
    print("=== 第7步：理解解析结果 ===")
    print("解析完成！现在 soup 是一个：")
    print("<class 'bs4.BeautifulSoup'>")
    print("")
    print("这表示：")
    print("✓ soup 已经不是一个普通的文字字符串了")
    print("✓ soup 是一个'智能对象'，知道网页的结构")
    print("✓ 我们可以用简单的方法找到想要的内容")
    print("")
    
    print("=== 举个例子 ===")
    print("整理前：需要在一堆文字里人工寻找")
    print("整理后：可以直接问 soup：'请给我所有电影标题'")
    
else:
    print("状态码不是200 = '访问被拒绝'")