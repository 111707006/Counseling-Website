#!/usr/bin/env python
import os
import sys
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from therapists.models import TherapistProfile
from users.models import User

def create_therapist_data():
    """創建治療師測試資料"""
    
    print("開始創建治療師資料...")
    
    # 心理師資料
    therapists_data = [
        {
            'name': '張心理師',
            'title': '臨床心理師',
            'license_number': 'A123456789',
            'education': '國立臺灣大學 心理學系 碩士',
            'experience': '擁有10年以上臨床經驗，專精認知行為治療與焦慮症治療。',
            'beliefs': '相信每個人都有自我療癒的能力，心理師只是陪伴者和引導者。',
            'specialties_text': '認知行為治療、焦慮症治療、憂鬱症治療、成人諮商、正念治療',
        },
        {
            'name': '李心理師',
            'title': '諮商心理師',
            'license_number': 'B987654321',
            'education': '國立陽明交通大學 臨床心理學系 博士',
            'experience': '擁有12年臨床經驗，專精家庭治療與伴侶諮商。',
            'beliefs': '相信每個家庭都有自己的解決方案，心理師只是陪伴者。',
            'specialties_text': '家族系統治療、伴侶諮商、家庭諮商、成人諮商',
        },
        {
            'name': '王心理師',
            'title': '諮商心理師',
            'license_number': 'C456789123',
            'education': '國立師範大學 教育心理與輔導學系 碩士',
            'experience': '7年青少年輔導經驗，善於運用藝術治療技巧。',
            'beliefs': '每個孩子都是獨特的，需要被看見與理解。',
            'specialties_text': '青少年諮商、藝術治療、遊戲治療、焦慮症治療',
        }
    ]
    
    for data in therapists_data:
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
            specialties_text=data['specialties_text']
        )
        
        print(f"成功建立 {therapist.name}")

    print(f"\n治療師資料創建完成！")
    print(f"現有治療師數量：{TherapistProfile.objects.count()} 位")

if __name__ == '__main__':
    create_therapist_data()