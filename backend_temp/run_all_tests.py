#!/usr/bin/env python
"""
主測試腳本 - 執行所有系統檢查
包含綜合測試、API相容性測試和資料庫完整性檢查
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def run_script(script_name, description):
    """執行測試腳本"""
    print(f"\n{'='*80}")
    print(f"🚀 執行 {description}")
    print(f"腳本: {script_name}")
    print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*80)
    
    try:
        # 執行Python腳本
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, 
                              encoding='utf-8', timeout=300)
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ 腳本執行失敗:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 腳本執行超時 (5分鐘)")
        return False
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")
        return False

def check_django_server():
    """檢查Django服務器是否運行"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/api/therapists/profiles/", timeout=5)
        return True
    except:
        return False

def main():
    """主函數"""
    print("🎯 心理諮商系統完整測試套件")
    print("="*80)
    print("本測試將執行以下檢查:")
    print("1. 🔍 綜合系統測試 (API、資料庫、郵件等)")
    print("2. 🌐 API相容性測試 (前後端介面檢查)")
    print("3. 📊 資料庫完整性檢查 (結構和約束)")
    print()
    
    # 檢查Django服務器
    if not check_django_server():
        print("⚠️  Django服務器未運行，請先啟動:")
        print("   python manage.py runserver")
        print()
        
        response = input("是否繼續執行資料庫檢查? (y/n): ")
        if response.lower() != 'y':
            print("❌ 測試取消")
            return
    else:
        print("✅ Django服務器正在運行")
    
    # 記錄開始時間
    start_time = time.time()
    
    # 執行測試腳本
    tests = [
        ("comprehensive_system_test.py", "綜合系統測試"),
        ("api_compatibility_test.py", "API相容性測試"), 
        ("database_integrity_check.py", "資料庫完整性檢查")
    ]
    
    results = {}
    
    for script, description in tests:
        if os.path.exists(script):
            success = run_script(script, description)
            results[description] = success
        else:
            print(f"❌ 找不到測試腳本: {script}")
            results[description] = False
            
        # 測試間隔
        time.sleep(2)
    
    # 生成總結報告
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*80}")
    print("📊 測試總結報告")
    print('='*80)
    print(f"總執行時間: {duration:.1f}秒")
    print(f"完成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"測試結果: {passed}/{total} 通過")
    print()
    
    for test, success in results.items():
        status = "✅ 通過" if success else "❌ 失敗"
        print(f"{status} {test}")
    
    # 生成建議
    print(f"\n🔧 修復建議:")
    
    if not results.get("資料庫完整性檢查", False):
        print("• 執行 database_fix_script.sh 修復資料庫問題")
        
    if not results.get("API相容性測試", False):
        print("• 檢查serializers.py和前端介面定義")
        print("• 確保Django服務器正在運行")
        
    if not results.get("綜合系統測試", False):
        print("• 檢查.env設定檔")
        print("• 執行資料庫遷移: python manage.py migrate")
        print("• 初始化測試資料")
    
    print("\n📋 詳細報告已輸出在上方，請向上捲動查看")
    
    # 如果有失敗的測試，以非零狀態碼退出
    if passed < total:
        sys.exit(1)
    else:
        print("\n🎉 所有測試通過！系統狀態良好")

if __name__ == "__main__":
    main()