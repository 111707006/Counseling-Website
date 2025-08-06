'use client'
import Link from "next/link"
import Image from "next/image"
import { useState } from "react"

export default function HomePage() {
  const images = [
    { src: "/images/唔談室2.JPG", alt: "唔談室環境2" },
    { src: "/images/唔談室3.JPG", alt: "唔談室環境3" },
    { src: "/images/唔談室4.JPG", alt: "唔談室環境4" },
    { src: "/images/唔談室5.JPG", alt: "唔談室環境5" },
    { src: "/images/唔談室6.JPG", alt: "唔談室環境6" }
  ]
  
  const [currentIndex, setCurrentIndex] = useState(0)
  const imagesPerView = 4
  
  const nextSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex + imagesPerView >= images.length ? 0 : prevIndex + 1
    )
  }
  
  const prevSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === 0 ? Math.max(0, images.length - imagesPerView) : prevIndex - 1
    )
  }
  
  const visibleImages = images.slice(currentIndex, currentIndex + imagesPerView)
  // 如果不足4張，從頭補齊
  if (visibleImages.length < imagesPerView) {
    const remaining = imagesPerView - visibleImages.length
    visibleImages.push(...images.slice(0, remaining))
  }

  return (
    <div className="min-h-screen">

      {/* Main Image with Clickable Areas */}
      <section
        className="relative bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('/images/網頁設計.png')", // ✅ 請放在 public/images/ 裡
      }}
    >

        <div className="relative max-w-4xl mx-auto">
          {/* Title Text Overlay */}
          <div className="absolute top-[8%] left-1/2 transform -translate-x-1/2 text-center">
            <h1
              className="font-bold mb-2"
              style={{
                fontSize: 'calc(2rem + 5px)', // 3xl 約2rem，+5px
                color: '#000',
                textShadow: "2px 2px 4px rgba(0,0,0,0.1)",
                position: 'relative',
                top: '5px',
                left: '15px',
              }}
            >
              張老師台北心理諮商所
            </h1>
          </div>

          {/* Subtitle Text */}
          <div className="absolute top-[15%] left-1/2 transform -translate-x-1/2 text-center">
            <p
              className="text-lg md:text-xl mb-1"
              style={{
                color: '#000',
                textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
              }}
            >
              心理諮商是一次與自己的語言整理
            </p>
            <p
              className="text-base md:text-lg"
              style={{
                color: '#000',
                textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
              }}
            >
              找出自己真正的聲音...
            </p>
          </div>

          {/* Additional descriptive text overlays */}
          <div
            className="absolute top-[26%] right-[30%] text-sm max-w-xs text-center"
            style={{
              color: '#000',
              textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
            }}
          >
            <p>從一通電話開始，張老師開啟了陪伴的旅程。</p>
            <p>台北諮商所秉持著關懷、專業與經驗的初心，</p>
            <p>期盼在您需要的時刻，成為那個陪伴您任您的人。</p>
          </div>
          <div
            className="absolute top-[38%] right-[15%] max-w-xs text-center"
            style={{
              color: '#000',
              fontSize: '1.2rem',
              textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
            }}
          >
            心理諮商是一次與自己的語言整理
          </div>
          <div
            className="absolute top-[44%] right-[26%]  max-w-xs text-center"
            style={{
              textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
            }}
          >
            
            <p className="mb-2">所內聚集了專業且擁有豐富經驗的心理師，</p>
            <p className="mb-2">無論您面臨什麼樣的困擾或需求，</p>
            <p className="mb-2">我們都會成為您堅實的支持與幫助。</p>
            <p>能成為您堅實的支持與幫助。</p>
          </div>

          <div
            className="absolute top-[62%] left-[35%]  max-w-xs text-center"
            style={{
              fontSize: '1.1rem',
              textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
            }}
          >
            <p className="mb-1">心理測驗，是一次與自己對話的起點。</p>
            <p>在這裡，慢慢找到屬於你的聲音與步調...</p>
          </div>

          <div className="absolute bottom-[8%] left-1/2 transform -translate-x-1/2 text-center">
            <p
              className="text-lg "
              style={{
                textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
              }}
            >
              心理諮商是一次與自己的語言整理
            </p>
            <p
              className="text-lg  mt-1"
              style={{
                textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
              }}
            >
              找出自己真正的聲音...
            </p>
          </div>
          <Image
            src="/images/clean-hero-design.png"
            alt="張老師台北心理諮商所服務介紹"
            width={1200}
            height={1600}
            className="w-full h-auto"
            priority
          />

          {/* Social Media Icons - Right Side */}
          <div className="fixed top-[20%] right-4 flex flex-col space-y-4 z-50">
            {/* Instagram */}
            <a
              href="https://www.instagram.com/psytp1980/"
              target="_blank"
              rel="noopener noreferrer"
              className="group"
            >
              <div className="w-12 h-12 bg-white/90 hover:bg-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group-hover:scale-110">
                <svg className="w-6 h-6 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </div>
            </a>

            {/* Facebook */}
            <a
              href="https://www.facebook.com/profile.php?id=61577644183952"
              target="_blank"
              rel="noopener noreferrer"
              className="group"
            >
              <div className="w-12 h-12 bg-white/90 hover:bg-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group-hover:scale-110">
                <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </div>
            </a>

            {/* LINE */}
            <a
              href="https://line.me/"
              target="_blank"
              rel="noopener noreferrer"
              className="group"
            >
              <div className="w-12 h-12 bg-white/90 hover:bg-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group-hover:scale-110">
                <svg className="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.627-.63h2.386c.349 0 .63.285.63.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.627-.63.349 0 .631.285.631.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314"/>
                </svg>
              </div>
            </a>

            {/* Threads */}
            <a
              href="https://www.threads.com/@psytp1980?xmt=AQF0ikYP-sDp6-xuLfBOt3K9XFhlbOh9zf-lmFC5f6YiUw"
              target="_blank"
              rel="noopener noreferrer"
              className="group"
            >
              <div className="w-12 h-12 bg-white/90 hover:bg-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group-hover:scale-110">
                <svg className="w-6 h-6 text-black" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-.584-2.043-1.496-3.467-2.711-4.231-1.33-1.025-3.058-1.563-5.143-1.563-.014 0-.027 0-.041.001-2.472.021-4.41.895-5.76 2.6C5.645 6.094 4.97 8.459 4.952 11.39c.018 2.931.693 5.295 2.005 7.037 1.35 1.704 3.288 2.578 5.76 2.6.014 0 .027 0 .041.001 2.085 0 3.813-.538 5.143-1.563 1.215-.764 2.127-2.188 2.711-4.231l2.04.569c-.651 2.337-1.832 4.177-3.509 5.467C17.225 23.275 14.928 23.98 12.186 24zM12 7.378c-2.552 0-4.622 2.07-4.622 4.622S9.448 16.622 12 16.622s4.622-2.07 4.622-4.622S14.552 7.378 12 7.378zm0 6.891c-1.252 0-2.269-1.017-2.269-2.269S10.748 9.731 12 9.731s2.269 1.017 2.269 2.269-1.017 2.269-2.269 2.269z"/>
                </svg>
              </div>
            </a>
          </div>

          {/* Clickable Hotspots */}
         
          {/* === [按鈕熱區] 立即預約（右上角人物） === */}
          <Link href="/appointments/book">
            <div className="absolute top-[19%] left-[70%] w-[25%] h-[15%] hover:bg-green-200/20 transition-colors duration-300 rounded-lg cursor-pointer group">
              <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-green-800/90 text-white p-2 rounded-lg text-center absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 whitespace-nowrap">
                點擊預約諮詢
              </div>
            </div>
          </Link>

          {/* 心理健康文章 - 左中人物 */}
          <Link href="/articles">
            <div className="absolute top-[35%] left-[8%] w-[22%] h-[18%] hover:bg-amber-200/20 transition-colors duration-300 rounded-lg cursor-pointer group">
              <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-amber-800/90 text-white p-2 rounded-lg text-center absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 whitespace-nowrap">
                瀏覽健康文章
              </div>
            </div>
          </Link>

          {/* 心理師介紹 - 左下人物 */}
          <Link href="/therapists">
            <div className="absolute top-[40%] left-[73%] w-[25%] h-[20%] hover:bg-amber-200/20 transition-colors duration-300 rounded-lg cursor-pointer group">
              <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-amber-800/90 text-white p-2 rounded-lg text-center absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 whitespace-nowrap">
                認識心理師團隊
              </div>
            </div>
          </Link>

          {/* 專業心理測驗 - 右下人物 */}
          <Link href="/assessments">
            <div className="absolute top-[52%] right-[70%] w-[25%] h-[18%] hover:bg-green-200/20 transition-colors duration-300 rounded-lg cursor-pointer group">
              <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-green-800/90 text-white p-2 rounded-lg text-center absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 whitespace-nowrap">
                開始心理測驗
              </div>
            </div>
          </Link>

          {/* 預約諮詢按鈕熱區 */}
          <Link href="/appointments/book">
            <div className="absolute top-[27%] left-[12%] w-[18%] h-[5%] hover:bg-amber-300/30 transition-colors duration-300 rounded-full cursor-pointer group">
             
            </div>
          </Link>

          {/* 心理健康文章按鈕熱區 */}
          <Link href="/articles">
            <div className="absolute top-[37%] left-[30%] w-[20%] h-[4%] hover:bg-amber-300/30 transition-colors duration-300 rounded-full cursor-pointer group">
              
            </div>
          </Link>

          {/* 心理師介紹按鈕熱區 */}
          <Link href="/therapists">
            <div className="absolute top-[53.5%] left-[47%] w-[21%] h-[4%] hover:bg-amber-300/30 transition-colors duration-300 rounded-full cursor-pointer group">
              
            </div>
          </Link>

          {/* 專業心理測驗按鈕熱區 */}
          <Link href="/assessments">
            <div className="absolute top-[69%] left-[39%] w-[20%] h-[4%] hover:bg-amber-300/30 transition-colors duration-300 rounded-full cursor-pointer group">
              
            </div>
          </Link>
        </div>

        {/* Mobile Navigation Cards - 只在小螢幕顯示 */}
        <div className="md:hidden mt-8 grid grid-cols-2 gap-4">
          <Link
            href="/appointments/book"
            className="bg-amber-200 hover:bg-amber-300 p-4 rounded-lg text-center transition-colors"
          >
            <div className="text-2xl mb-2">📞</div>
            <div className="text-amber-800 font-semibold">預約諮詢</div>
          </Link>
          <Link
            href="/articles"
            className="bg-green-200 hover:bg-green-300 p-4 rounded-lg text-center transition-colors"
          >
            <div className="text-2xl mb-2">📚</div>
            <div className="text-green-800 font-semibold">心理健康文章</div>
          </Link>
          <Link
            href="/therapists"
            className="bg-green-200 hover:bg-green-300 p-4 rounded-lg text-center transition-colors"
          >
            <div className="text-2xl mb-2">👥</div>
            <div className="text-green-800 font-semibold">心理師介紹</div>
          </Link>
          <Link
            href="/assessments"
            className="bg-amber-200 hover:bg-amber-300 p-4 rounded-lg text-center transition-colors"
          >
            <div className="text-2xl mb-2">📋</div>
            <div className="text-amber-800 font-semibold">專業心理測驗</div>
          </Link>
        </div>
      </section>

      {/* Counseling Room Environment Section */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-black text-center mb-8">諮商室環境</h2>
            <p className="text-lg text-black text-center mb-12 max-w-3xl mx-auto">
              我們提供溫馨、安全且隱私的諮商環境，讓您能在舒適的空間中敞開心扉，與心理師進行深度對話。
            </p>
            
            {/* Carousel Container */}
            <div className="relative">
              {/* Left Arrow */}
              <button
                onClick={prevSlide}
                className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition-all duration-300 hover:scale-110"
                aria-label="Previous images"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              {/* Images Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 transition-all duration-500 ease-in-out">
                {visibleImages.map((image, index) => (
                  <div key={`${currentIndex}-${index}`} className="group">
                    <div className="relative overflow-hidden rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
                      <Image
                        src={image.src}
                        alt={image.alt}
                        width={400}
                        height={300}
                        className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Right Arrow */}
              <button
                onClick={nextSlide}
                className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition-all duration-300 hover:scale-110"
                aria-label="Next images"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
                </button>

              {/* Dots Indicator */}
              <div className="flex justify-center mt-6 space-x-2">
                {Array.from({ length: Math.ceil(images.length - imagesPerView + 1) }).map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentIndex(index)}
                    className={`w-3 h-3 rounded-full transition-all duration-300 ${
                      currentIndex === index ? 'bg-black' : 'bg-gray-300 hover:bg-gray-400'
                    }`}
                    aria-label={`Go to slide ${index + 1}`}
                  />
                ))}
              </div>
            </div>
            
            <div className="text-center mt-8">
              <p className="text-black">每間諮商室都經過精心設計，確保您的隱私與舒適感</p>
            </div>
          </div>
        </div>
      </section>

      {/* Location Information Section */}
      <section className="container mx-auto px-4 py-12 bg-transparent">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-green-800 mb-8 text-center">張老師台北心理諮商所</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* 地圖區域 */}
            <div className="bg-transparent rounded-lg overflow-hidden">
              <div className="h-96 w-full">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3614.5!2d121.55!3d25.082!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2z5Y-w5YyX5biC5Lit5bGx5Y2A5aSn55u06KGXMjDlt7cxOOiZnw!5e0!3m2!1szh-TW!2stw!4v1693123456789!5m2!1szh-TW!2stw"
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="張老師台北心理諮商所位置"
                ></iframe>
              </div>
            </div>

            {/* 機構資訊區域 */}
            <div className="bg-transparent rounded-lg p-6">
              <h3 className="text-2xl font-bold text-green-800 mb-6">機構資訊</h3>
              
              <div className="space-y-4">
                {/* 機構名稱 */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm2 6a2 2 0 114 0 2 2 0 01-4 0zm8-2a2 2 0 100 4 2 2 0 000-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800">機構名稱</h4>
                    <p className="text-gray-600">財團法人「張老師」基金會台北分事務所</p>
                  </div>
                </div>

                {/* 聯絡電話 */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800">聯絡電話</h4>
                    <p className="text-gray-600">(02) 2532-6180</p>
                  </div>
                </div>

                {/* 地址 */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800">機構地址</h4>
                    <p className="text-gray-600">台北市中山區大直街 20 巷 18 號</p>
                  </div>
                </div>

                {/* 營業時間 */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-amber-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800">服務時間</h4>
                    <div className="text-gray-600 space-y-1">
                      <p>週一至週六：09:00 - 21:30</p>
                      <p>週日：09:00 - 17:00</p>
                    </div>
                  </div>
                </div>

                {/* 交通資訊 */}
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M8 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM15 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" />
                      <path d="M3 4a1 1 0 00-1 1v10a1 1 0 001 1h1.05a2.5 2.5 0 014.9 0H10a1 1 0 001-1V5a1 1 0 00-1-1H3zM14 7a1 1 0 00-1 1v6.05A2.5 2.5 0 0115.95 16H17a1 1 0 001-1V8a1 1 0 00-1-1h-3z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800">交通方式</h4>
                    <div className="text-gray-600 space-y-1">
                      <p>🚇 捷運大直站 1 號出口，步行約 5 分鐘</p>
                      <p>🚌 公車站：大直站、捷運大直站</p>
                      <p>🚗 附近有路邊停車格及收費停車場</p>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
