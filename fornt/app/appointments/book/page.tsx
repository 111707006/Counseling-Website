"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Checkbox } from "@/components/ui/checkbox"
import { Calendar, Plus, Trash2, Loader2, User, Shield, Briefcase, Users, Clock, MessageSquare } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { 
  getSpecialties, 
  getTherapistsBySpecialty, 
  getTherapists,
  createAppointment,
  type Specialty, 
  type TherapistProfile, 
  type AppointmentCreateRequest,
  type PreferredPeriod
} from "@/lib/api"

export default function BookAppointmentPage() {
  const searchParams = useSearchParams()
  const { toast } = useToast()

  // 狀態管理
  const [specialties, setSpecialties] = useState<Specialty[]>([])
  const [therapists, setTherapists] = useState<TherapistProfile[]>([])
  const [filteredTherapists, setFilteredTherapists] = useState<TherapistProfile[]>([])
  const [loading, setLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [loadingTherapists, setLoadingTherapists] = useState(false)

  // 表單資料
  const [formData, setFormData] = useState<AppointmentCreateRequest>({
    email: "",
    id_number: "",
    consultation_type: "offline",
    therapist: undefined,
    specialty: undefined,
    preferred_periods: [
      { date: "", periods: [] }
    ],
    name: "",
    phone: "",
    main_concerns: "",
    previous_therapy: false,
    urgency: "medium",
    special_needs: "",
  })

  // 初始化載入資料
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true)
        const [specialtiesData, therapistsData] = await Promise.all([
          getSpecialties(),
          getTherapists()
        ])
        
        setSpecialties(specialtiesData)
        setTherapists(therapistsData)
        setFilteredTherapists(therapistsData)
      } catch (error) {
        console.error('載入資料失敗:', error)
        toast({
          title: "載入失敗",
          description: "無法載入初始資料，請重新整理頁面",
          variant: "destructive",
        })
      } finally {
        setLoading(false)
      }
    }

    loadInitialData()
  }, [toast])

  // 當選擇專業領域時，篩選對應的心理師
  useEffect(() => {
    if (formData.specialty && therapists.length > 0) {
      const filtered = therapists.filter(therapist => 
        therapist.specialties.some(s => s.id === formData.specialty)
      )
      setFilteredTherapists(filtered)
      
      // 如果當前選擇的心理師不在篩選結果中，清除選擇
      if (formData.therapist && !filtered.some(t => t.id === formData.therapist)) {
        setFormData(prev => ({ ...prev, therapist: undefined }))
      }
    } else {
      setFilteredTherapists(therapists)
    }
  }, [formData.specialty, therapists, formData.therapist])

  // 新增偏好時間
  const addPreferredPeriod = () => {
    setFormData(prev => ({
      ...prev,
      preferred_periods: [
        ...(prev.preferred_periods || []),
        { date: "", periods: [] }
      ]
    }))
  }

  // 移除偏好時間
  const removePreferredPeriod = (index: number) => {
    setFormData(prev => ({
      ...prev,
      preferred_periods: prev.preferred_periods?.filter((_, i) => i !== index) || []
    }))
  }

  // 更新偏好時間
  const updatePreferredPeriod = (index: number, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      preferred_periods: prev.preferred_periods?.map((period, i) => 
        i === index ? { ...period, [field]: value } : period
      ) || []
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      // 除錯：印出要發送的資料
      console.log('發送的表單資料:', formData)
      const result = await createAppointment(formData)
      toast({
        title: "預約成功",
        description: "您的預約已提交！我們會透過Email與您聯繫確認時間。",
      })
      
      // Reset form
      setFormData({
        email: "",
        id_number: "",
        consultation_type: "offline",
        therapist: undefined,
        specialty: undefined,
        preferred_periods: [
          { date: "", periods: [] }
        ],
        name: "",
        phone: "",
        main_concerns: "",
        previous_therapy: false,
        urgency: "medium",
        special_needs: "",
      })
      
    } catch (error) {
      console.error('預約提交失敗:', error)
      toast({
        title: "預約失敗",
        description: "請檢查您的資料並重試，或聯繫我們的客服。",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
        <div className="container mx-auto px-4 flex justify-center items-center min-h-[400px]">
          <div className="flex items-center space-x-2">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>載入中...</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8" style={{backgroundImage: 'url("/images/bg-texture.png")', backgroundSize: 'cover', backgroundPosition: 'center'}}>
      <div className="container mx-auto px-4">
        <div className="max-w-2xl mx-auto">
          <Card className="bg-white/95 backdrop-blur-sm shadow-xl">
            <CardHeader className="text-center pb-4">
              <CardTitle className="text-2xl text-green-800 flex items-center justify-center gap-2">
                <Calendar className="h-6 w-6" />
                預約心理諮商
              </CardTitle>
              <p className="text-green-600 mt-1 text-sm">請依序填寫以下資料，我們會透過Email與您聯繫確認時間</p>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                
                {/* 1. 基本資料 */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4 text-green-600" />
                    <h3 className="text-lg font-bold text-green-800">基本資料</h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                      <Label htmlFor="name" className="font-semibold text-gray-700">姓名 <span className="text-red-500">*</span></Label>
                      <Input
                        id="name"
                        value={formData.name || ""}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="請輸入您的姓名"
                        required
                        className="h-9"
                      />
                    </div>
                    <div>
                      <Label htmlFor="phone" className="font-semibold text-gray-700">聯絡電話 <span className="text-red-500">*</span></Label>
                      <Input
                        id="phone"
                        value={formData.phone || ""}
                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                        placeholder="09XX-XXX-XXX"
                        required
                        className="h-9"
                      />
                    </div>
                    <div>
                      <Label htmlFor="email" className="font-semibold text-gray-700">電子郵件 <span className="text-red-500">*</span></Label>
                      <Input
                        id="email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        placeholder="example@email.com"
                        required
                        className="h-9"
                      />
                    </div>
                  </div>
                </div>

                {/* 2. 身分證字號 */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Shield className="h-4 w-4 text-green-600" />
                    <h3 className="text-lg font-bold text-green-800">身分驗證</h3>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <Label htmlFor="id_number" className="font-semibold text-gray-700">身分證字號 <span className="text-red-500">*</span></Label>
                      <Input
                        id="id_number"
                        value={formData.id_number}
                        onChange={(e) => setFormData({ ...formData, id_number: e.target.value })}
                        placeholder="A123456789"
                        required
                        className="h-9"
                      />
                    </div>
                    <div className="flex items-end">
                      <p className="text-xs text-gray-500">此資訊僅用於身分驗證，採加密保護</p>
                    </div>
                  </div>
                </div>

                {/* 3. 專業領域與心理師選擇 (選填) */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Briefcase className="h-4 w-4 text-green-600" />
                    <h3 className="text-lg font-bold text-green-800">專業領域與心理師偏好</h3>
                    <span className="text-sm text-gray-500 font-normal">(選填)</span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <Label htmlFor="specialty" className="font-semibold text-gray-700">專業領域</Label>
                      <Select
                        value={formData.specialty?.toString() || ""}
                        onValueChange={(value) => setFormData({ ...formData, specialty: value ? parseInt(value) : undefined })}
                      >
                      <SelectTrigger>
                        <SelectValue placeholder="選擇您需要的專業領域" />
                      </SelectTrigger>
                      <SelectContent>
                        {specialties.map(specialty => (
                          <SelectItem key={specialty.id} value={specialty.id.toString()}>
                            {specialty.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="therapist" className="font-semibold text-gray-700">指定心理師</Label>
                      <Select
                        value={formData.therapist?.toString() || ""}
                        onValueChange={(value) => setFormData({ ...formData, therapist: value ? parseInt(value) : undefined })}
                        disabled={!formData.specialty}
                      >
                        <SelectTrigger className={!formData.specialty ? "opacity-50 cursor-not-allowed" : ""}>
                          <SelectValue placeholder={
                            !formData.specialty 
                              ? "請先選擇專業領域"
                              : `從 ${specialties.find(s => s.id === formData.specialty)?.name} 專業的心理師中選擇`
                          }>
                            {formData.therapist && filteredTherapists.find(t => t.id === formData.therapist) && (
                              <span className="font-medium">
                                {filteredTherapists.find(t => t.id === formData.therapist)?.name}
                              </span>
                            )}
                          </SelectValue>
                        </SelectTrigger>
                        <SelectContent>
                          {filteredTherapists.map(therapist => (
                            <SelectItem key={therapist.id} value={therapist.id.toString()}>
                              <div className="flex flex-col">
                                <span className="font-medium">{therapist.name}</span>
                                <span className="text-xs text-gray-500">{therapist.title}</span>
                                <span className="text-xs text-blue-600">
                                  {(() => {
                                    const modes = Array.isArray(therapist.consultation_modes) 
                                      ? therapist.consultation_modes 
                                      : [];
                                    const hasOnline = modes.includes('online');
                                    const hasOffline = modes.includes('offline');
                                    
                                    if (hasOnline && hasOffline) return '線上/實體 ';
                                    if (hasOnline) return '線上 ';
                                    if (hasOffline) return '實體 ';
                                    return '未設定 ';
                                  })()}
                                  - NT$ {Math.min(...Object.values(therapist.pricing))}-{Math.max(...Object.values(therapist.pricing))}
                                </span>
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      {!formData.specialty && (
                        <p className="text-xs text-gray-500 mt-1">若要指定心理師，請先選擇專業領域</p>
                      )}
                      {formData.specialty && filteredTherapists.length === 0 && (
                        <p className="text-xs text-amber-600 mt-1">該專業領域目前無可預約的心理師</p>
                      )}
                    </div>
                  </div>
                </div>


                {/* 4. 偏好時間 */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-green-600" />
                    <h3 className="text-lg font-bold text-green-800">偏好時間</h3>
                  </div>
                  
                  {formData.preferred_periods?.map((period, index) => (
                    <div key={index} className="border rounded-lg p-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <Label className="text-sm font-bold text-gray-700">偏好時間 {index + 1}</Label>
                        {(formData.preferred_periods?.length || 0) > 1 && (
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={() => removePreferredPeriod(index)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                        <div>
                          <Label htmlFor={`date-${index}`} className="font-semibold text-gray-700">希望日期</Label>
                          <Input
                            id={`date-${index}`}
                            type="date"
                            value={period.date}
                            onChange={(e) => updatePreferredPeriod(index, 'date', e.target.value)}
                            min={new Date().toISOString().split('T')[0]}
                          />
                        </div>
                        <div>
                          <Label htmlFor={`period-${index}`} className="font-semibold text-gray-700">時段（可多選）</Label>
                          <div className="space-y-2 mt-2">
                            {(() => {
                              const timeSlots: Array<{
                                value: 'morning' | 'afternoon' | 'evening';
                                label: string;
                              }> = [
                                { value: 'morning', label: '上午 (09:00-12:00)' },
                                { value: 'afternoon', label: '下午 (13:00-17:00)' },
                                { value: 'evening', label: '晚上 (18:00-21:00)' }
                              ];
                              
                              return timeSlots.map(timeSlot => (
                                <div key={timeSlot.value} className="flex items-center space-x-2">
                                  <Checkbox
                                    id={`${timeSlot.value}-${index}`}
                                    checked={period.periods?.includes(timeSlot.value) || false}
                                    onCheckedChange={(checked) => {
                                      const currentPeriods = period.periods || []
                                      const newPeriods = checked
                                        ? [...currentPeriods, timeSlot.value]
                                        : currentPeriods.filter(p => p !== timeSlot.value)
                                      updatePreferredPeriod(index, 'periods', newPeriods)
                                    }}
                                  />
                                  <Label htmlFor={`${timeSlot.value}-${index}`} className="text-sm">
                                    {timeSlot.label}
                                  </Label>
                                </div>
                              ));
                            })()}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  <Button
                    type="button"
                    variant="outline"
                    onClick={addPreferredPeriod}
                    className="w-full"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    新增其他偏好時間
                  </Button>
                </div>

                {/* 6. 線上/實體選擇 */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-green-600" />
                    <h3 className="text-lg font-bold text-green-800">諮商方式</h3>
                  </div>
                  
                  <RadioGroup
                    value={formData.consultation_type}
                    onValueChange={(value: any) => setFormData({ ...formData, consultation_type: value })}
                    className="grid grid-cols-2 gap-3"
                  >
                    <div className="flex items-center space-x-2 border rounded-lg p-3">
                      <RadioGroupItem value="offline" id="offline" />
                      <Label htmlFor="offline" className="flex-1 cursor-pointer">
                        <div className="font-medium text-sm">實體諮商</div>
                        <div className="text-xs text-gray-500">面對面諮商服務</div>
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2 border rounded-lg p-3">
                      <RadioGroupItem value="online" id="online" />
                      <Label htmlFor="online" className="flex-1 cursor-pointer">
                        <div className="font-medium text-sm">線上諮商</div>
                        <div className="text-xs text-gray-500">視訊通話諮商服務</div>
                      </Label>
                    </div>
                  </RadioGroup>
                </div>

                {/* 7. 需求與注意事項 */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-4 w-4 text-green-600" />
                    <h3 className="text-lg font-bold text-green-800">需求與注意事項</h3>
                  </div>
                  
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                    <div>
                      <Label htmlFor="main_concerns" className="font-semibold text-gray-700">主要關注議題 <span className="text-red-500">*</span></Label>
                      <Textarea
                        id="main_concerns"
                        value={formData.main_concerns || ""}
                        onChange={(e) => setFormData({ ...formData, main_concerns: e.target.value })}
                        placeholder="請簡述您希望討論的議題或困擾..."
                        required
                        rows={2}
                        className="resize-none"
                      />
                    </div>

                    <div>
                      <Label htmlFor="special_needs" className="font-semibold text-gray-700">特殊需求或注意事項 <span className="text-gray-500 font-normal">(選填)</span></Label>
                      <Textarea
                        id="special_needs"
                        value={formData.special_needs || ""}
                        onChange={(e) => setFormData({ ...formData, special_needs: e.target.value })}
                        placeholder="如有特殊需求、身體限制或其他需要注意的事項，請告知我們..."
                        rows={2}
                        className="resize-none"
                      />
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="previous_therapy"
                      checked={formData.previous_therapy || false}
                      onCheckedChange={(checked) => setFormData({ ...formData, previous_therapy: checked as boolean })}
                    />
                    <Label htmlFor="previous_therapy" className="text-sm">
                      我曾經接受過心理諮商或治療
                    </Label>
                  </div>
                </div>

                <div className="pt-4 border-t">
                  <Button
                    type="submit"
                    className="w-full bg-green-600 hover:bg-green-700 text-white py-3 text-base"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        提交中...
                      </>
                    ) : (
                      "提交預約申請"
                    )}
                  </Button>
                  <p className="text-xs text-gray-500 text-center mt-2">
                    提交後，我們會透過Email與您聯繫確認預約時間
                  </p>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
