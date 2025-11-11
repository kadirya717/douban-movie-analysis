# data_enhancement.py - 数据清洗与增强
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

print("🔧 数据清洗与增强")
print("=" * 50)

def crawl_douban_top250():
    """爬取豆瓣TOP250数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get('https://movie.douban.com/top250', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_movies = soup.find_all('div', class_='item')
    
    movies_data = []
    
    for i, movie in enumerate(all_movies, 1):
        # 提取基本信息
        title_span = movie.find('span', class_='title')
        title = title_span.text if title_span else "未知标题"
        
        rating_span = movie.find('span', class_='rating_num')
        rating = rating_span.text if rating_span else "0"
        
        # 提取评价人数
        evaluation_count = "0"
        all_spans = movie.find_all('span')
        for span in all_spans:
            if '人评价' in span.text:
                num_match = re.search(r'(\d+)', span.text)
                if num_match:
                    evaluation_count = num_match.group(1)
                break
        
        # 提取短评
        quote_p = movie.find('p', class_='quote')
        if quote_p:
            quote_span = quote_p.find('span')
            short_comment = quote_span.text if quote_span else "无短评"
        else:
            short_comment = "无短评"
        
        # 提取导演和年份信息（新增！）
        info_p = movie.find('p', class_='')
        if info_p:
            info_text = info_p.get_text()
            # 简单的年份提取（实际项目可以用更复杂的方法）
            year_match = re.search(r'(\d{4})', info_text)
            year = year_match.group(1) if year_match else "未知"
        else:
            year = "未知"
        
        movie_info = {
            '排名': i,
            '电影标题': title,
            '评分': float(rating),
            '评价人数': int(evaluation_count),
            '上映年份': year,
            '精华短评': short_comment,
            '数据来源': '豆瓣TOP250',
            '采集时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        movies_data.append(movie_info)
    
    return pd.DataFrame(movies_data)

def enhance_data(df):
    """数据增强和清洗"""
    print("🔄 进行数据增强...")
    
    # 1. 数据清洗：处理可能的异常值
    df = df[df['评分'] >= 6.0]  # 移除评分异常低的电影
    
    # 2. 数据增强：创建新字段
    df['评价人数等级'] = pd.cut(df['评价人数'], 
                              bins=[0, 100000, 500000, 1000000, float('inf')],
                              labels=['小众', '热门', '很火', '现象级'])
    
    df['评分等级'] = pd.cut(df['评分'],
                          bins=[0, 8.5, 9.0, 9.5, 10],
                          labels=['良好', '优秀', '经典', '神作'])
    
    # 3. 计算衍生指标
    df['热度指数'] = (df['评分'] * 0.7 + (df['评价人数'] / 1000000) * 0.3).round(2)
    
    print("✅ 数据增强完成！")
    return df

def analyze_data(df):
    """数据分析"""
    print("\n📊 数据分析结果:")
    print("=" * 30)
    
    # 基本统计
    print(f"• 电影数量: {len(df)} 部")
    print(f"• 评分范围: {df['评分'].min()} - {df['评分'].max()}")
    print(f"• 平均评分: {df['评分'].mean():.2f}")
    print(f"• 总评价人数: {df['评价人数'].sum():,} 人")
    
    # 分布分析
    print(f"\n🎯 评分分布:")
    rating_stats = df['评分等级'].value_counts()
    for level, count in rating_stats.items():
        print(f"  {level}: {count} 部")
    
    print(f"\n🔥 热度分布:")
    popularity_stats = df['评价人数等级'].value_counts()
    for level, count in popularity_stats.items():
        print(f"  {level}: {count} 部")
    
    # 最佳推荐
    best_movie = df.loc[df['热度指数'].idxmax()]
    print(f"\n🏆 综合推荐: {best_movie['电影标题']}")
    print(f"   评分: {best_movie['评分']} | 热度指数: {best_movie['热度指数']}")

# 主程序
if __name__ == "__main__":
    # 1. 爬取数据
    print("🕸️ 开始爬取数据...")
    df = crawl_douban_top250()
    
    # 2. 数据增强
    df_enhanced = enhance_data(df)
    
    # 3. 数据分析
    analyze_data(df_enhanced)
    
    # 4. 保存增强后的数据
    df_enhanced.to_csv('douban_top250_enhanced.csv', index=False, encoding='utf-8-sig')
    print(f"\n💾 增强数据已保存: douban_top250_enhanced.csv")
    
    # 显示数据预览
    print("\n📋 增强数据预览:")
    print(df_enhanced[['排名', '电影标题', '评分', '评价人数等级', '评分等级', '热度指数']].head(8))