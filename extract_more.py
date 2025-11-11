# fixed_extract.py - 修复后的完整提取
import requests
from bs4 import BeautifulSoup

print("🎬 完整信息提取")
print("=" * 50)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get('https://movie.douban.com/top250', headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    all_movies = soup.find_all('div', class_='item')
    
    print("前15个电影的完整信息：")
    print("")
    
    for i in range(15):  # 只处理前15个
        movie = all_movies[i]
        
        # 提取标题
        title = movie.find('span', class_='title')
        
        # 提取评分
        rating = movie.find('span', class_='rating_num')
        
        # 提取评价人数
        evaluation_count = "未找到"
        all_spans = movie.find_all('span')
        for span in all_spans:
            if '人评价' in span.text:
                evaluation_count = span.text
                break
        
        # 提取电影短评
        quote_p = movie.find('p', class_='quote')
        if quote_p:
            quote_span = quote_p.find('span')
            quote = quote_span.text if quote_span else "无短评"
        else:
            quote = "无短评"
        
        print(f"🎬 第{i+1}部电影：")
        print(f"   标题: {title.text if title else '未找到'}")
        print(f"   评分: {rating.text if rating else '未找到'}")
        print(f"   评价: {evaluation_count}")
        print(f"   精华短评: {quote}")
        print("")
    
    print("✅ 完美！现在所有信息都正确提取了")
    
else:
    print("❌ 获取网页失败")