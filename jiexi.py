# test5.py - 学习解析网页
import requests
from bs4 import BeautifulSoup

print("🔧 准备解析工具...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get('https://movie.douban.com/top250', headers=headers)

if response.status_code == 200:
    print("✅ 拿到网页数据")
    
    # 用BeautifulSoup来解析网页
    soup = BeautifulSoup(response.text, 'html.parser')
    print("✅ 解析完成！")
    
    # 现在soup就是一个可以方便查找的结构了
    print("解析后的对象类型：", type(soup))
    
else:
    print("❌ 获取网页失败")