"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { getArticles, Article, processImageUrls } from "@/lib/api"

export default function ArticlesPage() {
  const [articles, setArticles] = useState<Article[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedTag, setSelectedTag] = useState("")

  useEffect(() => {
    fetchArticles()
  }, [])

  const fetchArticles = async () => {
    try {
      const data = await getArticles()
      
      // 處理圖片URL，將相對路徑轉換為完整URL
      const processedData = data.map(article => ({
        ...article,
        content: processImageUrls(article.content)
      }))
      
      setArticles(processedData)
    } catch (error) {
      console.error("Failed to fetch articles:", error)
      // Use mock data if API is not available
      setArticles([
        {
          id: 1,
          title: "如何管理日常壓力？5個實用技巧幫助你找回平靜",
          content:
            "現代生活節奏快速，每個人都面臨著各種壓力。學會有效管理壓力，是維護心理健康的重要技能。本文將分享5個實用的壓力管理技巧...",
          tags: ["壓力", "放鬆", "心理健康"],
          author: null,
          published_at: "2024-01-15T10:00:00Z",
        },
        {
          id: 2,
          title: "認識焦慮症：症狀、成因與治療方式",
          content:
            "焦慮症是常見的心理健康問題，影響著許多人的日常生活。了解焦慮症的症狀和成因，有助於及早發現並尋求適當的治療...",
          tags: ["焦慮症", "治療", "症狀"],
          author: null,
          published_at: "2024-01-10T14:30:00Z",
        },
        {
          id: 3,
          title: "建立健康的人際關係：溝通的藝術",
          content: "良好的人際關係是心理健康的重要基石。學會有效溝通，能夠幫助我們建立更深層、更有意義的人際連結...",
          tags: ["溝通", "人際關係", "社交技巧"],
          author: null,
          published_at: "2024-01-05T09:15:00Z",
        },
        {
          id: 4,
          title: "睡眠與心理健康的密切關係",
          content:
            "充足的睡眠對心理健康至關重要。睡眠不足會影響情緒調節、認知功能和整體心理狀態。本文探討睡眠與心理健康的關係...",
          tags: ["睡眠", "心理健康", "生活習慣"],
          author: null,
          published_at: "2024-01-01T16:45:00Z",
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const filteredArticles = articles.filter((article) => {
    const matchesSearch =
      article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      article.content.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesTag = !selectedTag || article.tags.includes(selectedTag)
    return matchesSearch && matchesTag
  })

  const allTags = [...new Set(articles.flatMap((article) => article.tags))]

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
        <div className="container mx-auto px-4">
          <div className="text-center">載入中...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-green-800 mb-4">心理健康文章</h1>
          <p className="text-xl text-green-600">探索心理健康知識，學習自我照顧的方法</p>
        </div>

        {/* Search and Filter */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <Input
              placeholder="搜尋文章..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1"
            />
            <div className="flex gap-2 flex-wrap">
              <Button variant={selectedTag === "" ? "default" : "outline"} onClick={() => setSelectedTag("")}>
                全部
              </Button>
              {allTags.map((tag) => (
                <Button
                  key={tag}
                  variant={selectedTag === tag ? "default" : "outline"}
                  onClick={() => setSelectedTag(tag)}
                >
                  {tag}
                </Button>
              ))}
            </div>
          </div>
        </div>

        {/* Articles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredArticles.map((article) => (
            <Card key={article.id} className="bg-white/90 backdrop-blur-sm hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start mb-2">
                  <div className="flex gap-1 flex-wrap">
                    {article.tags.slice(0, 2).map((tag, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {tag}
                      </Badge>
                    ))}
                    {article.tags.length > 2 && (
                      <Badge variant="outline" className="text-xs">
                        +{article.tags.length - 2}
                      </Badge>
                    )}
                  </div>
                  <span className="text-sm text-gray-500">
                    {new Date(article.published_at).toLocaleDateString("zh-TW")}
                  </span>
                </div>
                <CardTitle className="text-xl text-green-800 line-clamp-2">{article.title}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-gray-600 line-clamp-3">
                  {article.content.replace(/<[^>]*>/g, "").substring(0, 150)}...
                </p>

                {article.tags && article.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {article.tags.map((tag, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        #{tag}
                      </Badge>
                    ))}
                  </div>
                )}

                <Link href={`/articles/${article.id}`}>
                  <Button className="w-full bg-green-600 hover:bg-green-700 text-white">閱讀全文</Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredArticles.length === 0 && (
          <div className="text-center text-gray-500 mt-12">
            <p>沒有找到符合條件的文章</p>
          </div>
        )}
      </div>
    </div>
  )
}
