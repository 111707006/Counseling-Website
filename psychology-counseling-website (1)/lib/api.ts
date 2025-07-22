// API 配置文件
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// API 端點配置
export const API_ENDPOINTS = {
  // 心理師相關
  therapists: {
    profiles: '/api/therapists/profiles/',
    specialties: '/api/therapists/specialties/',
    categories: '/api/therapists/specialty-categories/',
  },
  // 預約相關
  appointments: {
    create: '/api/appointments/',
    list: '/api/appointments/',
    query: '/api/appointments/query/',
    confirm: '/api/appointments/{id}/confirm/',
    selectTime: '/api/appointments/{id}/select_time/',
  },
  // 測驗相關
  assessments: {
    tests: '/api/assessments/tests/',
    questions: '/api/assessments/tests/{code}/questions/',
    responses: '/api/assessments/tests/{code}/responses/',
    results: '/api/assessments/results/',
  },
  // 文章相關
  articles: {
    list: '/api/articles/',
    detail: '/api/articles/{id}/',
  }
}

// API 客戶端類別
class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  // 通用請求方法
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // GET 請求
  async get<T>(endpoint: string, params?: Record<string, string>): Promise<T> {
    let url = endpoint
    if (params) {
      const queryString = new URLSearchParams(params).toString()
      url += `?${queryString}`
    }
    return this.request<T>(url, { method: 'GET' })
  }

  // POST 請求
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // PUT 請求
  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // PATCH 請求
  async patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // DELETE 請求
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

// 創建 API 客戶端實例
export const apiClient = new ApiClient()

// 類型定義
export interface TherapistProfile {
  id: number
  user_id?: number
  name: string
  title: string
  license_number: string
  education: string
  experience: string
  specialties: Specialty[]
  specialties_display: string
  specialties_by_category: Record<string, string[]>
  specialties_text?: string
  beliefs: string
  publications: string[]
  photo?: string
  available_times: AvailableTime[]
  consultation_modes: string[]
  pricing: Record<string, number>
  created_at: string
}

export interface Specialty {
  id: number
  name: string
  category: SpecialtyCategory
  category_name: string
  description: string
  is_active: boolean
}

export interface SpecialtyCategory {
  id: number
  name: string
  description: string
}

export interface AvailableTime {
  id: number
  day_of_week: string
  start_time: string
  end_time: string
}

// API 服務函數
export const therapistService = {
  // 獲取所有心理師
  async getProfiles(params?: { 
    search?: string
    specialties?: string
    specialties__category?: string 
  }): Promise<TherapistProfile[]> {
    return apiClient.get<TherapistProfile[]>(API_ENDPOINTS.therapists.profiles, params)
  },

  // 獲取單一心理師
  async getProfile(id: number): Promise<TherapistProfile> {
    return apiClient.get<TherapistProfile>(`${API_ENDPOINTS.therapists.profiles}${id}/`)
  },

  // 獲取專業領域列表
  async getSpecialties(params?: { category?: string }): Promise<Specialty[]> {
    return apiClient.get<Specialty[]>(API_ENDPOINTS.therapists.specialties, params)
  },

  // 獲取專業領域分類
  async getCategories(): Promise<SpecialtyCategory[]> {
    return apiClient.get<SpecialtyCategory[]>(API_ENDPOINTS.therapists.categories)
  }
}