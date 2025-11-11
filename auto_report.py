# auto_report.py - 自动化分析报告
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def generate_analysis_report():
    """生成自动化分析报告"""
    print("📈 生成豆瓣TOP250分析报告")
    print("=" * 50)
    
    # 读取数据
    df = pd.read_csv('douban_top250_enhanced.csv')
    
    # 创建报告目录
    report_dir = 'douban_analysis_report'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    # 创建图表
    fig = plt.figure(figsize=(16, 12))
    
    # 1. 评分分布
    plt.subplot(2, 3, 1)
    df['评分'].hist(bins=15, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('评分分布', fontweight='bold', fontsize=12)
    plt.xlabel('评分')
    plt.ylabel('电影数量')
    plt.grid(True, alpha=0.3)
    
    # 2. 热度指数TOP10
    plt.subplot(2, 3, 2)
    top10_hot = df.nlargest(10, '热度指数')
    plt.barh(range(10), top10_hot['热度指数'], color='lightcoral')
    plt.yticks(range(10), [title[:10]+'...' if len(title)>10 else title for title in top10_hot['电影标题']])
    plt.title('热度指数TOP10', fontweight='bold', fontsize=12)
    plt.xlabel('热度指数')
    
    # 3. 评分等级分布
    plt.subplot(2, 3, 3)
    rating_level_count = df['评分等级'].value_counts()
    plt.pie(rating_level_count.values, labels=rating_level_count.index, autopct='%1.1f%%', startangle=90)
    plt.title('评分等级分布', fontweight='bold', fontsize=12)
    
    # 4. 评价人数分布
    plt.subplot(2, 3, 4)
    df['评价人数'].hist(bins=15, color='lightgreen', edgecolor='black', alpha=0.7)
    plt.title('评价人数分布', fontweight='bold', fontsize=12)
    plt.xlabel('评价人数')
    plt.ylabel('电影数量')
    plt.grid(True, alpha=0.3)
    
    # 5. 评分vs评价人数散点图
    plt.subplot(2, 3, 5)
    plt.scatter(df['评分'], df['评价人数']/10000, alpha=0.6, color='purple')
    plt.title('评分 vs 评价人数', fontweight='bold', fontsize=12)
    plt.xlabel('评分')
    plt.ylabel('评价人数 (万)')
    plt.grid(True, alpha=0.3)
    
    # 6. 各等级电影数量
    plt.subplot(2, 3, 6)
    level_count = df['评价人数等级'].value_counts()
    level_count.plot(kind='bar', color=['lightblue', 'lightgreen', 'orange', 'red'])
    plt.title('电影热度等级分布', fontweight='bold', fontsize=12)
    plt.xlabel('热度等级')
    plt.ylabel('电影数量')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'{report_dir}/analysis_charts.png', dpi=300, bbox_inches='tight')
    
    # 生成文本报告
    generate_text_report(df, report_dir)
    
    print(f"✅ 分析报告已生成到 {report_dir} 目录！")

def generate_text_report(df, report_dir):
    """生成文本分析报告"""
    report_content = f"""
豆瓣电影TOP250分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据分析员: {os.getenv('USERNAME', '你的名字')}

📊 数据概览
==============
• 分析电影数量: {len(df)} 部
• 数据时间范围: {df['上映年份'].min()} - {df['上映年份'].max()}
• 平均评分: {df['评分'].mean():.2f}
• 总评价人数: {df['评价人数'].sum():,} 人

🏆 最佳推荐
==============
综合最佳: {df.loc[df['热度指数'].idxmax(), '电影标题']}
   评分: {df.loc[df['热度指数'].idxmax(), '评分']} 
   热度指数: {df.loc[df['热度指数'].idxmax(), '热度指数']}

评分最高: {df.loc[df['评分'].idxmax(), '电影标题']}
   评分: {df.loc[df['评分'].idxmax(), '评分']}

最受欢迎: {df.loc[df['评价人数'].idxmax(), '电影标题']}
   评价人数: {df.loc[df['评价人数'].idxmax(), '评价人数']:,} 人

📈 分布分析
==============
评分分布:
{df['评分等级'].value_counts().to_string()}

热度分布:
{df['评价人数等级'].value_counts().to_string()}

🎯 数据洞察
==============
1. 大多数经典电影评分集中在 8.5-9.5 之间
2. 评分与评价人数呈现正相关关系
3. 现象级电影数量较少，但影响力巨大

📁 数据文件
==============
• 原始数据: douban_top250.csv
• 增强数据: douban_top250_enhanced.csv
• 分析图表: {report_dir}/analysis_charts.png
"""
    
    with open(f'{report_dir}/analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(report_content)

if __name__ == "__main__":
    generate_analysis_report()