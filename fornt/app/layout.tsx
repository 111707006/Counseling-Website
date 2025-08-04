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

        <nav className="bg-white/90 backdrop-blur-sm border-b border-green-200 sticky top-0 z-50">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <Link href="/" className="text-xl font-bold text-green-800">
                張老師台北心理諮商所
              </Link>
              <div className="hidden md:flex space-x-6">
                <Link href="/" className="text-green-700 hover:text-green-900">
                  首頁
                </Link>
                <Link href="/therapists" className="text-green-700 hover:text-green-900">
                  心理師介紹
                </Link>
                <Link href="/articles" className="text-green-700 hover:text-green-900">
                  心理健康文章
                </Link>
                <Link href="/assessments" className="text-green-700 hover:text-green-900">
                  心理測驗
                </Link>
                <Link href="/appointments/book" className="text-green-700 hover:text-green-900">
                  預約諮詢
                </Link>
                <Link href="/appointments/query" className="text-green-700 hover:text-green-900">
                  查詢預約
                </Link>
              </div>
            </div>
          </div>
        </nav>
        {children}
        <footer className="bg-green-800 text-white py-12 mt-16">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-xl font-bold mb-4">張老師台北心理諮商所</h3>
                <p className="text-green-200">專業心理諮商服務，陪伴您找到內心的平靜與力量</p>
              </div>
              <div>
                <h4 className="font-semibold mb-4">服務項目</h4>
                <ul className="space-y-2 text-green-200">
                  <li>個人心理諮商</li>
                  <li>伴侶諮商</li>
                  <li>家庭治療</li>
                  <li>心理測驗評估</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-4">聯絡資訊</h4>
                <div className="space-y-2 text-green-200">
                  <p>電話：(02) 1234-5678</p>
                  <p>地址：台北市中正區○○路123號</p>
                  <p>Email：info@counseling.com.tw</p>
                </div>
              </div>
            </div>
            <div className="border-t border-green-700 mt-8 pt-8 text-center text-green-200">
              <p>&copy; 2024 張老師台北心理諮商所. All rights reserved.</p>
            </div>
          </div>
        </footer>
        <Toaster />
      </body>
    </html>
  )
}
