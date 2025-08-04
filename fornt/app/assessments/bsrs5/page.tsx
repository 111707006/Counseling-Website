"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, ArrowRight, CheckCircle, Loader2, AlertTriangle } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { 
  getAssessmentQuestions,
  submitAssessment,
  type AssessmentQuestion,
  type AssessmentResponseItem
} from "@/lib/api"

export default function BSRS5TestPage() {
  const router = useRouter()
  const { toast } = useToast()
  
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([])
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<number, number>>({})
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [testCompleted, setTestCompleted] = useState(false)
  const [result, setResult] = useState<any>(null)

  // 載入測驗題目
  useEffect(() => {
    const loadQuestions = async () => {
      try {
        const questionsData = await getAssessmentQuestions('BSRS5')
        setQuestions(questionsData)
      } catch (error) {
        console.error('載入題目失敗:', error)
        toast({
          title: "載入失敗",
          description: "無法載入測驗題目，請重新整理頁面",
          variant: "destructive",
        })
      } finally {
        setLoading(false)
      }
    }

    loadQuestions()
  }, [toast])

  // 選擇答案
  const selectAnswer = (questionId: number, choiceId: number) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: choiceId
    }))
  }

  // 下一題
  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1)
    }
  }

  // 上一題
  const previousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1)
    }
  }

  // 提交測驗
  const submitTest = async () => {
    if (Object.keys(answers).length < questions.length) {
      toast({
        title: "請完成所有題目",
        description: "請確保每一題都有選擇答案",
        variant: "destructive",
      })
      return
    }

    setSubmitting(true)
    try {
      const items: AssessmentResponseItem[] = Object.entries(answers).map(([questionId, choiceId]) => ({
        question: parseInt(questionId),
        choice: choiceId
      }))

      const result = await submitAssessment('BSRS5', { items })
      setResult(result)
      setTestCompleted(true)
      
      toast({
        title: "測驗完成",
        description: "您的測驗結果已生成",
      })
    } catch (error) {
      console.error('提交測驗失敗:', error)
      toast({
        title: "提交失敗",
        description: "測驗提交時發生錯誤，請稍後重試",
        variant: "destructive",
      })
    } finally {
      setSubmitting(false)
    }
  }

  // 獲取風險等級顏色和圖示
  const getRiskLevelStyle = (level: string) => {
    switch (level) {
      case '正常':
        return {
          color: 'text-green-600 bg-green-50 border-green-200',
          icon: '✅'
        }
      case '輕度':
        return {
          color: 'text-yellow-600 bg-yellow-50 border-yellow-200',
          icon: '⚠️'
        }
      case '中度':
        return {
          color: 'text-orange-600 bg-orange-50 border-orange-200',
          icon: '🚨'
        }
      case '重度':
        return {
          color: 'text-red-600 bg-red-50 border-red-200',
          icon: '🆘'
        }
      default:
        return {
          color: 'text-gray-600 bg-gray-50 border-gray-200',
          icon: 'ℹ️'
        }
    }
  }

  // 獲取建議文字
  const getRecommendation = (level: string, score: number) => {
    // 檢查是否有自殺意念風險（第6題）
    const suicideQuestion = questions.find(q => q.order === 6)
    const suicideAnswer = suicideQuestion ? answers[suicideQuestion.id] : 0
    const hasSuicideRisk = suicideAnswer && suicideAnswer >= 1

    if (hasSuicideRisk) {
      return "⚠️ 檢測到自殺意念風險，無論總分高低，強烈建議立即尋求專業心理師或精神科醫師的協助。"
    }

    switch (level) {
      case '正常':
        return "您的心理狀態良好！請繼續保持健康的生活方式和正向的心態。"
      case '輕度':
        return "您有輕度心理困擾，建議多與親友談談，適度抒發情緒，並注意休息與放鬆。"
      case '中度':
        return "您有中度心理困擾，建議尋求心理諮商或專業協助，以獲得更好的支持。"
      case '重度':
        return "您有重度心理困擾，需要高度關懷，強烈建議尋求精神科治療或專業心理治療。"
      default:
        return "感謝您完成測驗。"
    }
  }

  // 獲取分數解釋
  const getScoreInterpretation = (score: number) => {
    if (score <= 5) {
      return "身心適應狀況良好"
    } else if (score <= 9) {
      return "輕度情緒困擾"
    } else if (score <= 14) {
      return "中度情緒困擾"
    } else {
      return "重度情緒困擾"
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen py-8" style={{backgroundImage: 'url("/images/bg-texture.png")', backgroundSize: 'cover', backgroundPosition: 'center'}}>
        <div className="container mx-auto px-4 flex justify-center items-center min-h-[400px]">
          <div className="flex items-center space-x-2">
            <Loader2 className="h-6 w-6 animate-spin" />
            <span>載入測驗中...</span>
          </div>
        </div>
      </div>
    )
  }

  if (testCompleted && result) {
    const riskStyle = getRiskLevelStyle(result.risk_level)
    
    return (
      <div className="min-h-screen py-8" style={{backgroundImage: 'url("/images/bg-texture.png")', backgroundSize: 'cover', backgroundPosition: 'center'}}>
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <Card className="bg-white/95 backdrop-blur-sm shadow-xl">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <div className="text-2xl">{riskStyle.icon}</div>
                </div>
                <CardTitle className="text-2xl text-blue-800">BSRS-5 測驗結果</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                
                {/* 分數顯示 */}
                <div className="text-center">
                  <div className="text-4xl font-bold text-blue-800 mb-2">
                    {result.total_score}
                  </div>
                  <div className="text-gray-600">總分 (滿分 20)</div>
                  <div className="text-sm text-gray-500 mt-1">
                    {getScoreInterpretation(result.total_score)}
                  </div>
                </div>

                {/* 風險等級 */}
                <div className={`p-4 rounded-lg border ${riskStyle.color}`}>
                  <div className="flex items-center justify-center space-x-2 mb-2">
                    {(result.risk_level === '中度' || result.risk_level === '重度') && <AlertTriangle className="h-5 w-5" />}
                    <span className="font-semibold text-lg">{result.risk_level}心理困擾</span>
                  </div>
                  <p className="text-center text-sm">
                    {getRecommendation(result.risk_level, result.total_score)}
                  </p>
                </div>

                {/* 說明 */}
                <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-800 mb-2">關於 BSRS-5 量表</h4>
                  <div className="text-sm text-blue-700 space-y-1">
                    <p>• 0-5 分：正常心理反應（低壓狀態）</p>
                    <p>• 6-9 分：輕度心理困擾，建議觀察或諮詢</p>
                    <p>• ≥10 分：中重度心理困擾，建議尋求專業協助</p>
                    <p className="text-red-600 font-medium">• 第6題（自殺意念）≥1分：無論總分高低，建議進一步評估</p>
                  </div>
                </div>

                {/* 按鈕區域 */}
                <div className="flex flex-col space-y-4">
                  <Button
                    onClick={() => router.push('/appointments/book')}
                    className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 py-3 text-base font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
                  >
                    📅 預約心理諮商
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => router.push('/assessments')}
                    className="w-full border-2 border-blue-600 text-blue-600 hover:bg-blue-50 py-3 text-base font-semibold shadow-md hover:shadow-lg transition-all duration-300"
                  >
                    🔙 回到測驗選單
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen py-8" style={{backgroundImage: 'url("/images/bg-texture.png")', backgroundSize: 'cover', backgroundPosition: 'center'}}>
        <div className="container mx-auto px-4">
          <div className="text-center">
            <p>無法載入測驗題目</p>
            <Button onClick={() => router.push('/assessments')} className="mt-4">
              返回測驗列表
            </Button>
          </div>
        </div>
      </div>
    )
  }

  const currentQ = questions[currentQuestion]
  const progress = ((currentQuestion + 1) / questions.length) * 100
  const allAnswered = Object.keys(answers).length === questions.length
  const isLastQuestion = currentQuestion === questions.length - 1
  const isSuicideQuestion = currentQ?.order === 6

  return (
    <div className="min-h-screen py-8" style={{backgroundImage: 'url("/images/bg-texture.png")', backgroundSize: 'cover', backgroundPosition: 'center'}}>
      <div className="container mx-auto px-4">
        <div className="max-w-2xl mx-auto">
          
          {/* 進度條 */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-700">
                題目 {currentQuestion + 1} / {questions.length}
              </span>
              <span className="text-sm text-blue-600">
                {Math.round(progress)}% 完成
              </span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          <Card className="bg-white/95 backdrop-blur-sm shadow-xl">
            <CardHeader>
              <CardTitle className="text-xl text-blue-800 text-center">
                簡式健康量表（BSRS-5）
              </CardTitle>
              <p className="text-center text-gray-600 text-sm">
                {isSuicideQuestion 
                  ? "以下是附加題，請誠實作答"
                  : "請根據您最近一週的感受選擇最符合的選項"
                }
              </p>
              {isSuicideQuestion && (
                <div className="bg-red-50 border border-red-200 p-3 rounded-lg">
                  <p className="text-red-700 text-sm text-center font-medium">
                    ⚠️ 重要：此題目關於自殺意念，請誠實回答以獲得適當協助
                  </p>
                </div>
              )}
            </CardHeader>
            
            <CardContent className="space-y-6">
              
              {/* 題目 */}
              <div className="text-center">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  {currentQ.text}
                </h3>
              </div>

              {/* 選項 */}
              <RadioGroup
                value={answers[currentQ.id]?.toString() || ""}
                onValueChange={(value) => selectAnswer(currentQ.id, parseInt(value))}
                className="space-y-3"
              >
                {currentQ.choices.map((choice) => (
                  <Label 
                    key={choice.id}
                    htmlFor={choice.id.toString()}
                    className={`flex items-center space-x-3 p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                      answers[currentQ.id] === choice.id 
                        ? isSuicideQuestion && choice.score > 0
                          ? 'border-red-500 bg-red-50 shadow-md'
                          : 'border-blue-500 bg-blue-50 shadow-md'
                        : isSuicideQuestion && choice.score > 0 
                        ? 'border-red-200 hover:border-red-400 hover:bg-red-50 hover:shadow-sm'
                        : 'border-gray-200 hover:border-blue-400 hover:bg-blue-50 hover:shadow-sm'
                    }`}
                  >
                    <RadioGroupItem value={choice.id.toString()} id={choice.id.toString()} />
                    <span className="flex-1 font-medium text-gray-700 select-none">
                      {choice.text}
                    </span>
                  </Label>
                ))}
              </RadioGroup>

              {/* 導航按鈕 */}
              <div className="flex justify-between pt-4 border-t">
                <Button
                  variant="outline"
                  onClick={previousQuestion}
                  disabled={currentQuestion === 0}
                  className="flex items-center space-x-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  <span>上一題</span>
                </Button>

                {isLastQuestion ? (
                  <Button
                    onClick={submitTest}
                    disabled={!allAnswered || submitting}
                    className="bg-blue-600 hover:bg-blue-700 flex items-center space-x-2"
                  >
                    {submitting ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span>提交中...</span>
                      </>
                    ) : (
                      <>
                        <CheckCircle className="h-4 w-4" />
                        <span>提交測驗</span>
                      </>
                    )}
                  </Button>
                ) : (
                  <Button
                    onClick={nextQuestion}
                    disabled={!answers[currentQ.id]}
                    className="bg-blue-600 hover:bg-blue-700 flex items-center space-x-2"
                  >
                    <span>下一題</span>
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}