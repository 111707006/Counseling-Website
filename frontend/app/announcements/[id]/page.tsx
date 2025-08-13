'use client'

import React, { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { 
  Calendar, 
  Pin, 
  ArrowLeft, 
  User, 
  Clock,
  Share2,
  AlertTriangle 
} from 'lucide-react'

interface AnnouncementCategory {
  id: number
  name: string
  color: string
}

interface AnnouncementImage {
  id: number
  image: string
  image_url: string
  caption: string
  order: number
}

interface AnnouncementDetail {
  id: number
  title: string
  summary: string
  content: string
  category?: AnnouncementCategory
  featured_image_url?: string
  additional_images: AnnouncementImage[]
  priority: 'low' | 'medium' | 'high'
  priority_display: string
  is_pinned: boolean
  publish_date: string
  expire_date?: string
  author: {
    id: number
    username: string
  }
  views_count: number
  likes_count: number
  can_display: boolean
  is_expired: boolean
  created_at: string
  updated_at: string
}

export default function AnnouncementDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [announcement, setAnnouncement] = useState<AnnouncementDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const announcementId = params.id as string

  useEffect(() => {
    if (announcementId) {
      fetchAnnouncement()
    }
  }, [announcementId])

  const fetchAnnouncement = async () => {
    try {
      setLoading(true)
      const response = await fetch(`http://localhost:8000/api/announcements/${announcementId}/`)
      
      if (response.ok) {
        const data = await response.json()
        setAnnouncement(data)
      } else if (response.status === 404) {
        setError('找不到該公告')
      } else {
        setError('載入公告時發生錯誤')
      }
    } catch (error) {
      console.error('Error fetching announcement:', error)
      setError('網路連線錯誤')
    } finally {
      setLoading(false)
    }
  }


  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: announcement?.title,
        text: announcement?.summary,
        url: window.location.href,
      })
    } else {
      // 複製到剪貼板作為備用方案
      navigator.clipboard.writeText(window.location.href)
      alert('連結已複製到剪貼板')
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
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
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">載入中...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !announcement) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
        <div className="max-w-4xl mx-auto">
          <Card className="mt-12">
            <CardContent className="text-center py-12">
              <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <h2 className="text-xl font-semibold text-gray-900 mb-2">載入失敗</h2>
              <p className="text-gray-600 mb-6">{error || '無法載入公告內容'}</p>
              <div className="flex gap-4 justify-center">
                <Button onClick={() => router.back()}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  返回上一頁
                </Button>
                <Button variant="outline" onClick={() => window.location.href = '/announcements'}>
                  查看所有公告
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto p-4">
        {/* 返回按鈕 */}
        <div className="mb-6">
          <Button 
            variant="ghost" 
            onClick={() => router.back()}
            className="text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            返回列表
          </Button>
        </div>

        <Card>
          <CardContent className="p-8">
            {/* 標題區域 */}
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-4 flex-wrap">
                {announcement.is_pinned && (
                  <Badge variant="secondary" className="bg-yellow-100 text-yellow-800">
                    <Pin className="h-3 w-3 mr-1" />
                    置頂
                  </Badge>
                )}
                
                {announcement.category && (
                  <Badge 
                    className="text-white"
                    style={{ backgroundColor: announcement.category.color }}
                  >
                    {announcement.category.name}
                  </Badge>
                )}
                
                <Badge 
                  className={`text-white ${getPriorityColor(announcement.priority)}`}
                >
                  {announcement.priority_display}
                </Badge>

                {announcement.is_expired && (
                  <Badge variant="destructive">
                    已過期
                  </Badge>
                )}
              </div>

              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                {announcement.title}
              </h1>

              {announcement.summary && (
                <p className="text-lg text-gray-600 mb-6">
                  {announcement.summary}
                </p>
              )}

              {/* 元數據 */}
              <div className="flex items-center justify-between text-sm text-gray-500 mb-6">
                <div className="flex items-center gap-6 flex-wrap">
                  <div className="flex items-center gap-1">
                    <User className="h-4 w-4" />
                    發布者：{announcement.author.username}
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {formatDate(announcement.publish_date)}
                  </div>
                  {announcement.expire_date && (
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      到期：{formatDate(announcement.expire_date)}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-4">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleShare}
                  >
                    <Share2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>

            <Separator className="mb-8" />

            {/* 特色圖片 */}
            {announcement.featured_image_url && (
              <div className="mb-8">
                <div className="relative w-full h-64 md:h-96 rounded-lg overflow-hidden bg-gray-100">
                  <Image
                    src={announcement.featured_image_url}
                    alt={announcement.title}
                    fill
                    className="object-cover"
                  />
                </div>
              </div>
            )}

            {/* 內容 */}
            <div className="prose prose-lg max-w-none mb-8">
              <div
                dangerouslySetInnerHTML={{ 
                  __html: announcement.content 
                }}
                className="text-gray-700 leading-relaxed"
              />
            </div>

            {/* 附加圖片 */}
            {announcement.additional_images.length > 0 && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">相關圖片</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {announcement.additional_images.map((image) => (
                    <div key={image.id} className="space-y-2">
                      <div className="relative h-48 rounded-lg overflow-hidden bg-gray-100">
                        <Image
                          src={image.image_url}
                          alt={image.caption || `圖片 ${image.order}`}
                          fill
                          className="object-cover"
                        />
                      </div>
                      {image.caption && (
                        <p className="text-sm text-gray-600 text-center">
                          {image.caption}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <Separator className="mb-6" />

            {/* 底部操作區 */}
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                最後更新：{formatDate(announcement.updated_at)}
              </div>

              <div className="flex gap-3">
                
                <Button onClick={handleShare} className="flex items-center gap-2">
                  <Share2 className="h-4 w-4" />
                  分享
                </Button>

                <Link href="/announcements">
                  <Button variant="outline">
                    查看更多公告
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}