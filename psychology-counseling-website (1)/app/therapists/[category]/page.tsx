"use client"

import { useParams, useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { ArrowLeft, Star, Clock, MapPin, Phone, Mail } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { therapistService, type TherapistProfile, type SpecialtyCategory } from "@/lib/api"
import dynamic from "next/dynamic"

const categoryNames = {
  general: "不分類",
  workplace: "職場問題",
  relationship: "感情問題",
  family: "家庭問題",
  "life-meaning": "生命意義",
  "sex-counseling": "性諮商",
  biofeedback: "生理回饋",
  multicultural: "多元文化議題",
  children: "兒童",
  adolescent: "青少年",
  "special-situations": "特殊狀況",
  "general-adult": "一般成人心理問題",
}

function TherapistListPage() {
  const params = useParams()
  const router = useRouter()
  const category = params.category as string
  const categoryName = categoryNames[category as keyof typeof categoryNames] || "心理師"
  
  const [therapists, setTherapists] = useState<TherapistProfile[]>([])
  const [categories, setCategories] = useState<SpecialtyCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (!mounted) return

    const fetchTherapists = async () => {
      try {
        setLoading(true)
        
        // 獲取所有心理師
        let therapistData: TherapistProfile[]
        
        if (category === 'general') {
          // 顯示所有心理師
          therapistData = await therapistService.getProfiles()
        } else {
          // TODO: 根據分類篩選心理師
          // 目前先顯示所有心理師，之後可以根據專業領域分類篩選
          therapistData = await therapistService.getProfiles()
        }
        
        setTherapists(therapistData)
      } catch (err) {
        setError('無法載入心理師資料，請稍後再試')
        console.error('Failed to fetch therapists:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchTherapists()
  }, [category, mounted])

  if (!mounted) {
    return null
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">載入中...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
        <div className="flex items-center justify-center h-64">
          <div className="text-red-500">{error}</div>
        </div>
      </div>
    )
  }

  const handleBooking = (therapistId: number) => {
    // 這裡可以實現預約功能
    alert(`預約心理師 ID: ${therapistId}`)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100">
      <div className="container mx-auto p-6">
        {/* 返回按鈕 */}
        <Button
          variant="ghost"
          onClick={() => router.back()}
          className="mb-6 text-orange-700 hover:text-orange-800 hover:bg-orange-200"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          返回分類選擇
        </Button>

        {/* 頁面標題 */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-orange-800 mb-2">{categoryName} - 心理師介紹</h1>
          <p className="text-orange-600">為您推薦專業的心理師</p>
        </div>

        {/* 心理師列表 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {therapists.map((therapist) => (
            <Card
              key={therapist.id}
              className="bg-white border-orange-200 hover:shadow-xl transition-all duration-300 hover:scale-105"
            >
              <CardContent className="p-4">
                <div className="text-center mb-3">
                  <img
                    src={therapist.photo || "/placeholder.svg"}
                    alt={therapist.name}
                    className="w-20 h-20 rounded-full mx-auto mb-2 border-3 border-orange-200"
                  />
                  <h3 className="text-lg font-bold text-orange-900">{therapist.name}</h3>
                  <p className="text-orange-600 font-medium text-sm">{therapist.title}</p>
                  <p className="text-orange-500 text-xs">證照：{therapist.license_number}</p>
                </div>

                <div className="space-y-2">
                  {/* 專長 */}
                  <div>
                    <h4 className="font-semibold text-orange-800 mb-1 text-sm">專長領域：</h4>
                    <div className="flex flex-wrap gap-1">
                      {therapist.specialties.map((specialty) => (
                        <span key={specialty.id} className="px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full text-xs">
                          {specialty.name}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* 服務方式 */}
                  <div>
                    <h4 className="font-semibold text-orange-800 mb-1 text-sm">諮詢方式：</h4>
                    <div className="flex flex-wrap gap-1">
                      {therapist.consultation_modes.map((mode) => (
                        <span key={mode} className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
                          {mode === 'online' ? '線上' : '實體'}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* 收費 */}
                  <div>
                    <h4 className="font-semibold text-orange-800 mb-1 text-sm">收費：</h4>
                    <div className="flex flex-wrap gap-2 text-xs text-orange-700">
                      {Object.entries(therapist.pricing).map(([mode, price]) => (
                        <span key={mode}>
                          {mode === 'online' ? '線上' : '實體'}: NT$ {price}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* 學歷 */}
                  <div className="text-orange-700 text-xs">
                    <strong>學歷：</strong> {therapist.education}
                  </div>

                  {/* 經驗 */}
                  <div className="text-orange-700 text-xs">
                    <strong>經驗：</strong> {therapist.experience}
                  </div>

                  {/* 理念 */}
                  <div className="text-orange-600 text-xs leading-relaxed">
                    <strong>諮商信念：</strong> {therapist.beliefs}
                  </div>

                  {/* 預約按鈕 */}
                  <Button
                    onClick={() => handleBooking(therapist.id)}
                    className="w-full bg-gradient-to-r from-orange-400 to-orange-500 hover:from-orange-500 hover:to-orange-600 text-white font-semibold py-1.5 text-sm rounded-lg transition-all duration-300"
                  >
                    立即預約
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* 如果沒有心理師 */}
        {therapists.length === 0 && (
          <div className="text-center py-12">
            <p className="text-orange-600 text-lg">此分類暫無可預約的心理師</p>
            <p className="text-orange-500 mt-2">請選擇其他分類或稍後再試</p>
          </div>
        )}
      </div>
    </div>
  )
}

// 使用動態導入避免 hydration 錯誤
export default dynamic(() => Promise.resolve(TherapistListPage), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 p-4">
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">載入中...</div>
      </div>
    </div>
  )
})
