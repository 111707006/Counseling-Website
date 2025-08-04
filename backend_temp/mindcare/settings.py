import os
from pathlib import Path
# 自動載入 .env
from dotenv import load_dotenv
load_dotenv()

# 專案根目錄路徑（BASE_DIR 是推薦的標準）
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 安全金鑰（開發時可用 .env 管理）
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-temp")

# 🚧 開發階段建議設定 True，正式部署記得關閉
DEBUG = True

# 允許的前端來源（React 前端用）
ALLOWED_HOSTS = ["*"]  # 或指定 frontend 網域

# ✅ App 註冊清單
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三方
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'rest_framework.authtoken',
    'ckeditor',
    'ckeditor_uploader',
    # 自訂 app
    'users',
    'therapists',
    'appointments',
    'assessments',
    'articles',
]

# ✅ 中介軟體（React 跨來源支援、Admin 正常啟動所需）
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨來源支援
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ 主 URL 配置
ROOT_URLCONF = 'mindcare.urls'

# Debug: 印出 MYSQL_PASSWORD 是否有正確讀取
print('DEBUG: MYSQL_PASSWORD from env =', os.getenv('MYSQL_PASSWORD'))

# ✅ TEMPLATES 設定（Django admin 需要）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ✅ REST Framework 設定（使用 SimpleJWT）
REST_FRAMEWORK = {
    # 認證類別設定
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT認證（管理員用）
        'rest_framework.authentication.TokenAuthentication',          # Token認證（PostMan測試用）
    ],
    # 權限類別設定：移除全域IsAuthenticated限制，讓ViewSet自行決定權限
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # 允許ViewSet自行決定權限
    ]
}

# ✅ 自訂使用者模型
AUTH_USER_MODEL = 'users.User'

# Debug: 印出 MYSQL_DB 是否有正確讀取
print('DEBUG: MYSQL_DB from env =', os.getenv('MYSQL_DB'))

# ✅ 資料庫設定（MySQL，讀取環境變數）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB', 'mindcare_v2'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
    }
}

# ✅ 跨來源設定（給 React 前端用）
CORS_ALLOW_ALL_ORIGINS = True  # 開發階段開放全部前端呼叫

# ✅ 靜態檔案設定（管理頁面 / CSS）
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# 媒體檔案設定
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# CKEditor 設定
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
    'article': {
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Source']
        ],
        'height': 400,
        'width': '100%',
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserUploadMethod': 'form',
        'removeDialogTabs': 'image:Link',
        'allowedContent': True,
        'removeButtons': '',
        'dialog_backgroundCoverOpacity': 0.5,
        'dialog_backgroundCoverColor': 'black',
        'removePlugins': 'elementspath',
        'resize_enabled': False,
        'image2_captionedClass': 'image-captioned',
        'image2_alignClasses': ['image-align-left', 'image-align-center', 'image-align-right'],
        'extraPlugins': 'image2',
        # 圖片預設設定
        'image_previewText': ' ',
        'filebrowserImageUploadUrl': '/ckeditor/upload/',
        'imageUploadUrl': '/ckeditor/upload/',
        # 自訂樣式
        'stylesSet': [
            # 圖片大小樣式
            {'name': '極小圖片 (200px)', 'element': 'img', 'attributes': {'class': 'img-xs', 'style': 'max-width: 200px; height: auto;'}},
            {'name': '小圖片 (300px)', 'element': 'img', 'attributes': {'class': 'img-sm', 'style': 'max-width: 300px; height: auto;'}},
            {'name': '中圖片 (500px)', 'element': 'img', 'attributes': {'class': 'img-md', 'style': 'max-width: 500px; height: auto;'}},
            {'name': '大圖片 (700px)', 'element': 'img', 'attributes': {'class': 'img-lg', 'style': 'max-width: 700px; height: auto;'}},
            {'name': '全寬圖片', 'element': 'img', 'attributes': {'class': 'img-full', 'style': 'width: 100%; height: auto;'}},
            
            # 圖片排版樣式
            {'name': '置中圖片', 'element': 'img', 'attributes': {'class': 'img-center', 'style': 'display: block; margin: 16px auto; max-width: 600px; height: auto;'}},
            {'name': '左對齊圖片', 'element': 'img', 'attributes': {'class': 'img-left', 'style': 'float: left; margin: 0 16px 16px 0; max-width: 400px; height: auto;'}},
            {'name': '右對齊圖片', 'element': 'img', 'attributes': {'class': 'img-right', 'style': 'float: right; margin: 0 0 16px 16px; max-width: 400px; height: auto;'}},
            
            # 圖片框架樣式
            {'name': '陰影圖片', 'element': 'img', 'attributes': {'class': 'img-shadow', 'style': 'max-width: 600px; height: auto; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border-radius: 8px; display: block; margin: 16px auto;'}},
            {'name': '圓角圖片', 'element': 'img', 'attributes': {'class': 'img-rounded', 'style': 'max-width: 600px; height: auto; border-radius: 12px; display: block; margin: 16px auto;'}},
            {'name': '圓形圖片', 'element': 'img', 'attributes': {'class': 'img-circle', 'style': 'width: 200px; height: 200px; border-radius: 50%; object-fit: cover; display: block; margin: 16px auto;'}},
            {'name': '邊框圖片', 'element': 'img', 'attributes': {'class': 'img-border', 'style': 'max-width: 600px; height: auto; border: 3px solid #e5e7eb; padding: 8px; display: block; margin: 16px auto;'}},
            
            # 特殊效果
            {'name': '懸浮效果圖片', 'element': 'img', 'attributes': {'class': 'img-hover', 'style': 'max-width: 600px; height: auto; transition: transform 0.3s ease; display: block; margin: 16px auto; cursor: pointer;'}},
            {'name': '灰階圖片', 'element': 'img', 'attributes': {'class': 'img-grayscale', 'style': 'max-width: 600px; height: auto; filter: grayscale(100%); display: block; margin: 16px auto;'}},
        ],
    },
}

# ✅ 預設語言與時區
LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ 郵件設定（開發階段使用控制台輸出）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 開發時用console
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 正式環境用SMTP

# SMTP 設定（正式環境時啟用）
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'noreply@mindcare.com'
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@mindcare.com')
