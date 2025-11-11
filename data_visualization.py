# data_visualization.py - 学习数据可视化
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import re

# 设置中文字体，让图表能显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

print("📊 学习数据可视化")
print("=" * 50)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get('https://movie.douban.com/top250', headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    all_movies = soup.find_all('div', class_='item')
    
    movies_data = []
    
    for i, movie in enumerate(all_movies, 1):
        title_span = movie.find('span', class_='title')
        title = title_span.text if title_span else "未知标题"
        
        rating_span = movie.find('span', class_='rating_num')
        rating = rating_span.text if rating_span else "0"
        
        evaluation_count = "0"
        all_spans = movie.find_all('span')
        for span in all_spans:
            if '人评价' in span.text:
                num_match = re.search(r'(\d+)', span.text)
                if num_match:
                    evaluation_count = num_match.group(1)
                break
        
        movie_info = {
            '排名': i,
            '电影标题': title,
            '评分': float(rating),
            '评价人数': int(evaluation_count)
        }
        
        movies_data.append(movie_info)
    
    df = pd.DataFrame(movies_data)
    
    print("✅ 数据准备完成，开始制作图表...")
    
    # 创建画布，包含多个子图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('豆瓣电影TOP250数据分析', fontsize=16, fontweight='bold')
    
    # 图表1：评分分布直方图
    print("1. 制作评分分布图...")
    axes[0, 0].hist(df['评分'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('评分分布', fontweight='bold')
    axes[0, 0].set_xlabel('评分')
    axes[0, 0].set_ylabel('电影数量')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 图表2：前10名电影评分
    print("2. 制作TOP10电影评分图...")
    top10 = df.head(10)
    axes[0, 1].barh(top10['电影标题'], top10['评分'], color='lightcoral')
    axes[0, 1].set_title('TOP10电影评分', fontweight='bold')
    axes[0, 1].set_xlabel('评分')
    
    # 图表3：评价人数最多的10部电影
    print("3. 制作评价人数TOP10图...")
    top10_popular = df.nlargest(10, '评价人数')
    axes[1, 0].barh(top10_popular['电影标题'], top10_popular['评价人数']/10000, color='lightgreen')
    axes[1, 0].set_title('评价人数TOP10 (单位: 万)', fontweight='bold')
    axes[1, 0].set_xlabel('评价人数 (万)')
    
    # 图表4：评分与评价人数的关系
    print("4. 制作评分vs评价人数散点图...")
    axes[1, 1].scatter(df['评分'], df['评价人数']/10000, alpha=0.6, color='purple')
    axes[1, 1].set_title('评分 vs 评价人数', fontweight='bold')
    axes[1, 1].set_xlabel('评分')
    axes[1, 1].set_ylabel('评价人数 (万)')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('douban_analysis.png', dpi=300, bbox_inches='tight')
    print("\n🎉 图表制作完成！已保存为: douban_analysis.png")
    
    # 显示图表
    plt.show()
    
    # 数据洞察
    print("\n🔍 数据洞察:")
    print(f"• 评分范围: {df['评分'].min()} - {df['评分'].max()}")
    print(f"• 平均评分: {df['评分'].mean():.2f}")
    print(f"• 最受欢迎电影: {df.loc[df['评价人数'].idxmax(), '电影标题']}")
    print(f"• 评分最高电影: {df.loc[df['评分'].idxmax(), '电影标题']}")
    
else:
    print("❌ 获取网页失败")