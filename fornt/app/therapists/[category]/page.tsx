"use client"

import { useParams, useRouter } from "next/navigation"
import { useState, useEffect } from "react"
import { ArrowLeft, Star, Clock, MapPin, Phone, Mail, Loader2, AlertCircle } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { getTherapists, getTherapistsBySpecialty, getSpecialties, type TherapistProfile, type Specialty } from "@/lib/api"

export default function TherapistListPage() {
  const params = useParams()
  const router = useRouter()
  const specialtyId = params.category as string
  
  const [therapists, setTherapists] = useState<TherapistProfile[]>([])
  const [specialties, setSpecialties] = useState<Specialty[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [specialtyName, setSpecialtyName] = useState("心理師")

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true)
        setError(null)

        // 載入專業領域資料來獲取專業領域名稱
        const specialtiesData = await getSpecialties()
        setSpecialties(specialtiesData)

        // 根據專業領域ID載入心理師資料
        let therapistsData: TherapistProfile[]
        
        if (specialtyId === "0") {
          // 載入所有心理師
          therapistsData = await getTherapists()
          setSpecialtyName("全部心理師")
        } else {
          // 根據專業領域篩選心理師
          const specialtyIdNum = parseInt(specialtyId, 10)
          if (!isNaN(specialtyIdNum)) {
            const selectedSpecialty = specialtiesData.find(spec => spec.id === specialtyIdNum)
            setSpecialtyName(selectedSpecialty?.name || "心理師")
            
            therapistsData = await getTherapistsBySpecialty(specialtyIdNum)
          } else {
            therapistsData = await getTherapists()
            setSpecialtyName("心理師")
          }
        }

        setTherapists(therapistsData)
      } catch (err) {
        console.error('載入心理師資料失敗:', err)
        setError('載入心理師資料失敗，請稍後再試')
        setTherapists([])
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [specialtyId])

  const handleBooking = (therapistId: number) => {
    // 導向預約頁面，並帶上心理師ID參數
    router.push(`/appointments/book?therapist=${therapistId}`)
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
          <h1 className="text-3xl font-bold text-orange-800 mb-2">{specialtyName} - 專業心理師</h1>
          <p className="text-orange-600">為您推薦具備相關專業領域的心理師</p>
        </div>

        {/* 載入狀態 */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
            <span className="ml-2 text-orange-600">載入中...</span>
          </div>
        ) : error ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-center">
              <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-2" />
              <p className="text-red-600 mb-4">{error}</p>
              <Button 
                onClick={() => window.location.reload()} 
                className="bg-orange-500 hover:bg-orange-600 text-white"
              >
                重新載入
              </Button>
            </div>
          </div>
        ) : (
          <>
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
                          {therapist.specialties.length === 0 && therapist.specialties_text && (
                            <span className="px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full text-xs">
                              {therapist.specialties_text}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* 學歷 */}
                      {therapist.education && (
                        <div className="text-orange-700 text-sm">
                          <strong>學歷：</strong>{therapist.education}
                        </div>
                      )}

                      {/* 經歷 */}
                      {therapist.experience && (
                        <div className="text-orange-700 text-sm">
                          <strong>經歷：</strong>{therapist.experience}
                        </div>
                      )}

                      {/* 諮商模式與收費 */}
                      {therapist.consultation_modes.length > 0 && (
                        <div className="text-orange-700 text-sm">
                          <strong>諮商方式：</strong>
                          {therapist.consultation_modes.map(mode => 
                            `${mode === 'online' ? '線上' : '實體'}（$${therapist.pricing[mode] || 'N/A'}）`
                          ).join('、')}
                        </div>
                      )}

                      {/* 可預約時段 */}
                      {therapist.available_times.length > 0 && (
                        <div className="text-orange-700 text-xs">
                          <strong>可預約時段：</strong>
                          <div className="mt-1 flex flex-wrap gap-1">
                            {therapist.available_times.slice(0, 3).map((time) => (
                              <span key={time.id} className="px-1.5 py-0.5 bg-green-100 text-green-700 rounded text-xs">
                                {time.day_of_week} {time.start_time}-{time.end_time}
                              </span>
                            ))}
                            {therapist.available_times.length > 3 && (
                              <span className="text-orange-600 text-xs">等{therapist.available_times.length}個時段</span>
                            )}
                          </div>
                        </div>
                      )}

                      {/* 信念 */}
                      {therapist.beliefs && (
                        <p className="text-orange-600 text-xs leading-relaxed">{therapist.beliefs}</p>
                      )}

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
                <p className="text-orange-600 text-lg">此專業領域暫無可預約的心理師</p>
                <p className="text-orange-500 mt-2">請選擇其他專業領域或稍後再試</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
