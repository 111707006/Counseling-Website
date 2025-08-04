import Link from "next/link"
import Image from "next/image"

export default function HomePage() {
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

      {/* Additional Information Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-green-800 mb-6">關於張老師台北心理諮商所</h2>
          <p className="text-lg text-green-700 leading-relaxed mb-8">
            心理諮商是一次與自己的語言整理，找出自己真正的聲音。我們致力於提供專業、溫暖的心理諮商服務，
            陪伴每一位來談者在人生的旅程中找到屬於自己的答案。
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="text-xl font-semibold text-green-800 mb-2">專業陪伴</h3>
              <p className="text-green-600">經驗豐富的心理師團隊，提供專業且溫暖的陪伴</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-amber-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">🌱</span>
              </div>
              <h3 className="text-xl font-semibold text-green-800 mb-2">成長支持</h3>
              <p className="text-green-600">協助您探索內在，促進個人成長與自我實現</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-2xl">💚</span>
              </div>
              <h3 className="text-xl font-semibold text-green-800 mb-2">用心關懷</h3>
              <p className="text-green-600">以同理心與專業知識，為您的心理健康把關</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
