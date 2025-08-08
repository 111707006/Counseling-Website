#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# 設置 Django 環境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from announcements.models import AnnouncementCategory, Announcement
from users.models import User

def add_new_announcement():
    print("新增假資料公告...")
    
    # 獲取管理員用戶
    admin_user = User.objects.get(email='admin@mindcare.com')
    
    # 獲取活動消息分類
    activity_category = AnnouncementCategory.objects.get(name='活動消息')
    
    # 創建新公告
    new_announcement_data = {
        'title': '2025年專業心理師證照考試資訊說明會',
        'summary': '針對想要報考專業心理師證照的民眾，我們將舉辦詳細的資訊說明會，包含考試內容、報名流程、準備方式等重要資訊。',
        'content': '''
        <h2>2025年專業心理師證照考試資訊說明會</h2>
        
        <p>親愛的朋友們：</p>
        
        <p>為了協助有志從事心理諮商工作的朋友們，張老師台北心理諮商所將舉辦專業心理師證照考試資訊說明會。</p>
        
        <h3>說明會內容：</h3>
        <ul>
            <li>心理師證照考試制度介紹</li>
            <li>考試科目與內容分析</li>
            <li>報名資格與流程說明</li>
            <li>準備策略與讀書方法</li>
            <li>實習機會與就業前景</li>
        </ul>
        
        <h3>活動資訊：</h3>
        <ul>
            <li><strong>時間：</strong>2025年3月8日（六）09:30-12:00</li>
            <li><strong>地點：</strong>張老師台北心理諮商所 大會議室</li>
            <li><strong>講師：</strong>資深心理師 王心理師、李心理師</li>
            <li><strong>費用：</strong>免費參加（需事先報名）</li>
            <li><strong>名額：</strong>限30名</li>
        </ul>
        
        <h3>適合參加對象：</h3>
        <p>• 心理學系學生</p>
        <p>• 相關科系畢業生</p>
        <p>• 有志轉職心理諮商領域者</p>
        <p>• 對心理師職涯感興趣的民眾</p>
        
        <h3>報名方式：</h3>
        <p>📞 電話報名：(02) 2532-6180</p>
        <p>💻 線上報名：透過本網站報名系統</p>
        <p>📧 Email報名：info@mindcare.com.tw</p>
        
        <p><strong>報名截止：</strong>2025年3月5日（三）或額滿為止</p>
        
        <p>歡迎對心理諮商專業有興趣的朋友踴躍參加！</p>
        ''',
        'category': activity_category,
        'priority': 'medium',
        'is_pinned': False,
        'show_on_homepage': True,
        'author': admin_user,
        'status': 'published',
        'views_count': 28,
        'likes_count': 5
    }
    
    # 設置發布時間（1天前）
    publish_time = timezone.now() - timedelta(days=1, hours=2)
    
    announcement, created = Announcement.objects.get_or_create(
        title=new_announcement_data['title'],
        defaults={
            **new_announcement_data,
            'publish_date': publish_time,
            'created_at': publish_time,
            'updated_at': publish_time,
        }
    )
    
    if created:
        print(f"成功創建新公告：{announcement.title}")
    else:
        print(f"公告已存在：{announcement.title}")
    
    print(f"\n目前公告總數：{Announcement.objects.filter(status='published').count()}筆")
    
    # 顯示最新的3筆公告
    latest_announcements = Announcement.objects.filter(
        status='published'
    ).order_by('-publish_date')[:3]
    
    print("\n最新3筆公告：")
    for i, ann in enumerate(latest_announcements, 1):
        print(f"{i}. {ann.title}")
        print(f"   發布時間：{ann.publish_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"   分類：{ann.category.name}")
        print()

if __name__ == '__main__':
    add_new_announcement()