# 多階段構建 - 後端 Django
# 階段 1: 基礎映像和依賴安裝
FROM python:3.11-slim as base

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 更新系統包並安裝必要的系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 設置工作目錄
WORKDIR /app

# 複製依賴文件
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 階段 2: 生產環境映像
FROM python:3.11-slim as production

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=mindcare.settings

# 安裝運行時依賴
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 創建非 root 用戶
RUN groupadd -r django && useradd -r -g django django

# 設置工作目錄
WORKDIR /app

# 從基礎階段複製已安裝的 Python 包
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# 複製應用程式代碼
COPY . .

# 創建必要的目錄並設置權限
RUN mkdir -p /app/static /app/media && \
    chown -R django:django /app

# 切換到非 root 用戶
USER django

# 收集靜態文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python manage.py check --deploy || exit 1

# 啟動命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "mindcare.wsgi:application"]