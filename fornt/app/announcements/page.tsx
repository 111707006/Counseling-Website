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
import { getAnnouncements, type Announcement as APIAnnouncement, type AnnouncementCategory as APIAnnouncementCategory } from '@/lib/api'

// 使用API中定義的介面
type AnnouncementCategory = APIAnnouncementCategory
type Announcement = APIAnnouncement

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
      
      // 使用API函數獲取公告列表
      const response = await getAnnouncements({
        search: searchQuery || undefined
      })
      setAnnouncements(response)
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
      default: return 'bg-brand-bg0'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-brand-bg p-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-text mx-auto"></div>
            <p className="mt-4 text-brand-text/70">載入中...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-brand-bg">
      <div className="max-w-6xl mx-auto p-4">
        {/* 頁面標題 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-brand-text mb-4">最新消息</h1>
          <p className="text-lg text-brand-text/70">掌握心理健康相關的重要資訊與動態</p>
        </div>

        {/* 搜尋區域 */}
        <Card className="mb-8 border-brand-orange/30">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              {/* 搜尋框 */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-brand-text/50" />
                <Input
                  placeholder="搜尋公告標題或內容..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 border-brand-orange/30 focus:border-brand-orange focus:ring-brand-orange"
                />
              </div>

              {/* 清除按鈕 */}
              {searchQuery && (
                <Button 
                  variant="outline" 
                  className="border-brand-orange/30 text-brand-text hover:bg-brand-orange/10"
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
              <p className="text-brand-text/50 text-lg">目前沒有符合條件的公告</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6">
            {announcements.map((announcement) => (
              <Card key={announcement.id} className="border-brand-orange/30 hover:shadow-lg transition-shadow duration-200">
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
                            <Badge variant="secondary" className="bg-brand-orange/20 text-brand-text border-brand-orange/40">
                              <Pin className="h-3 w-3 mr-1" />
                              置頂
                            </Badge>
                          )}
                          
                          {announcement.category && (
                            <Badge 
                              className="text-white bg-brand-orange"
                            >
                              {announcement.category.name}
                            </Badge>
                          )}
                        </div>
                      </div>

                      <Link href={`/announcements/${announcement.id}`}>
                        <h3 className="text-xl font-semibold text-brand-text hover:text-brand-orange transition-colors mb-2">
                          {announcement.title}
                        </h3>
                      </Link>

                      {announcement.summary && (
                        <p className="text-brand-text/70 mb-4 line-clamp-2">
                          {announcement.summary}
                        </p>
                      )}

                      {/* 元數據 */}
                      <div className="flex items-center justify-between text-sm text-brand-text/60">
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            {formatDate(announcement.publish_date)}
                          </div>
                          <div className="flex items-center gap-1">
                            <Eye className="h-4 w-4" />
                            {announcement.views_count}
                          </div>
                        </div>

                        <Link href={`/announcements/${announcement.id}`}>
                          <Button variant="outline" size="sm" className="border-brand-orange/40 text-brand-text hover:bg-brand-orange/10">
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