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
        'DIRS': [],
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
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),# 為postman新增
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 預設登入才能操作
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

# ✅ 預設語言與時區
LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
