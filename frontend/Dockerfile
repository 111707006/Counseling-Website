# 多階段構建 - 前端 Next.js
# 階段 1: 依賴安裝
FROM node:18-alpine AS deps

# 設置工作目錄
WORKDIR /app

# 複製 package 文件
COPY package*.json ./
COPY pnpm-lock.yaml* ./

# 安裝依賴
RUN \
  if [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm install --no-frozen-lockfile; \
  else \
    npm install --legacy-peer-deps && npm cache clean --force; \
  fi

# 階段 2: 構建應用
FROM node:18-alpine AS builder

# 設置工作目錄
WORKDIR /app

# 從 deps 階段複製 node_modules
COPY --from=deps /app/node_modules ./node_modules

# 複製應用程式代碼
COPY . .

# 設置環境變數
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# 構建應用
RUN \
  if [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm build; \
  else \
    npm run build; \
  fi

# 階段 3: 運行環境
FROM node:18-alpine AS runner

# 設置工作目錄
WORKDIR /app

# 設置環境變數
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# 創建非 root 用戶
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# 複製公共文件
COPY --from=builder /app/public ./public

# 複製構建產物
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
# 複製 package.json (standalone 模式需要)
COPY --from=builder /app/package.json ./package.json

# 切換到非 root 用戶
USER nextjs

# 暴露端口
EXPOSE 3000

# 設置環境變數
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# 健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD node --version || exit 1

# 啟動命令
CMD ["node", "server.js"]