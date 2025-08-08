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
            'summary': '2025年度的心理諮商預約正式開放，歡迎有需要的民眾來電預約。我們提供專業的心理諮商服務，協助您面對生活中的各種挑戰。',
            'content': '''
            <h2>新年度心理諮商預約正式開放</h2>
            
            <p>親愛的朋友們：</p>
            
            <p>張老師台北心理諮商所很高興宣布，2025年度的心理諮商預約服務正式開放受理！</p>
            
            <h3>服務內容包括：</h3>
            <ul>
                <li>個別心理諮商</li>
                <li>伴侶諮商</li>
                <li>家庭治療</li>
                <li>青少年諮商</li>
                <li>創傷治療</li>
            </ul>
            
            <h3>預約方式：</h3>
            <p>📞 電話預約：(02) 2532-6180</p>
            <p>💻 線上預約：透過本網站預約系統</p>
            <p>🕐 服務時間：週一至週六 09:00-21:30，週日 09:00-17:00</p>
            
            <p>我們的專業心理師團隊將提供您最適切的協助，陪伴您走過生命中的每個階段。</p>
            ''',
            'category': created_categories[0],  # 重要通知
            'priority': 'high',
            'is_pinned': True,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 156,
            'likes_count': 23
        },
        {
            'title': '心理健康講座「情緒管理與自我照顧」即日起報名',
            'summary': '本講座將深入探討情緒管理的技巧與自我照顧的重要性，由資深心理師主講，歡迎民眾踴躍報名參加。',
            'content': '''
            <h2>心理健康講座：情緒管理與自我照顧</h2>
            
            <p>在快節奏的現代生活中，學會管理情緒和照顧自己是非常重要的生活技能。</p>
            
            <h3>講座資訊：</h3>
            <ul>
                <li><strong>主題：</strong>情緒管理與自我照顧</li>
                <li><strong>講師：</strong>資深心理師 李心理師</li>
                <li><strong>時間：</strong>2025年2月15日（六）14:00-16:00</li>
                <li><strong>地點：</strong>張老師台北心理諮商所</li>
                <li><strong>費用：</strong>免費參加</li>
            </ul>
            
            <h3>講座內容：</h3>
            <p>• 認識情緒的本質與功能</p>
            <p>• 學習情緒調節的實用技巧</p>
            <p>• 建立健康的自我照顧習慣</p>
            <p>• 壓力管理與放鬆技巧</p>
            
            <p><strong>報名方式：</strong>請來電 (02) 2532-6180 或透過網站報名</p>
            <p>名額有限，敬請把握機會！</p>
            ''',
            'category': created_categories[1],  # 活動消息
            'priority': 'medium',
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 89,
            'likes_count': 15
        },
        {
            'title': '線上諮商服務持續提供，方便您的時間安排',
            'summary': '考量到現代人的忙碌生活，我們持續提供線上心理諮商服務，讓您可以在舒適的環境中接受專業協助。',
            'content': '''
            <h2>線上心理諮商服務</h2>
            
            <p>為了讓更多需要幫助的朋友能夠便利地接受心理諮商服務，張老師台北心理諮商所持續提供線上諮商服務。</p>
            
            <h3>線上諮商的優點：</h3>
            <ul>
                <li>節省通勤時間</li>
                <li>在熟悉環境中進行諮商</li>
                <li>適合行動不便者</li>
                <li>保有完全的隱私性</li>
                <li>彈性的時間安排</li>
            </ul>
            
            <h3>技術要求：</h3>
            <p>• 穩定的網路連線</p>
            <p>• 電腦、平板或智慧型手機</p>
            <p>• 安靜且私密的空間</p>
            <p>• 視訊軟體（我們將協助安裝）</p>
            
            <h3>如何開始：</h3>
            <ol>
                <li>來電預約諮商時間</li>
                <li>告知需要線上諮商服務</li>
                <li>我們將協助您設定技術環境</li>
                <li>在預約時間開始諮商</li>
            </ol>
            
            <p>線上諮商與面對面諮商具有相同的專業品質，歡迎您多加利用！</p>
            ''',
            'category': created_categories[2],  # 服務公告
            'priority': 'low',
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 67,
            'likes_count': 8
        },
        {
            'title': '春節期間服務時間調整通知',
            'summary': '2025年農曆春節期間，本所服務時間將有所調整，請民眾留意相關異動訊息。',
            'content': '''
            <h2>春節期間服務時間調整</h2>
            
            <p>親愛的服務使用者，</p>
            
            <p>配合2025年農曆春節假期，張老師台北心理諮商所服務時間調整如下：</p>
            
            <h3>休假期間：</h3>
            <ul>
                <li>1月28日（二）除夕：休診</li>
                <li>1月29日（三）初一：休診</li>
                <li>1月30日（四）初二：休診</li>
                <li>1月31日（五）初三：休診</li>
            </ul>
            
            <h3>正常服務：</h3>
            <p>2月1日（六）初四起恢復正常服務時間</p>
            
            <h3>緊急聯絡：</h3>
            <p>春節期間如有緊急心理危機需求，請聯絡：</p>
            <p>• 生命線：1995</p>
            <p>• 張老師專線：1980</p>
            <p>• 緊急專線：(02) 2532-6180 轉分機999</p>
            
            <p>祝您新春愉快，身心健康！</p>
            ''',
            'category': created_categories[0],  # 重要通知
            'priority': 'medium',
            'is_pinned': False,
            'show_on_homepage': False,
            'author': admin_user,
            'views_count': 124,
            'likes_count': 12
        },
        {
            'title': '團體治療課程「人際關係成長團體」開始招生',
            'summary': '透過團體互動的方式，學習建立健康的人際關係，提升溝通技巧與情感表達能力。',
            'content': '''
            <h2>人際關係成長團體</h2>
            
            <p>人際關係是影響心理健康的重要因素。透過團體治療的方式，我們可以在安全的環境中練習與他人互動，學習更好的溝通方式。</p>
            
            <h3>課程特色：</h3>
            <ul>
                <li>小班制教學（6-8人）</li>
                <li>專業心理師帶領</li>
                <li>結構化的學習內容</li>
                <li>實際演練與回饋</li>
            </ul>
            
            <h3>適合對象：</h3>
            <p>• 想要改善人際關係的朋友</p>
            <p>• 在職場溝通上遇到困難者</p>
            <p>• 希望提升自信心的民眾</p>
            <p>• 想要學習表達情感的人</p>
            
            <h3>課程資訊：</h3>
            <ul>
                <li><strong>時間：</strong>每週四 19:00-21:00</li>
                <li><strong>期間：</strong>連續8週</li>
                <li><strong>開課日：</strong>2025年2月20日</li>
                <li><strong>費用：</strong>每人4800元</li>
            </ul>
            
            <p>報名請洽：(02) 2532-6180</p>
            ''',
            'category': created_categories[1],  # 活動消息
            'priority': 'medium',
            'is_pinned': False,
            'show_on_homepage': False,
            'author': admin_user,
            'views_count': 45,
            'likes_count': 7
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
                **ann_data,
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