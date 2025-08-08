"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/hooks/use-toast"

// 使用與後端匹配的AppointmentResponse介面
import { AppointmentResponse, queryAppointments } from "@/lib/api"

export default function QueryAppointmentPage() {
  const [queryData, setQueryData] = useState({
    email: "",
    id_number: "",
  })
  const [appointments, setAppointments] = useState<AppointmentResponse[]>([])
  const [isQuerying, setIsQuerying] = useState(false)
  const { toast } = useToast()

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsQuerying(true)

    try {
      console.log('查詢資料:', queryData)
      const result = await queryAppointments(queryData.email, queryData.id_number)
      console.log('查詢結果:', result)
      setAppointments(result)
      if (result.length === 0) {
        toast({
          title: "查無預約紀錄",
          description: "請確認您的電子郵件和身分證字號是否正確。",
        })
      }
    } catch (error) {
      toast({
        title: "查詢失敗",
        description: "請檢查您的資料並重試。",
        variant: "destructive",
      })
    } finally {
      setIsQuerying(false)
    }
  }

  const handleCancel = async (appointmentId: number) => {
    try {
      // 使用新的取消預約API，需要提供驗證資料
      const response = await fetch(`/api/appointments/${appointmentId}/cancel/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: queryData.email,        // 使用查詢時的email
          id_number: queryData.id_number // 使用查詢時的身分證號
        }),
      })

      if (response.ok) {
        // 更新預約狀態為cancelled，而不是從列表中移除
        setAppointments(appointments.map(apt => 
          apt.id === appointmentId 
            ? { ...apt, status: 'cancelled', status_display: '已取消' }
            : apt
        ))
        toast({
          title: "取消成功",
          description: "您的預約已成功取消。",
        })
      } else {
        const errorData = await response.json()
        throw new Error(errorData.error || "取消失敗")
      }
    } catch (error) {
      toast({
        title: "取消失敗",
        description: error instanceof Error ? error.message : "無法取消預約，請聯繫客服。",
        variant: "destructive",
      })
    }
  }

  const getStatusBadge = (status: string, status_display?: string) => {
    const statusMap = {
      pending: { label: "待確認", variant: "secondary" as const },
      confirmed: { label: "已確認", variant: "default" as const },
      completed: { label: "已完成", variant: "outline" as const },
      cancelled: { label: "已取消", variant: "destructive" as const },
      rejected: { label: "已拒絕", variant: "destructive" as const },
    }
    const statusInfo = statusMap[status as keyof typeof statusMap] || { 
      label: status_display || status, 
      variant: "secondary" as const 
    }
    return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>
  }

  return (
    <div className="min-h-screen py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-white/90 backdrop-blur-sm mb-8">
            <CardHeader className="text-center">
              <CardTitle className="text-3xl text-brand-text">查詢預約紀錄</CardTitle>
              <p className="text-brand-text/70 mt-2">請輸入您的電子郵件和身分證字號查詢預約狀況</p>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleQuery} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="email">電子郵件 *</Label>
                    <Input
                      id="email"
                      type="email"
                      value={queryData.email}
                      onChange={(e) => setQueryData({ ...queryData, email: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="id_number">身分證字號 *</Label>
                    <Input
                      id="id_number"
                      value={queryData.id_number}
                      onChange={(e) => setQueryData({ ...queryData, id_number: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <Button
                  type="submit"
                  className="w-full bg-brand-button hover:bg-brand-button/80 text-white"
                  disabled={isQuerying}
                >
                  {isQuerying ? "查詢中..." : "查詢預約"}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Appointments List */}
          {appointments.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-brand-text mb-4">您的預約紀錄</h2>
              {appointments.map((appointment) => (
                <Card key={appointment.id} className="bg-white/90 backdrop-blur-sm">
                  <CardContent className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <p className="text-brand-text/70">心理師：{appointment.therapist}</p>
                        {appointment.detail?.name && (
                          <p className="text-sm text-gray-600">申請人：{appointment.detail.name}</p>
                        )}
                      </div>
                      {getStatusBadge(appointment.status, appointment.status_display)}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-gray-600">諮商方式</p>
                        <p className="font-medium">{appointment.consultation_type_display}</p>
                      </div>
                      
                      {appointment.confirmed_datetime ? (
                        <div>
                          <p className="text-sm text-gray-600">確認時間</p>
                          <p className="font-medium text-brand-text">
                            {new Date(appointment.confirmed_datetime).toLocaleString("zh-TW", {
                              year: 'numeric',
                              month: '2-digit',
                              day: '2-digit',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                        </div>
                      ) : (
                        <div>
                          <p className="text-sm text-gray-600">偏好時間</p>
                          <div className="space-y-1">
                            {appointment.preferred_periods.length > 0 ? (
                              appointment.preferred_periods.map((period, index) => (
                                <p key={index} className="font-medium text-sm">
                                  {period.date} {period.period_display}
                                </p>
                              ))
                            ) : (
                              <p className="font-medium">未指定</p>
                            )}
                          </div>
                        </div>
                      )}
                      
                      {appointment.detail?.urgency && (
                        <div>
                          <p className="text-sm text-gray-600">緊急程度</p>
                          <p className="font-medium">
                            {appointment.detail.urgency === 'high' ? '高' : 
                             appointment.detail.urgency === 'medium' ? '中' : '低'}
                          </p>
                        </div>
                      )}
                    </div>

                    {appointment.detail?.main_concerns && (
                      <div className="mb-4">
                        <p className="text-sm text-gray-600">主要關注議題</p>
                        <p className="font-medium text-sm bg-gray-50 p-2 rounded">
                          {appointment.detail.main_concerns}
                        </p>
                      </div>
                    )}

                    {appointment.detail?.special_needs && (
                      <div className="mb-4">
                        <p className="text-sm text-gray-600">特殊需求</p>
                        <p className="font-medium text-sm bg-gray-50 p-2 rounded">
                          {appointment.detail.special_needs}
                        </p>
                      </div>
                    )}

                    <div className="flex justify-between items-center">
                      <p className="text-sm text-gray-500">
                        申請時間：{new Date(appointment.created_at).toLocaleString("zh-TW")}
                      </p>
                      {appointment.status === "pending" && (
                        <Button variant="destructive" size="sm" onClick={() => handleCancel(appointment.id)}>
                          取消預約
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
