'use client'

import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Calendar, Eye, Heart, Pin, Search, Filter } from 'lucide-react'

interface AnnouncementCategory {
  id: number
  name: string
  color: string
  announcements_count: number
}

interface Announcement {
  id: number
  title: string
  summary: string
  category?: AnnouncementCategory
  featured_image_url?: string
  priority: 'low' | 'medium' | 'high'
  priority_display: string
  is_pinned: boolean
  publish_date: string
  views_count: number
  likes_count: number
  author: {
    id: number
    username: string
  }
}

export default function AnnouncementsPage() {
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [categories, setCategories] = useState<AnnouncementCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchData()
  }, [searchQuery])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // 構建查詢參數
      const params = new URLSearchParams()
      if (searchQuery) params.append('search', searchQuery)

      // 獲取公告列表
      const announcementsRes = await fetch(`http://localhost:8000/api/announcements/?${params.toString()}`)
      if (announcementsRes.ok) {
        const announcementsData = await announcementsRes.json()
        setAnnouncements(announcementsData.results || announcementsData)
      }
    } catch (error) {
      console.error('Error fetching announcements:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'numeric',
      day: 'numeric'
    })
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-500'
      case 'medium': return 'bg-yellow-500'
      default: return 'bg-gray-500'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto"></div>
            <p className="mt-4 text-gray-700">載入中...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto p-4">
        {/* 頁面標題 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-black mb-4">最新消息</h1>
          <p className="text-lg text-gray-700">掌握心理健康相關的重要資訊與動態</p>
        </div>

        {/* 搜尋區域 */}
        <Card className="mb-8 border-gray-300">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              {/* 搜尋框 */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                <Input
                  placeholder="搜尋公告標題或內容..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 border-gray-300 focus:border-black focus:ring-black"
                />
              </div>

              {/* 清除按鈕 */}
              {searchQuery && (
                <Button 
                  variant="outline" 
                  className="border-gray-300 text-black hover:bg-gray-100"
                  onClick={() => {
                    setSearchQuery('')
                  }}
                >
                  清除搜尋
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* 公告列表 */}
        {announcements.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <p className="text-gray-500 text-lg">目前沒有符合條件的公告</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6">
            {announcements.map((announcement) => (
              <Card key={announcement.id} className="border-gray-300 hover:shadow-lg transition-shadow duration-200">
                <CardContent className="p-6">
                  <div className="flex flex-col lg:flex-row gap-4">
                    {/* 特色圖片 */}
                    {announcement.featured_image_url && (
                      <div className="lg:w-48 h-32 relative rounded-lg overflow-hidden bg-gray-200">
                        <Image
                          src={announcement.featured_image_url}
                          alt={announcement.title}
                          fill
                          className="object-cover grayscale"
                        />
                      </div>
                    )}

                    {/* 內容區域 */}
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2 flex-wrap">
                          {announcement.is_pinned && (
                            <Badge variant="secondary" className="bg-gray-200 text-black border-gray-400">
                              <Pin className="h-3 w-3 mr-1" />
                              置頂
                            </Badge>
                          )}
                          
                          {announcement.category && (
                            <Badge 
                              className="text-white bg-black"
                            >
                              {announcement.category.name}
                            </Badge>
                          )}
                        </div>
                      </div>

                      <Link href={`/announcements/${announcement.id}`}>
                        <h3 className="text-xl font-semibold text-black hover:text-gray-600 transition-colors mb-2">
                          {announcement.title}
                        </h3>
                      </Link>

                      {announcement.summary && (
                        <p className="text-gray-700 mb-4 line-clamp-2">
                          {announcement.summary}
                        </p>
                      )}

                      {/* 元數據 */}
                      <div className="flex items-center justify-between text-sm text-gray-600">
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            {formatDate(announcement.publish_date)}
                          </div>
                          <div className="flex items-center gap-1">
                            <Eye className="h-4 w-4" />
                            {announcement.views_count}
                          </div>
                          <div className="flex items-center gap-1">
                            <Heart className="h-4 w-4" />
                            {announcement.likes_count}
                          </div>
                        </div>

                        <Link href={`/announcements/${announcement.id}`}>
                          <Button variant="outline" size="sm" className="border-gray-400 text-black hover:bg-gray-100">
                            閱讀更多
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}