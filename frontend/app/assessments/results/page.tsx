"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Calendar, TrendingUp, TrendingDown, Minus, AlertTriangle } from "lucide-react"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"
import { getAssessmentResults, type AssessmentResult } from "@/lib/api"

export default function AssessmentResultsPage() {
  const router = useRouter()
  const { toast } = useToast()
  
  const [results, setResults] = useState<AssessmentResult[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'WHO5' | 'BSRS5'>('all')

  useEffect(() => {
    loadResults()
  }, [])

  const loadResults = async () => {
    try {
      const data = await getAssessmentResults()
      setResults(data)
    } catch (error) {
      console.error('載入結果失敗:', error)
      toast({
        title: "載入失敗",
        description: "無法載入測驗結果，請重新整理頁面",
        variant: "destructive",
      })
      // 使用模擬數據進行演示
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const filteredResults = filter === 'all' 
    ? results 
    : results.filter(result => result.test === filter)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getRiskLevelBadge = (level: string, testType: string) => {
    if (testType === 'WHO5') {
      switch (level) {
        case '良好':
          return <Badge className="bg-green-100 text-green-800 border-green-200">良好</Badge>
        case '中度關注':
          return <Badge className="bg-yellow-100 text-yellow-800 border-yellow-200">中度關注</Badge>
        case '需要關注':
          return <Badge className="bg-red-100 text-red-800 border-red-200">需要關注</Badge>
        default:
          return <Badge variant="secondary">{level}</Badge>
      }
    } else {
      // BSRS5
      switch (level) {
        case '正常':
          return <Badge className="bg-green-100 text-green-800 border-green-200">正常</Badge>
        case '輕度':
          return <Badge className="bg-yellow-100 text-yellow-800 border-yellow-200">輕度困擾</Badge>
        case '中度':
          return <Badge className="bg-orange-100 text-orange-800 border-orange-200">中度困擾</Badge>
        case '重度':
          return <Badge className="bg-red-100 text-red-800 border-red-200">重度困擾</Badge>
        default:
          return <Badge variant="secondary">{level}</Badge>
      }
    }
  }

  const getScoreTrend = (currentResult: AssessmentResult, index: number) => {
    if (index === filteredResults.length - 1) return null
    
    const sameTestResults = filteredResults.filter(r => r.test === currentResult.test)
    const currentIndex = sameTestResults.findIndex(r => r.id === currentResult.id)
    
    if (currentIndex === sameTestResults.length - 1) return null
    
    const previousResult = sameTestResults[currentIndex + 1]
    const scoreDiff = currentResult.total_score - previousResult.total_score
    
    if (scoreDiff > 0) {
      return (
        <div className="flex items-center text-red-600 text-sm">
          <TrendingUp className="h-4 w-4 mr-1" />
          <span>+{scoreDiff}</span>
        </div>
      )
    } else if (scoreDiff < 0) {
      return (
        <div className="flex items-center text-green-600 text-sm">
          <TrendingDown className="h-4 w-4 mr-1" />
          <span>{scoreDiff}</span>
        </div>
      )
    } else {
      return (
        <div className="flex items-center text-gray-600 text-sm">
          <Minus className="h-4 w-4 mr-1" />
          <span>0</span>
        </div>
      )
    }
  }

  const getTestName = (testCode: string) => {
    switch (testCode) {
      case 'WHO5':
        return 'WHO-5 幸福感量表'
      case 'BSRS5':
        return '簡式健康量表（BSRS-5）'
      default:
        return testCode
    }
  }

  const getMaxScore = (testCode: string) => {
    return testCode === 'WHO5' ? 100 : 20
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
        <div className="container mx-auto px-4 flex justify-center items-center min-h-[400px]">
          <div>載入中...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-amber-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          
          {/* 標題區域 */}
          <div className="flex items-center mb-8">
            <Button
              variant="ghost"
              onClick={() => router.push('/assessments')}
              className="mr-4 p-2"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-green-800">測驗結果歷史</h1>
              <p className="text-green-600 mt-2">追蹤您的心理健康狀況變化</p>
            </div>
          </div>

          {/* 篩選器 */}
          <Card className="bg-white/95 backdrop-blur-sm mb-6 shadow-lg border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-center">
                <div className="flex flex-wrap gap-3 justify-center">
                  <Button
                    variant={filter === 'all' ? 'default' : 'outline'}
                    onClick={() => setFilter('all')}
                    className={`px-6 py-2 font-semibold transition-all duration-300 ${
                      filter === 'all' 
                        ? 'bg-green-600 hover:bg-green-700 shadow-lg' 
                        : 'border-2 hover:border-green-400 hover:bg-green-50'
                    }`}
                  >
                    📊 全部測驗
                  </Button>
                  <Button
                    variant={filter === 'WHO5' ? 'default' : 'outline'}
                    onClick={() => setFilter('WHO5')}
                    className={`px-6 py-2 font-semibold transition-all duration-300 ${
                      filter === 'WHO5' 
                        ? 'bg-amber-500 hover:bg-amber-600 shadow-lg' 
                        : 'border-2 hover:border-amber-400 hover:bg-amber-50'
                    }`}
                  >
                    😊 WHO-5
                  </Button>
                  <Button
                    variant={filter === 'BSRS5' ? 'default' : 'outline'}
                    onClick={() => setFilter('BSRS5')}
                    className={`px-6 py-2 font-semibold transition-all duration-300 ${
                      filter === 'BSRS5' 
                        ? 'bg-blue-500 hover:bg-blue-600 shadow-lg' 
                        : 'border-2 hover:border-blue-400 hover:bg-blue-50'
                    }`}
                  >
                    🧠 BSRS-5
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 結果列表 */}
          {filteredResults.length === 0 ? (
            <Card className="bg-white/95 backdrop-blur-sm shadow-lg border-0">
              <CardContent className="p-12 text-center">
                <div className="text-gray-500 mb-8">
                  <div className="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full mx-auto mb-6 flex items-center justify-center">
                    <Calendar className="h-12 w-12 text-gray-400" />
                  </div>
                  <p className="text-xl font-semibold text-gray-700 mb-2">尚無測驗記錄</p>
                  <p className="text-gray-500 max-w-sm mx-auto leading-relaxed">
                    完成測驗後，結果會顯示在這裡，您可以追蹤自己的心理健康狀況變化
                  </p>
                </div>
                <Button
                  onClick={() => router.push('/assessments')}
                  className="bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 px-8 py-3 text-base font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  🚀 開始測驗
                </Button>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-6">
              {filteredResults.map((result, index) => (
                <Card key={result.id} className="bg-white/95 backdrop-blur-sm hover:shadow-xl transition-all duration-300 border-0 shadow-lg group">
                  <CardContent className="p-8">
                    <div className="flex items-center justify-between">
                      
                      {/* 測驗資訊 */}
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="font-semibold text-lg text-gray-800">
                            {getTestName(result.test)}
                          </h3>
                          {getRiskLevelBadge(result.risk_level, result.test)}
                        </div>
                        
                        <div className="flex items-center text-sm text-gray-600 space-x-4">
                          <div className="flex items-center">
                            <Calendar className="h-4 w-4 mr-1" />
                            <span>{formatDate(result.created_at)}</span>
                          </div>
                          {/* 檢查是否有自殺意念風險 */}
                          {result.test === 'BSRS5' && result.items.some(item => 
                            result.items.length >= 6 && 
                            result.items[5] && 
                            result.items[5].score >= 1
                          ) && (
                            <div className="flex items-center text-red-600">
                              <AlertTriangle className="h-4 w-4 mr-1" />
                              <span className="text-xs font-medium">自殺意念風險</span>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* 分數與趨勢 */}
                      <div className="text-right">
                        <div className="flex items-center space-x-2">
                          <div className="text-right">
                            <div className="text-2xl font-bold text-gray-800">
                              {result.total_score}
                            </div>
                            <div className="text-sm text-gray-500">
                              / {getMaxScore(result.test)}
                            </div>
                          </div>
                          {getScoreTrend(result, index)}
                        </div>
                      </div>
                    </div>

                    {/* 進度條 */}
                    <div className="mt-4">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            result.test === 'WHO5'
                              ? result.total_score >= 50
                                ? 'bg-green-500'
                                : result.total_score >= 29
                                ? 'bg-yellow-500'
                                : 'bg-red-500'
                              : result.total_score <= 5
                              ? 'bg-green-500'
                              : result.total_score <= 9
                              ? 'bg-yellow-500'
                              : 'bg-red-500'
                          }`}
                          style={{
                            width: `${(result.total_score / getMaxScore(result.test)) * 100}%`
                          }}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* 底部說明 */}
          {filteredResults.length > 0 && (
            <Card className="bg-white/95 backdrop-blur-sm mt-8 shadow-lg border-0">
              <CardContent className="p-8">
                <div className="text-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <div className="text-2xl">💡</div>
                  </div>
                  <h4 className="text-xl font-bold text-gray-800 mb-2">如何解讀結果趨勢</h4>
                  <p className="text-gray-600">了解您的測驗結果變化，更好地掌握心理健康狀況</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="bg-amber-50 p-6 rounded-lg border border-amber-200">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 bg-amber-100 rounded-full flex items-center justify-center mr-3">
                        <span className="text-lg">😊</span>
                      </div>
                      <h5 className="font-bold text-amber-800">WHO-5 幸福感量表</h5>
                    </div>
                    <ul className="space-y-2 text-sm text-amber-700">
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">📈</span>
                        <span>分數上升：幸福感改善</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-red-600 mr-2">📉</span>
                        <span>分數下降：需要關注情緒狀態</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-blue-600 mr-2">⏰</span>
                        <span>建議每2-4週測驗一次</span>
                      </li>
                    </ul>
                  </div>
                  
                  <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                        <span className="text-lg">🧠</span>
                      </div>
                      <h5 className="font-bold text-blue-800">BSRS-5 簡式健康量表</h5>
                    </div>
                    <ul className="space-y-2 text-sm text-blue-700">
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">📉</span>
                        <span>分數下降：心理困擾減少</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-red-600 mr-2">📈</span>
                        <span>分數上升：壓力可能增加</span>
                      </li>
                      <li className="flex items-start">
                        <span className="text-blue-600 mr-2">⏰</span>
                        <span>建議每週測驗以監控狀態</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}