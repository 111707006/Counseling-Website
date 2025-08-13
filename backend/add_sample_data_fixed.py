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

def create_sample_data():
    print("開始創建假資料...")
    
    # 創建管理員用戶（如果不存在）
    admin_user, created = User.objects.get_or_create(
        email='admin@mindcare.com',
        defaults={
            'username': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("管理員用戶已創建")
    else:
        print("管理員用戶已存在")

    # 創建公告分類
    categories_data = [
        {
            'name': '重要通知',
            'description': '重要的機構通知事項',
            'color': '#000000',
            'order': 1
        },
        {
            'name': '活動消息',
            'description': '各種活動和講座消息',
            'color': '#666666',
            'order': 2
        },
        {
            'name': '服務公告',
            'description': '服務相關的公告',
            'color': '#333333',
            'order': 3
        }
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category, created = AnnouncementCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        created_categories.append(category)
        if created:
            print(f"創建分類：{category.name}")
        else:
            print(f"分類已存在：{category.name}")

    # 創建公告
    announcements_data = [
        {
            'title': '新年度心理諮商預約開始受理',
            'summary': '2025年度的心理諮商預約正式開放，歡迎有需要的民眾來電預約。',
            'content': '''<h2>新年度心理諮商預約正式開放</h2>
            <p>親愛的朋友們：</p>
            <p>張老師台北心理諮商所很高興宣布，2025年度的心理諮商預約服務正式開放受理！</p>
            <h3>服務內容包括：</h3>
            <ul>
                <li>個別心理諮商</li>
                <li>伴侶諮商</li>
                <li>家庭治療</li>
                <li>青少年諮商</li>
                <li>創傷治療</li>
            </ul>''',
            'category': created_categories[0],
            'is_pinned': True,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 156
        },
        {
            'title': '心理健康講座「情緒管理與自我照顧」即日起報名',
            'summary': '本講座將深入探討情緒管理的技巧與自我照顧的重要性，由資深心理師主講。',
            'content': '''<h2>心理健康講座：情緒管理與自我照顧</h2>
            <p>在快節奏的現代生活中，學會管理情緒和照顧自己是非常重要的生活技能。</p>
            <h3>講座資訊：</h3>
            <ul>
                <li><strong>主題：</strong>情緒管理與自我照顧</li>
                <li><strong>講師：</strong>資深心理師 李心理師</li>
                <li><strong>時間：</strong>2025年2月15日（六）14:00-16:00</li>
                <li><strong>地點：</strong>張老師台北心理諮商所</li>
                <li><strong>費用：</strong>免費參加</li>
            </ul>''',
            'category': created_categories[1],
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 89
        },
        {
            'title': '線上諮商服務持續提供，方便您的時間安排',
            'summary': '考量到現代人的忙碌生活，我們持續提供線上心理諮商服務。',
            'content': '''<h2>線上心理諮商服務</h2>
            <p>為了讓更多需要幫助的朋友能夠便利地接受心理諮商服務，張老師台北心理諮商所持續提供線上諮商服務。</p>
            <h3>線上諮商的優點：</h3>
            <ul>
                <li>節省通勤時間</li>
                <li>在熟悉環境中進行諮商</li>
                <li>適合行動不便者</li>
                <li>保有完全的隱私性</li>
                <li>彈性的時間安排</li>
            </ul>''',
            'category': created_categories[2],
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 67
        }
    ]

    # 設置發布時間
    base_time = timezone.now()
    
    for i, ann_data in enumerate(announcements_data):
        # 設置不同的發布時間
        publish_time = base_time - timedelta(days=i*2, hours=i*3)
        
        announcement, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults={
                'title': ann_data['title'],
                'summary': ann_data['summary'],
                'content': ann_data['content'],
                'category': ann_data['category'],
                'is_pinned': ann_data['is_pinned'],
                'show_on_homepage': ann_data['show_on_homepage'],
                'author': ann_data['author'],
                'views_count': ann_data['views_count'],
                'status': 'published',
                'publish_date': publish_time,
                'created_at': publish_time,
                'updated_at': publish_time,
            }
        )
        
        if created:
            print(f"創建公告：{announcement.title}")
        else:
            print(f"公告已存在：{announcement.title}")

    print("\n假資料創建完成！")
    print(f"創建了 {len(categories_data)} 個分類")
    print(f"創建了 {len(announcements_data)} 個公告")

if __name__ == '__main__':
    create_sample_data()