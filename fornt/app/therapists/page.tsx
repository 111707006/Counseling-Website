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
  
  // 理論取向
  "認知行為治療": Brain,
  "心理動力取向": Brain,
  "人本主義取向": Heart,
  "存在主義治療": Hands,
  "完形治療": Brain,
  "敘事治療": Heart,
  "焦點解決短期治療": Settings,
  "接納與承諾治療": Heart,
  
  // 議題專精
  "焦慮症治療": AlertCircle,
  "憂鬱症治療": Heart,
  "創傷治療": AlertCircle,
  "成癮治療": AlertCircle,
  "飲食障礙": Heart,
  "睡眠障礙": Brain,
  "強迫症治療": Brain,
  "恐慌症治療": AlertCircle,
  "ADHD": Brain,
  "自閉症譜系": Brain,
  
  // 關係與家庭
  "伴侶諮商": Heart,
  "婚姻治療": Heart,
  "家族治療": Users,
  "親子關係": Users,
  "離婚諮商": Heart,
  
  // 特定族群
  "兒童心理治療": Baby,
  "青少年諮商": GraduationCap,
  "老人心理學": Users,
  "LGBTQ+友善": Heart,
  "多元文化": Globe,
  
  // 職場與生活
  "職場諮商": Briefcase,
  "生涯諮商": Briefcase,
  "壓力管理": AlertCircle,
  "情緒管理": Heart,
  "人際關係": Users,
  "自我探索": Hands,
  "生命意義": Hands,
  
  // 特殊治療方式
  "藝術治療": Heart,
  "音樂治療": Heart,
  "舞蹈治療": Heart,
  "遊戲治療": Baby,
  "沙遊治療": Baby,
  "生理回饋治療": Brain,
  "正念療法": Brain,
  "催眠治療": Brain,
  
  // 性相關
  "性治療": UserCheck,
  "性創傷": UserCheck,
}

// 預設的全部分類
const defaultGeneralSpecialty = {
  id: 0,
  name: "全部",
  description: "查看所有心理師",
  category: { id: 0, name: "全部", description: "" },
  category_name: "全部",
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
            <div className="text-orange-700 text-lg font-semibold mb-2">張老師基金會台北分事務所</div>
            <h1 className="text-4xl font-extrabold text-black mb-2 leading-tight">依據專業領域分類</h1>
            <h2 className="text-3xl font-extrabold text-black mb-4">快速媒合專業心理師</h2>
            <p className="text-base text-zinc-800 mb-2">
              每個人都有感到辛苦的時候，無論你正經歷什麼，都值得被理解與支持。<br />
              請看右側的專業領域分類，選擇最符合您需求的治療方向，我們將為您推薦具有相關專長的心理師，
              一步步走向安心與自我照顧的旅程。若希望尋求專業協助，請點選下方預約表單。
            </p>
          </div>
          <button
            className="mt-4 px-8 py-3 bg-orange-500 hover:bg-orange-600 text-white text-lg font-bold rounded-full shadow transition-all w-fit"
            onClick={() => router.push('/appointments/book')}
          >
            填寫預約表單
          </button>
        </div>

        {/* 右側分類卡片區塊 */}
        <div className="md:w-1/2">
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
              <span className="ml-2 text-orange-600">載入中...</span>
            </div>
          ) : error ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-center">
                <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-2" />
                <p className="text-red-600">{error}</p>
                <button 
                  onClick={() => window.location.reload()} 
                  className="mt-2 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
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
                    className={`cursor-pointer rounded-xl border bg-white/90 hover:bg-orange-50 transition-all duration-200 shadow-sm flex flex-col items-center p-3 text-sm ${
                      isHighlighted ? 'ring-2 ring-orange-400 border-orange-300' : 'border-orange-200'
                    }`}
                    onClick={() => handleSpecialtyClick(specialty.id)}
                  >
                    <CardContent className="flex flex-col items-center p-0 space-y-2 text-center">
                      <div className="p-2 rounded-full bg-orange-100">
                        <IconComponent className="w-6 h-6 text-orange-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-orange-900">{specialty.name}</h3>
                        {specialty.category_name !== "全部" && (
                          <p className="text-xs font-medium text-orange-700">{specialty.category_name}</p>
                        )}
                        <p className="text-xs text-orange-600 mt-1">{specialty.description || "專業心理治療服務"}</p>
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
