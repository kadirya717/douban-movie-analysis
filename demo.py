# demo.py - 实际演示解析效果
import requests
from bs4 import BeautifulSoup

print("🎬 实际演示：从乱码到有用信息")
print("=" * 50)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get('https://movie.douban.com/top250', headers=headers)

if response.status_code == 200:
    # 解析网页
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("✅ 解析完成！现在演示如何提取信息")
    print("")
    
    # 演示1：找到第一个电影标题
    print("🔍 演示1：找到第一个电影标题")
    print("方法：soup.find('span', class_='title')")
    
    first_title = soup.find('span', class_='title')
    print(f"找到的结果：{first_title}")
    print(f"提取文字：{first_title.text}")
    print("")
    
    # 演示2：找到所有电影卡片
    print("🔍 演示2：找到所有电影卡片") 
    print("方法：soup.find_all('div', class_='item')")
    
    all_movies = soup.find_all('div', class_='item')
    print(f"找到 {len(all_movies)} 个电影卡片")
    print("")
    
    # 演示3：提取前3个电影标题
    print("🔍 演示3：提取前3个电影标题")
    for i in range(3):
        movie = all_movies[i]
        title = movie.find('span', class_='title')
        print(f"第{i+1}部电影：{title.text}")
    
else:
    print("❌ 获取网页失败")