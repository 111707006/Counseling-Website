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
            'is_pinned': True,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 156
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
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 89
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
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 67
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
            'is_pinned': False,
            'show_on_homepage': False,
            'author': admin_user,
            'views_count': 124
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
            'is_pinned': False,
            'show_on_homepage': False,
            'author': admin_user,
            'views_count': 45
        },
        {
            'title': '2025年專業心理師證照考試資訊說明會',
            'summary': '針對想要報考專業心理師證照的民眾，我們將舉辦詳細的資訊說明會，包含考試內容、報名流程、準備方式等重要資訊。',
            'content': '''
            <h2>專業心理師證照考試資訊說明會</h2>
            
            <p>想要成為專業心理師嗎？讓我們為您詳細解說考試的各項資訊！</p>
            
            <h3>說明會內容：</h3>
            <ul>
                <li>心理師證照考試制度介紹</li>
                <li>考試科目與內容詳解</li>
                <li>報名條件與流程說明</li>
                <li>備考策略與讀書計畫</li>
                <li>實習機會與職涯發展</li>
                <li>Q&A 問答時間</li>
            </ul>
            
            <h3>活動資訊：</h3>
            <ul>
                <li><strong>時間：</strong>2025年2月8日（六）10:00-12:00</li>
                <li><strong>地點：</strong>張老師台北心理諮商所 會議室</li>
                <li><strong>對象：</strong>心理相關科系學生、有意從事心理師工作者</li>
                <li><strong>費用：</strong>免費參加</li>
                <li><strong>講師：</strong>資深心理師團隊</li>
            </ul>
            
            <h3>報名方式：</h3>
            <p>📞 電話報名：(02) 2532-6180</p>
            <p>📧 Email：info@mindcare.tw</p>
            <p>💻 線上報名：官網報名系統</p>
            
            <p>名額限定30人，請提前報名以免向隅！</p>
            ''',
            'category': created_categories[1],  # 活動消息
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 30
        },
        {
            'title': '新增兒童青少年心理治療服務',
            'summary': '因應社會需求，本所新增專業兒童青少年心理治療服務，由具豐富經驗的專業心理師提供個別化治療計畫。',
            'content': '''
            <h2>兒童青少年心理治療服務</h2>
            
            <p>張老師台北心理諮商所很高興宣布，我們新增了專業的兒童青少年心理治療服務！</p>
            
            <h3>服務對象：</h3>
            <ul>
                <li>6-12歲兒童</li>
                <li>13-18歲青少年</li>
                <li>家長親職諮詢</li>
            </ul>
            
            <h3>治療範圍：</h3>
            <p>• 學習困難與注意力問題</p>
            <p>• 情緒行為困擾</p>
            <p>• 人際關係問題</p>
            <p>• 親子溝通障礙</p>
            <p>• 適應性困難</p>
            <p>• 創傷後壓力症候群</p>
            
            <h3>治療方式：</h3>
            <ul>
                <li>遊戲治療</li>
                <li>藝術治療</li>
                <li>認知行為治療</li>
                <li>家族治療</li>
                <li>沙盤治療</li>
            </ul>
            
            <h3>專業團隊：</h3>
            <p>我們的兒童青少年心理師均具備：</p>
            <p>• 國家專技高考心理師證照</p>
            <p>• 兒童青少年專業訓練背景</p>
            <p>• 豐富的臨床實務經驗</p>
            
            <p><strong>預約專線：</strong>(02) 2532-6180 分機2</p>
            <p>我們將為每個孩子量身打造最適合的治療計畫。</p>
            ''',
            'category': created_categories[2],  # 服務公告
            'is_pinned': True,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 78
        },
        {
            'title': '免費心理健康篩檢週活動',
            'summary': '為推廣心理健康概念，本所將於3月第一週舉辦免費心理健康篩檢活動，歡迎民眾踴躍參加。',
            'content': '''
            <h2>免費心理健康篩檢週</h2>
            
            <p>心理健康與身體健康同等重要！為了讓更多民眾了解自己的心理健康狀態，我們特別舉辦免費篩檢週活動。</p>
            
            <h3>活動時間：</h3>
            <p>2025年3月3日（一）至 3月7日（五）</p>
            <p>每日 09:00-17:00</p>
            
            <h3>篩檢項目：</h3>
            <ul>
                <li>壓力指數評估</li>
                <li>情緒狀態檢測</li>
                <li>睡眠品質分析</li>
                <li>焦慮程度測量</li>
                <li>憂鬱傾向篩檢</li>
                <li>人際關係評量</li>
            </ul>
            
            <h3>活動特色：</h3>
            <p>• 完全免費參加</p>
            <p>• 專業心理師現場解說</p>
            <p>• 個人化建議報告</p>
            <p>• 免費諮詢15分鐘</p>
            <p>• 心理健康資源包</p>
            
            <h3>參加方式：</h3>
            <ol>
                <li>現場報名（無需預約）</li>
                <li>攜帶身分證明文件</li>
                <li>填寫基本資料</li>
                <li>完成篩檢量表</li>
                <li>領取結果報告</li>
            </ol>
            
            <h3>注意事項：</h3>
            <p>• 每日限額50名</p>
            <p>• 建議提早到場</p>
            <p>• 篩檢時間約30分鐘</p>
            
            <p>愛護自己，從關心心理健康開始！</p>
            ''',
            'category': created_categories[1],  # 活動消息
            'is_pinned': True,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 156
        },
        {
            'title': '夜間諮商服務時間延長通知',
            'summary': '為服務更多上班族朋友，本所夜間諮商服務時間將延長至22:00，提供更彈性的預約選擇。',
            'content': '''
            <h2>夜間諮商服務時間延長</h2>
            
            <p>考量到許多上班族朋友下班後才有時間接受心理諮商服務，張老師台北心理諮商所決定延長夜間服務時間。</p>
            
            <h3>新的服務時間：</h3>
            <ul>
                <li><strong>週一至週五：</strong>09:00-22:00</li>
                <li><strong>週六：</strong>09:00-21:00</li>
                <li><strong>週日：</strong>09:00-17:00</li>
            </ul>
            
            <h3>夜間時段的優勢：</h3>
            <p>• 適合上班族的時間安排</p>
            <p>• 避開尖峰交通時段</p>
            <p>• 諮商環境更加寧靜</p>
            <p>• 有更充裕的時間進行深度對談</p>
            
            <h3>夜間服務心理師：</h3>
            <p>我們安排了經驗豐富的心理師提供夜間服務，確保服務品質不打折扣。</p>
            
            <h3>預約方式：</h3>
            <p>📞 預約專線：(02) 2532-6180</p>
            <p>💻 線上預約：官網預約系統</p>
            <p>⏰ 預約時間：週一至週五 09:00-21:00</p>
            
            <h3>注意事項：</h3>
            <p>• 夜間時段預約需提前3天</p>
            <p>• 大樓管制時間請配合門禁規定</p>
            <p>• 建議攜帶身分證明以利通行</p>
            
            <p>新的服務時間自2025年2月1日起正式實施，歡迎多加利用！</p>
            ''',
            'category': created_categories[2],  # 服務公告
            'is_pinned': False,
            'show_on_homepage': True,
            'author': admin_user,
            'views_count': 91
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