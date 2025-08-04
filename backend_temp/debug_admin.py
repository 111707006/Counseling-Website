#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare.settings')
django.setup()

from django.contrib import admin

print("=== Django Admin 註冊檢查 ===")
print("所有已註冊的模型:")

for model, admin_class in admin.site._registry.items():
    app_label = model._meta.app_label
    model_name = model.__name__
    admin_class_name = admin_class.__class__.__name__
    
    print(f"{app_label}.{model_name} -> {admin_class_name}")
    
    if app_label == 'appointments':
        print(f"  *** APPOINTMENTS 模型: {model_name} ***")

print("\n=== 結論 ===")
appointments_found = any(model._meta.app_label == 'appointments' for model in admin.site._registry.keys())
print(f"APPOINTMENTS 區塊存在: {appointments_found}")

if not appointments_found:
    print("❌ 需要檢查 appointments/admin.py 是否被正確載入")
else:
    print("✅ APPOINTMENTS 已註冊，但可能需要重啟服務器才能在 Web 界面顯示")