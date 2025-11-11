# save_to_csv.py - 学习保存数据到CSV文件
import requests
from bs4 import BeautifulSoup
import pandas as pd  # 这是处理表格数据的专业工具箱

print("💾 学习保存数据到CSV文件")
print("=" * 50)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get('https://movie.douban.com/top250', headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    all_movies = soup.find_all('div', class_='item')
    
    print(f"找到 {len(all_movies)} 部电影，开始提取数据...")
    
    # 创建一个空列表来存储所有电影数据
    movies_data = []
    
    for i, movie in enumerate(all_movies, 1):
        # 提取信息
        title_span = movie.find('span', class_='title')
        title = title_span.text if title_span else "未知标题"
        
        rating_span = movie.find('span', class_='rating_num')
        rating = rating_span.text if rating_span else "无评分"
        
        # 提取评价人数（只保留数字）
        evaluation_count = "0"
        all_spans = movie.find_all('span')
        for span in all_spans:
            if '人评价' in span.text:
                # 用正则表达式提取纯数字
                import re
                num_match = re.search(r'(\d+)', span.text)
                if num_match:
                    evaluation_count = num_match.group(1)
                break
        
        # 提取精华短评
        quote_p = movie.find('p', class_='quote')
        if quote_p:
            quote_span = quote_p.find('span')
            short_comment = quote_span.text if quote_span else "无短评"
        else:
            short_comment = "无短评"
        
        # 把数据整理成字典格式
        movie_info = {
            '排名': i,
            '电影标题': title,
            '评分': float(rating),  # 转换成数字，方便后续分析
            '评价人数': int(evaluation_count),  # 转换成数字
            '精华短评': short_comment
        }
        
        movies_data.append(movie_info)
        
        # 显示进度
        if i <= 3:
            print(f"✅ 已提取: {title}")
    
    print(f"\n📊 数据提取完成！共 {len(movies_data)} 部电影")
    
    # 使用pandas创建数据框（类似Excel表格）
    print("\n🛠️ 正在创建数据表格...")
    df = pd.DataFrame(movies_data)
    
    # 显示表格预览
    print("\n📋 数据预览（前5行）:")
    print(df.head())
    
    # 保存为CSV文件
    csv_filename = 'douban_top250_movies.csv'
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n🎉 成功保存到文件: {csv_filename}")
    print("💡 你可以用Excel打开这个文件查看数据！")
    
    # 显示一些基本统计信息
    print(f"\n📈 基本统计:")
    print(f"平均评分: {df['评分'].mean():.2f}")
    print(f"总评价人数: {df['评价人数'].sum():,} 人")
    print(f"最高评分: {df['评分'].max()}")
    print(f"最低评分: {df['评分'].min()}")
    
else:
    print("❌ 获取网页失败")