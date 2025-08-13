#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from articles.models import Article
from users.models import User

def create_article_data():
    """創建文章測試資料"""
    
    print("開始創建文章資料...")
    
    # 獲取管理員用戶
    admin_user = User.objects.get(email='admin@mindcare.com')
    
    # 文章資料
    articles_data = [
        {
            'title': '認識焦慮症：症狀、成因與治療方法',
            'excerpt': '焦慮症是現代社會常見的心理健康問題。了解焦慮症的症狀和治療方法，有助於及早發現並尋求專業協助。',
            'content': '''
            <p>焦慮症是一種常見的心理健康問題，影響著全球數百萬人的生活品質。了解焦慮症的症狀、成因和治療方法，對於患者和家屬都是非常重要的。</p>
            
            <h2>什麼是焦慮症？</h2>
            <p>焦慮症是一類精神疾病的總稱，特徵是持續性的焦慮、擔憂和恐懼感，這些感受會干擾日常生活和工作。</p>
            
            <h2>常見症狀</h2>
            <ul>
                <li>持續的擔憂和緊張</li>
                <li>心跳加速</li>
                <li>呼吸急促</li>
                <li>肌肉緊張</li>
                <li>睡眠困難</li>
                <li>注意力不集中</li>
            </ul>
            
            <h2>治療方法</h2>
            <p>焦慮症的治療通常包括心理治療和藥物治療：</p>
            <ul>
                <li>認知行為治療 (CBT)</li>
                <li>放鬆訓練</li>
                <li>正念冥想</li>
                <li>必要時的藥物輔助</li>
            </ul>
            
            <p>如果您或您的親友正在經歷焦慮症狀，建議尋求專業心理師的協助。</p>
            ''',
            'tags': '焦慮症, 心理健康, 認知行為治療',
        },
        {
            'title': '如何建立健康的人際關係',
            'excerpt': '良好的人際關係是心理健康的重要基石。學習溝通技巧和建立信任，能幫助我們維持更好的關係品質。',
            'content': '''
            <p>人際關係對我們的心理健康和生活滿意度有著深遠的影響。建立和維持健康的人際關係是一門需要學習的藝術。</p>
            
            <h2>健康人際關係的特徵</h2>
            <ul>
                <li>相互尊重和理解</li>
                <li>開放和誠實的溝通</li>
                <li>互相支持</li>
                <li>保持個人界限</li>
                <li>共同成長</li>
            </ul>
            
            <h2>改善溝通技巧</h2>
            <p>良好的溝通是關係成功的關鍵：</p>
            <ul>
                <li>主動聆聽</li>
                <li>表達真實感受</li>
                <li>避免批判性語言</li>
                <li>學會同理心</li>
                <li>處理衝突的技巧</li>
            </ul>
            
            <h2>建立信任</h2>
            <p>信任是所有深層關係的基礎，需要時間和一致的行動來建立。</p>
            
            <p>如果您在人際關係上遇到困難，專業的諮商可以幫助您發展更好的關係技巧。</p>
            ''',
            'tags': '人際關係, 溝通技巧, 諮商',
        },
        {
            'title': '壓力管理與自我照顧的重要性',
            'excerpt': '現代生活充滿各種壓力，學會有效的壓力管理技巧和自我照顧方法，對維持身心健康至關重要。',
            'content': '''
            <p>在快節奏的現代生活中，壓力已成為我們日常生活的一部分。學會有效管理壓力和照顧自己，是維持心理健康的重要技能。</p>
            
            <h2>認識壓力</h2>
            <p>壓力是身體對挑戰或威脅的自然反應。適量的壓力可以激勵我們，但過度的壓力則可能對身心健康造成負面影響。</p>
            
            <h2>壓力的警示信號</h2>
            <ul>
                <li>身體症狀：頭痛、肌肉緊張、疲勞</li>
                <li>情緒症狀：易怒、焦慮、憂鬱</li>
                <li>行為症狀：食慾改變、睡眠問題、社交退縮</li>
                <li>認知症狀：注意力不集中、記憶力下降</li>
            </ul>
            
            <h2>有效的壓力管理策略</h2>
            <ul>
                <li>深呼吸和放鬆技巧</li>
                <li>規律運動</li>
                <li>充足睡眠</li>
                <li>健康飲食</li>
                <li>時間管理</li>
                <li>尋求社會支持</li>
                <li>學會說「不」</li>
            </ul>
            
            <h2>自我照顧的重要性</h2>
            <p>自我照顧不是自私，而是維持身心健康的必需品。定期投入時間照顧自己的身心需求，能讓我們更好地面對生活挑戰。</p>
            
            <p>如果壓力持續影響您的日常生活，建議尋求專業心理師的協助。</p>
            ''',
            'tags': '壓力管理, 自我照顧, 心理健康',
        }
    ]
    
    base_time = timezone.now()
    
    for i, article_data in enumerate(articles_data):
        # 設置不同的發布時間
        publish_time = base_time - timedelta(days=i*3, hours=i*2)
        
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'title': article_data['title'],
                'excerpt': article_data['excerpt'],
                'content': article_data['content'],
                'tags': article_data['tags'],
                'author': admin_user,
                'is_published': True,
                'published_at': publish_time,
            }
        )
        
        if created:
            print(f"創建文章：{article.title}")
        else:
            print(f"文章已存在：{article.title}")

    print(f"\n文章資料創建完成！")
    print(f"現有文章數量：{Article.objects.count()} 篇")

if __name__ == '__main__':
    create_article_data()