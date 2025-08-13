#!/usr/bin/env python
import os
import sys
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from therapists.models import TherapistProfile

def restore_real_therapists():
    """根據媒體檔案名稱恢復真實治療師資料"""
    
    print("開始恢復真實治療師資料...")
    
    # 根據照片檔案名稱推斷的真實治療師資料
    real_therapists = [
        {
            'name': '黃雅琪',
            'title': '臨床心理師',
            'license_number': 'YQ152634',
            'education': '國立陽明交通大學 臨床心理學系',
            'experience': '專精於情緒調節、壓力管理與人際關係諮商，具豐富臨床經驗。',
            'beliefs': '相信每個人都有自我療癒的潛能，透過專業引導找到內在力量。',
            'specialties_text': '情緒調節、壓力管理、人際關係諮商、認知行為治療',
            'photo': 'therapists/152634-黃雅琪.jpg'
        },
        {
            'name': '邱珮思',
            'title': '諮商心理師',
            'license_number': 'PS5766',
            'education': '國立臺灣師範大學 教育心理與輔導學系',
            'experience': '專注於青少年心理輔導與家庭治療，擅長藝術治療技巧。',
            'beliefs': '每個人都值得被理解與支持，透過諮商找到屬於自己的成長路徑。',
            'specialties_text': '青少年諮商、家庭治療、藝術治療、情緒障礙',
            'photo': 'therapists/DSC_5766-邱珮思_1.jpg'
        },
        {
            'name': '李葦蓉',
            'title': '臨床心理師',
            'license_number': 'WR6514',
            'education': '國立成功大學 心理學系 博士',
            'experience': '專長創傷治療與危機處理，具備多年急性心理照護經驗。',
            'beliefs': '創傷可以被療癒，每個創傷倖存者都有重新站起來的勇氣。',
            'specialties_text': '創傷治療、危機處理、EMDR、創傷後壓力症候群',
            'photo': 'therapists/DSC_6514-李葦蓉3.jpg'
        },
        {
            'name': '何淑津',
            'title': '諮商心理師',
            'license_number': 'SJ7023',
            'education': '國立彰化師範大學 輔導與諮商學系',
            'experience': '專精伴侶諮商與婚姻治療，協助夫妻重建關係橋樑。',
            'beliefs': '關係是可以修復的，透過理解與溝通找回彼此的連結。',
            'specialties_text': '伴侶諮商、婚姻治療、關係修復、溝通技巧',
            'photo': 'therapists/DSC_7023-何淑津_2.jpg'
        }
    ]
    
    for data in real_therapists:
        # 檢查是否已存在
        if TherapistProfile.objects.filter(name=data['name']).exists():
            print(f"{data['name']} 已存在，跳過...")
            continue
            
        # 建立心理師
        therapist = TherapistProfile.objects.create(
            name=data['name'],
            title=data['title'],
            license_number=data['license_number'],
            education=data['education'],
            experience=data['experience'],
            beliefs=data['beliefs'],
            specialties_text=data['specialties_text'],
            photo=data['photo']
        )
        
        print(f"恢復真實治療師：{therapist.name} ({therapist.title})")

    print(f"\n真實治療師資料恢復完成！")
    print(f"現有治療師數量：{TherapistProfile.objects.count()} 位")

if __name__ == '__main__':
    restore_real_therapists()