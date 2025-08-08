"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import {
  User,
  Briefcase,
  Heart,
  Users,
  HandIcon as Hands,
  UserCheck,
  Brain,
  Globe,
  Baby,
  GraduationCap,
  AlertCircle,
  Settings,
  Loader2,
} from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { getSpecialties, type Specialty } from "@/lib/api"

// 圖標映射（用於將專業領域名稱對應到圖標）
const iconMapping: Record<string, any> = {
  // 預設
  "全部": User,
  
  // 新的專業領域分類
  "自我探索": Hands,
  "壓力調適": AlertCircle,
  "人際關係": Users,
  "親密關係": Heart,
  "生涯諮商": Briefcase,
  "情緒調節": Heart,
  "親子溝通": Users,
  "家庭關係": Users,
  "創傷與失落": AlertCircle,
  "憂鬱與焦慮適應": Brain,
}

// 預設的全部分類
const defaultGeneralSpecialty = {
  id: 0,
  name: "全部",
  description: "查看所有心理師",
  is_active: true
}

export default function TherapistCategories() {
  const [selectedSpecialty, setSelectedSpecialty] = useState<number | null>(null)
  const [specialties, setSpecialties] = useState<Specialty[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    async function loadSpecialties() {
      try {
        setLoading(true)
        const data = await getSpecialties()
        // 加入"全部"選項
        const allSpecialties = [defaultGeneralSpecialty, ...data]
        setSpecialties(allSpecialties)
        setSelectedSpecialty(0) // 預設選擇"全部"
      } catch (err) {
        console.error('載入專業領域失敗:', err)
        setError('載入專業領域失敗，請稍後再試')
        // 發生錯誤時使用預設專業領域
        setSpecialties([defaultGeneralSpecialty])
        setSelectedSpecialty(0)
      } finally {
        setLoading(false)
      }
    }

    loadSpecialties()
  }, [])

  const handleSpecialtyClick = (specialtyId: number) => {
    setSelectedSpecialty(specialtyId)
    router.push(`/therapists/${specialtyId}`)
  }

  return (
    <div className="min-h-screen bg-texture bg-cover bg-center bg-no-repeat flex items-center justify-center font-['GenRyuMin2TC-B'],serif">
      <div className="container mx-auto p-6 flex flex-col md:flex-row gap-8">
        {/* 左側文字區塊 */}
        <div className="md:w-1/2 flex flex-col justify-center">
          <div className="mb-6">
            <div className="text-brand-orange text-lg font-semibold mb-2">張老師基金會台北分事務所</div>
            <h1 className="text-4xl font-extrabold text-brand-text mb-2 leading-tight">依據專業領域分類</h1>
            <h2 className="text-3xl font-extrabold text-brand-text mb-4">快速媒合專業心理師</h2>
            <p className="text-base text-brand-text mb-2">
              每個人都有感到辛苦的時候，無論你正經歷什麼，都值得被理解與支持。<br />
              請看右側的專業領域分類，選擇最符合您需求的治療方向，我們將為您推薦具有相關專長的心理師，
              一步步走向安心與自我照顧的旅程。若希望尋求專業協助，請點選下方預約表單。
            </p>
          </div>
          <button
            className="mt-4 px-8 py-3 bg-brand-button hover:bg-brand-button/80 text-white text-lg font-bold rounded-full shadow transition-all w-fit"
            onClick={() => router.push('/appointments/book')}
          >
            填寫預約表單
          </button>
        </div>

        {/* 右側分類卡片區塊 */}
        <div className="md:w-1/2">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="w-8 h-8 animate-spin text-brand-orange" />
              <span className="ml-2 text-brand-orange">載入中...</span>
            </div>
          ) : error ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-center">
                <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-2" />
                <p className="text-red-600">{error}</p>
                <button 
                  onClick={() => window.location.reload()} 
                  className="mt-2 px-4 py-2 bg-brand-orange text-white rounded-lg hover:opacity-80 transition-opacity"
                >
                  重新載入
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 max-h-96 overflow-y-auto">
              {specialties.map((specialty) => {
                const IconComponent = iconMapping[specialty.name] || Settings
                const isHighlighted = selectedSpecialty === specialty.id
                return (
                  <Card
                    key={specialty.id}
                    className={`cursor-pointer rounded-xl border bg-brand-bg hover:bg-brand-orange/10 transition-all duration-200 shadow-sm flex flex-col items-center p-3 text-sm ${
                      isHighlighted ? 'ring-2 ring-brand-orange border-brand-orange' : 'border-brand-orange/60'
                    }`}
                    onClick={() => handleSpecialtyClick(specialty.id)}
                  >
                    <CardContent className="flex flex-col items-center p-0 space-y-2 text-center">
                      <div className="p-2 rounded-full bg-brand-orange/20">
                        <IconComponent className="w-6 h-6 text-brand-orange" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-brand-text">{specialty.name}</h3>
                        <p className="text-xs text-brand-orange mt-1">{specialty.description || "專業心理治療服務"}</p>
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
