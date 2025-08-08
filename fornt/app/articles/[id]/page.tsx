"use client"

import { useState, useEffect } from "react"
import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel"
import Link from "next/link"
import Image from "next/image"
import { getArticle, Article, processImageUrls } from "@/lib/api"

export default function ArticleDetailPage() {
  const params = useParams()
  const [article, setArticle] = useState<Article | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>("")

  useEffect(() => {
    if (params.id) {
      fetchArticle(Number(params.id))
    }
  }, [params.id])

  const fetchArticle = async (id: number) => {
    try {
      const data = await getArticle(id)
      
      // 處理圖片URL，將相對路徑轉換為完整URL
      data.content = processImageUrls(data.content)
      
      setArticle(data)
    } catch (error) {
      console.error("Failed to fetch article:", error)
      setError("無法載入文章內容")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
        <div className="container mx-auto px-4">
          <div className="text-center">載入中...</div>
        </div>
      </div>
    )
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <p className="text-red-600 mb-4">{error || "文章不存在"}</p>
            <Link href="/articles">
              <Button variant="outline">
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回文章列表
              </Button>
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <div className="mb-6">
            <Link href="/articles">
              <Button variant="outline" className="mb-4">
                <ArrowLeft className="w-4 h-4 mr-2" />
                返回文章列表
              </Button>
            </Link>
          </div>

          {/* Article Content */}
          <Card className="bg-white/90 backdrop-blur-sm">
            <CardHeader className="pb-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex gap-2 flex-wrap">
                  {article.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary" className="text-sm">
                      {tag}
                    </Badge>
                  ))}
                </div>
                <span className="text-sm text-gray-500">
                  {new Date(article.published_at).toLocaleDateString("zh-TW", {
                    year: "numeric",
                    month: "long",
                    day: "numeric"
                  })}
                </span>
              </div>
              <CardTitle className="text-3xl text-green-800 leading-tight">
                {article.title}
              </CardTitle>
              
              {/* Display excerpt if available */}
              {article.excerpt && (
                <div className="mt-4">
                  <p className="text-gray-600 text-lg leading-relaxed">{article.excerpt}</p>
                </div>
              )}
            </CardHeader>
            
            {/* Image Carousel - Display images if available */}
            {article.images && article.images.length > 0 && (
              <div className="px-6 pb-6">
                <div className="relative">
                  <Carousel 
                    className="w-full max-w-4xl mx-auto"
                    opts={{
                      align: "start",
                      loop: true,
                    }}
                  >
                    <CarouselContent>
                      {article.images
                        .sort((a, b) => a.order - b.order)
                        .map((image, index) => (
                          <CarouselItem key={image.id}>
                            <div className="relative w-full overflow-hidden rounded-lg shadow-lg bg-white flex items-center justify-center" style={{ height: '400px' }}>
                              <Image
                                src={image.image_url}
                                alt={image.caption || `文章圖片 ${index + 1}`}
                                fill
                                className="object-contain transition-transform duration-300 hover:scale-105"
                              />
                              {/* Image Caption */}
                              {image.caption && (
                                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
                                  <p className="text-white text-sm">{image.caption}</p>
                                </div>
                              )}
                            </div>
                          </CarouselItem>
                        ))}
                    </CarouselContent>
                    {article.images.length > 1 && (
                      <>
                        <CarouselPrevious className="left-4" />
                        <CarouselNext className="right-4" />
                      </>
                    )}
                  </Carousel>
                  
                  {/* Image Count Indicator */}
                  {article.images.length > 1 && (
                    <div className="text-center mt-2">
                      <p className="text-sm text-gray-500">
                        {article.images.length} 張圖片
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            <CardContent className="prose prose-lg max-w-none">
              <div 
                className="text-gray-700 leading-relaxed article-content"
                dangerouslySetInnerHTML={{ __html: article.content }}
                style={{
                  lineHeight: '1.8',
                }}
              />
              
              <style jsx>{`
                .article-content img {
                  max-width: 600px;
                  width: 100%;
                  height: auto;
                  border-radius: 8px;
                  margin: 16px auto;
                  display: block;
                  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                }
                
                /* 圖片大小樣式 */
                .article-content .img-xs { max-width: 200px !important; }
                .article-content .img-sm { max-width: 300px !important; }
                .article-content .img-md { max-width: 500px !important; }
                .article-content .img-lg { max-width: 700px !important; }
                .article-content .img-full { width: 100% !important; max-width: none !important; }
                
                /* 圖片排版樣式 */
                .article-content .img-center {
                  display: block !important;
                  margin: 16px auto !important;
                  max-width: 600px !important;
                }
                .article-content .img-left {
                  float: left !important;
                  margin: 0 16px 16px 0 !important;
                  max-width: 400px !important;
                }
                .article-content .img-right {
                  float: right !important;
                  margin: 0 0 16px 16px !important;
                  max-width: 400px !important;
                }
                
                /* 圖片效果樣式 */
                .article-content .img-shadow {
                  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                  border-radius: 8px !important;
                }
                .article-content .img-rounded {
                  border-radius: 12px !important;
                }
                .article-content .img-circle {
                  border-radius: 50% !important;
                  width: 200px !important;
                  height: 200px !important;
                  object-fit: cover !important;
                }
                .article-content .img-border {
                  border: 3px solid #e5e7eb !important;
                  padding: 8px !important;
                }
                .article-content .img-hover {
                  transition: transform 0.3s ease !important;
                  cursor: pointer !important;
                }
                .article-content .img-hover:hover {
                  transform: scale(1.05) !important;
                }
                .article-content .img-grayscale {
                  filter: grayscale(100%) !important;
                }
                .article-content .img-grayscale:hover {
                  filter: grayscale(0%) !important;
                  transition: filter 0.3s ease !important;
                }
                
                @media (max-width: 768px) {
                  .article-content img,
                  .article-content .img-left,
                  .article-content .img-right {
                    float: none !important;
                    display: block !important;
                    margin: 12px auto !important;
                    max-width: 100% !important;
                  }
                  .article-content .img-circle {
                    width: 150px !important;
                    height: 150px !important;
                  }
                }
                .article-content h1, .article-content h2, .article-content h3 {
                  color: #166534;
                  margin-top: 32px;
                  margin-bottom: 16px;
                }
                .article-content h1 {
                  font-size: 1.875rem;
                  font-weight: 700;
                }
                .article-content h2 {
                  font-size: 1.5rem;
                  font-weight: 600;
                }
                .article-content h3 {
                  font-size: 1.25rem;
                  font-weight: 600;
                }
                .article-content p {
                  margin-bottom: 16px;
                }
                .article-content ul, .article-content ol {
                  padding-left: 24px;
                  margin-bottom: 16px;
                }
                .article-content li {
                  margin-bottom: 8px;
                }
                .article-content blockquote {
                  border-left: 4px solid #10b981;
                  padding-left: 16px;
                  margin: 24px 0;
                  font-style: italic;
                  background-color: #f0fdf4;
                  padding: 16px;
                  border-radius: 4px;
                }
                .article-content table {
                  width: 100%;
                  border-collapse: collapse;
                  margin: 24px 0;
                }
                .article-content th, .article-content td {
                  border: 1px solid #d1d5db;
                  padding: 12px;
                  text-align: left;
                }
                .article-content th {
                  background-color: #f9fafb;
                  font-weight: 600;
                }
              `}</style>
              
              {/* Tags Section */}
              {article.tags && article.tags.length > 0 && (
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <h3 className="text-lg font-semibold text-green-800 mb-3">相關標籤</h3>
                  <div className="flex flex-wrap gap-2">
                    {article.tags.map((tag, index) => (
                      <Badge key={index} variant="outline" className="text-sm">
                        #{tag}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Navigation */}
          <div className="mt-8 text-center">
            <Link href="/articles">
              <Button className="bg-green-600 hover:bg-green-700 text-white">
                瀏覽更多文章
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}