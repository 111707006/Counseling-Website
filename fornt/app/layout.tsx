import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Toaster } from "@/components/ui/toaster"
import Link from "next/link"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "張老師台北心理諮商所",
  description: "專業心理諮商服務，陪伴您找到內心的平靜與力量",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen`} suppressHydrationWarning>
  {/* ✅ 疊底背景圖，撐滿全畫面，不受容器限制 */}
  <div className="fixed inset-0 -z-10 bg-texture bg-cover bg-center bg-no-repeat" />

        <nav className="bg-white/90 backdrop-blur-sm border-b border-gray-300 sticky top-0 z-50">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="text-xl font-bold text-black">
                張老師台北心理諮商所
              </Link>
              <div className="hidden md:flex space-x-6">
                <Link href="/" className="text-gray-700 hover:text-black">
                  首頁
                </Link>
                <Link href="/therapists" className="text-gray-700 hover:text-black">
                  心理師介紹
                </Link>
                <Link href="/articles" className="text-gray-700 hover:text-black">
                  心理健康文章
                </Link>
                <Link href="/announcements" className="text-gray-700 hover:text-black">
                  最新消息
                </Link>
                <Link href="/assessments" className="text-gray-700 hover:text-black">
                  心理測驗
                </Link>
                <Link href="/appointments/book" className="text-gray-700 hover:text-black">
                  預約諮詢
                </Link>
                <Link href="/appointments/query" className="text-gray-700 hover:text-black">
                  查詢預約
                </Link>
              </div>
            </div>
          </div>
        </nav>
        {children}
        <Toaster />
      </body>
    </html>
  )
}
