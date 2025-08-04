"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"

interface AssessmentTest {
  code: string
  name: string
  description: string
  question_count: number
}

export default function AssessmentsPage() {
  const [tests, setTests] = useState<AssessmentTest[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTests()
  }, [])

  const fetchTests = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/assessments/tests/")
      if (response.ok) {
        const data = await response.json()
        // Add question_count to each test (since backend doesn't provide it)
        const testsWithCount = data.map((test: any) => ({
          ...test,
          question_count: 5 // Default to 5 questions
        }))
        setTests(testsWithCount)
      } else {
        // If API is not available, use mock data
        setTests([
          {
            code: "WHO5",
            name: "WHO-5 幸福感量表",
            description: "請回想過去兩週的情況，評估您的整體幸福感和心理健康狀況",
            question_count: 5,
          },
          {
            code: "BSRS5",
            name: "簡式健康量表（BSRS-5）",
            description: "評估最近一週的心理困擾程度，包含焦慮、憂鬱、敵意、人際敏感、失眠等面向。",
            question_count: 6,
          }
        ])
      }
    } catch (error) {
      console.error("API not available, using mock data:", error)
      // Use mock data when API is not available
      setTests([
        {
          code: "WHO5",
          name: "WHO-5 幸福感量表",
          description: "請回想過去兩週的情況，評估您的整體幸福感和心理健康狀況",
          question_count: 5,
        },
        {
          code: "BSRS5",
          name: "簡式健康量表（BSRS-5）",
          description: "評估最近一週的心理困擾程度，包含焦慮、憂鬱、敵意、人際敏感、失眠等面向。",
          question_count: 6,
        }
      ])
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

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-green-800 mb-4">專業心理測驗</h1>
          <p className="text-xl text-green-600 mb-8">透過專業的心理測驗，更了解自己的心理狀態</p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Introduction */}
          <Card className="bg-white/90 backdrop-blur-sm mb-8">
            <CardContent className="p-8">
              <h2 className="text-2xl font-bold text-green-800 mb-4">關於心理測驗</h2>
              <div className="space-y-4 text-gray-700">
                <p>
                  心理測驗是了解自己心理狀態的有效工具。我們提供經過專業驗證的測驗量表， 幫助您評估自己的心理健康狀況。
                </p>
                <p>
                  請注意：這些測驗結果僅供參考，不能替代專業的心理諮商或醫療診斷。
                  如果您對結果有疑慮，建議尋求專業心理師的協助。
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Available Tests */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
            {tests.map((test) => (
              <Card key={test.code} className="bg-white/95 backdrop-blur-sm hover:shadow-xl transition-all duration-300 border-0 shadow-lg group">
                <CardHeader className="text-center pb-4">
                  <div className={`w-24 h-24 rounded-full mx-auto mb-6 flex items-center justify-center transition-transform duration-300 group-hover:scale-110 ${
                    test.code === 'WHO5' ? 'bg-gradient-to-br from-amber-100 to-amber-200' : test.code === 'BSRS5' ? 'bg-gradient-to-br from-blue-100 to-blue-200' : 'bg-gradient-to-br from-green-100 to-green-200'
                  }`}>
                    <div className="text-4xl">
                      {test.code === 'WHO5' ? '😊' : test.code === 'BSRS5' ? '🧠' : '🔍'}
                    </div>
                  </div>
                  <CardTitle className="text-2xl text-green-800 mb-3 leading-tight">{test.name}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6 pt-0">
                  <p className="text-gray-600 text-center leading-relaxed">{test.description}</p>
                  
                  <div className={`grid grid-cols-1 gap-3 p-4 rounded-lg ${
                    test.code === 'WHO5' ? 'bg-amber-50' : test.code === 'BSRS5' ? 'bg-blue-50' : 'bg-green-50'
                  }`}>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 font-medium">⏱️ 測驗時間</span>
                      <span className="text-gray-800 font-semibold">約 2-5 分鐘</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 font-medium">📝 題目數量</span>
                      <span className="text-gray-800 font-semibold">{test.question_count} 題</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 font-medium">🎯 評估範圍</span>
                      <span className="text-gray-800 font-semibold">
                        {test.code === 'WHO5' ? '整體幸福感' : test.code === 'BSRS5' ? '心理困擾程度' : '壓力與情緒狀態'}
                      </span>
                    </div>
                  </div>
                  
                  <Link href={`/assessments/${test.code.toLowerCase()}`} className="block">
                    <Button className={`w-full text-white font-semibold py-3 text-base shadow-lg hover:shadow-xl transition-all duration-300 ${
                      test.code === 'WHO5' 
                        ? 'bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700' 
                        : test.code === 'BSRS5'
                        ? 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800'
                        : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
                    }`}>
                      🚀 開始測驗
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
            
            {/* 如果沒有測驗，顯示提示 */}
            {tests.length === 0 && (
              <div className="col-span-2 text-center py-8">
                <p className="text-gray-600">目前沒有可用的測驗</p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}
