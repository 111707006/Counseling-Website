-- 資料庫初始化腳本
-- 此腳本會在 MySQL 容器首次啟動時執行

-- 設置字符集
SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

-- 確保資料庫存在並使用正確的字符集
CREATE DATABASE IF NOT EXISTS `mindcare_v2` 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS `mindcare_v2_dev` 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 授予權限
GRANT ALL PRIVILEGES ON `mindcare_v2`.* TO 'mindcare_user'@'%';
GRANT ALL PRIVILEGES ON `mindcare_v2_dev`.* TO 'dev_user'@'%';

-- 刷新權限
FLUSH PRIVILEGES;

-- 設置時區
SET time_zone = '+08:00';