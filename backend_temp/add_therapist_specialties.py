#!/usr/bin/env python
"""
快速腳本：為現有心理師加上專業領域
"""
import os
import sys
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from therapists.models import TherapistProfile, Specialty, SpecialtyCategory

def add_therapist_specialties():
    """為現有心理師加上專業領域"""
    
    # 獲取第一個心理師（張心理師）
    therapist = TherapistProfile.objects.first()
    if not therapist:
        print("沒有找到心理師資料")
        return
    
    print(f"為 {therapist.name} 加上專業領域...")
    
    # 選擇一些專業領域
    specialty_names = [
        '認知行為治療',   # 理論取向
        '焦慮症治療',     # 議題專精
        '憂鬱症治療',     # 議題專精
        '成人諮商',       # 服務族群
        '正念治療',       # 治療方式
    ]
    
    specialties = []
    for name in specialty_names:
        try:
            specialty = Specialty.objects.get(name=name)
            specialties.append(specialty)
            print(f"  - {specialty.category.name}: {specialty.name}")
        except Specialty.DoesNotExist:
            print(f"  警告：找不到專業領域 '{name}'")
    
    # 加上專業領域關聯
    therapist.specialties.set(specialties)
    
    # 更新舊格式的專業領域文字（向後相容）
    therapist.specialties_text = "認知行為治療、焦慮症治療、憂鬱症治療、成人諮商、正念治療"
    therapist.save()
    
    print(f"成功為 {therapist.name} 加上 {len(specialties)} 個專業領域")
    print(f"專業領域顯示：{therapist.get_specialties_display()}")
    print(f"依分類整理：{therapist.get_specialties_by_category()}")

def create_more_therapists():
    """建立更多心理師測試資料"""
    
    # 心理師資料
    therapists_data = [
        {
            'name': '李心理師',
            'title': '臨床心理師',
            'license_number': 'B987654321',
            'education': '國立陽明大學 臨床心理學系 博士',
            'experience': '擁有12年臨床經驗，專精家庭治療與伴侶諮商。',
            'beliefs': '相信每個家庭都有自己的解決方案，心理師只是陪伴者。',
            'consultation_modes': ['online', 'offline'],
            'pricing': {'online': 1500, 'offline': 1800},
            'specialties': ['家族系統治療', '伴侶諮商', '家庭諮商', '成人諮商'],
        },
        {
            'name': '王心理師',
            'title': '諮商心理師',
            'license_number': 'C456789123',
            'education': '國立師範大學 教育心理與輔導學系 碩士',
            'experience': '7年青少年輔導經驗，善於運用藝術治療技巧。',
            'beliefs': '每個孩子都是獨特的，需要被看見與理解。',
            'consultation_modes': ['offline'],
            'pricing': {'offline': 1400},
            'specialties': ['青少年諮商', '藝術治療', '遊戲治療', '焦慮症治療'],
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
            consultation_modes=data['consultation_modes'],
            pricing=data['pricing'],
            specialties_text=', '.join(data['specialties'])  # 舊格式
        )
        
        # 加上專業領域關聯
        specialties = []
        for name in data['specialties']:
            try:
                specialty = Specialty.objects.get(name=name)
                specialties.append(specialty)
            except Specialty.DoesNotExist:
                print(f"  警告：找不到專業領域 '{name}'")
        
        therapist.specialties.set(specialties)
        print(f"成功建立 {therapist.name}，包含 {len(specialties)} 個專業領域")

if __name__ == '__main__':
    print("開始建立心理師測試資料...")
    add_therapist_specialties()
    print()
    create_more_therapists()
    print("\n完成！")