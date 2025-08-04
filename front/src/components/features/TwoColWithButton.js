import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import tw from "twin.macro"
import styled from "styled-components"
import {
  User,
  Briefcase,
  Heart,
  Users,
  HelpingHand,
  UserCheck,
  Brain,
  Globe,
  Baby,
  GraduationCap,
  AlertCircle,
  Settings,
} from "lucide-react"

import TeamIllustrationSrc from "../../images/team-illustration-2.svg"

// === 元件樣式 ===
const Container = tw.div`relative py-20 bg-orange-100`
const TwoColumn = tw.div`flex flex-col md:flex-row max-w-screen-xl mx-auto`
const Column = tw.div`w-full md:w-6/12`
const Image = tw.img`w-full`
const TextContent = tw.div`text-left md:pr-12`

const Heading = tw.h2`text-4xl font-bold text-orange-600 mb-4`
const Subheading = tw.p`text-sm text-orange-500 mb-2`
const Description = tw.p`text-gray-700 mb-6 text-sm leading-relaxed`

const Steps = tw.div`grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4`
const Step = styled.div(({ selected }) => [
  tw`p-4 border rounded-lg cursor-pointer transition-all duration-300`,
  selected ? tw`bg-orange-500 text-white shadow-lg` : tw`bg-white hover:shadow-md`
])
const StepIcon = styled.div(({ selected }) => [
  tw`mb-2 inline-block p-2 rounded-full`,
  selected ? tw`bg-white/20` : tw`bg-orange-200`
])
const StepTitle = styled.h4(({ selected }) => [
  tw`font-semibold mb-1 text-base`,
  selected ? tw`text-white` : tw`text-orange-900`
])
const StepDescription = styled.p(({ selected }) => [
  tw`text-xs`,
  selected ? tw`text-white/80` : tw`text-orange-600`
])

const Button = tw.button`mt-4 px-6 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-full font-medium`
const Notice = tw.div`mt-8 p-4 bg-orange-200 border border-orange-300 rounded-lg`
const NoticeText = tw.p`text-sm text-orange-800`

// === 分類資料 ===
const categories = [
  { id: "general", title: "不分類", description: "全部治療師列表", icon: User },
  { id: "workplace", title: "職場問題", description: "所有跟工作有關的", icon: Briefcase },
  { id: "relationship", title: "感情問題", description: "跟感情有關的", icon: Heart },
  { id: "family", title: "家庭問題", description: "父母兄弟姊妹配偶子女", icon: Users },
  { id: "life-meaning", title: "生命意義", description: "人生價值與方向", icon: HelpingHand },
  { id: "sex-counseling", title: "性諮商", description: "性相關議題與諮詢", icon: UserCheck },
  { id: "biofeedback", title: "生理回饋", description: "改善焦慮、放鬆練習", icon: Brain },
  { id: "multicultural", title: "多元文化", description: "跨文化適應與伴侶關係", icon: Globe },
  { id: "children", title: "兒童", description: "12歲以下", icon: Baby },
  { id: "adolescent", title: "青少年", description: "12–18歲", icon: GraduationCap },
  { id: "special-situations", title: "特殊狀況", description: "創傷、自傷、自殺、安寧", icon: AlertCircle },
  { id: "general-adult", title: "一般成人", description: "職涯、壓力、失眠等", icon: Settings },
]

// === 主組件 ===
const TherapistCategories = () => {
  const navigate = useNavigate()
  const [selectedCategory, setSelectedCategory] = useState("general")

  const handleSelect = (id) => {
    setSelectedCategory(id)
    navigate(`/therapists/${id}`)
  }

  return (
    <Container>
      <TwoColumn>
        <Column>
          <TextContent>
            <Subheading>張老師基金會台北分事務所</Subheading>
            <Heading>快速媒合心理師</Heading>
            <Description>
              每個人都有感到辛苦的時候，無論你正經歷什麼，都值得被理解與支持。
              請從右方選擇你最想談的方向，我們將陪你一起找尋適合的心理師。
            </Description>
            <Button onClick={() => alert("跳轉預約表單")}>填寫預約表單</Button>
          </TextContent>
        </Column>
        <Column>
          <Steps>
            {categories.map(({ id, title, description, icon: Icon }) => (
              <Step key={id} selected={selectedCategory === id} onClick={() => handleSelect(id)}>
                <StepIcon selected={selectedCategory === id}>
                  <Icon size={20} />
                </StepIcon>
                <StepTitle selected={selectedCategory === id}>{title}</StepTitle>
                <StepDescription selected={selectedCategory === id}>{description}</StepDescription>
              </Step>
            ))}
          </Steps>
        </Column>
      </TwoColumn>

      <Notice>
        <NoticeText>ℹ️ 僅顯示三週內可預約的新案心理師。</NoticeText>
      </Notice>
    </Container>
  )
}

export default TherapistCategories
