// API 基礎配置
// 使用相對路徑，透過Next.js的API代理轉發到Django後端
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

// 處理圖片URL的輔助函數
export function processImageUrls(content: string): string {
  if (!content) return content;
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  return content.replace(/src="\/media\//g, `src="${baseUrl}/media/`);
}

// API 請求封裝函數
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    console.log(`API Request: ${config.method || 'GET'} ${url}`);
    if (config.body) {
      console.log('Request body:', config.body);
    }
    
    const response = await fetch(url, config);
    
    if (!response.ok) {
      // 嘗試讀取錯誤詳細資訊
      let errorDetail = '';
      try {
        const errorData = await response.json();
        errorDetail = JSON.stringify(errorData, null, 2);
        console.error('API Error Details:', errorData);
      } catch {
        errorDetail = await response.text();
        console.error('API Error Text:', errorDetail);
      }
      throw new Error(`API Error: ${response.status} ${response.statusText}\nDetails: ${errorDetail}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`API Request failed for ${endpoint}:`, error);
    throw error;
  }
}

// 心理師相關 API

export interface SpecialtyCategory {
  id: number;
  name: string;
  description: string;
}

export interface Specialty {
  id: number;
  name: string;
  category: SpecialtyCategory;
  category_name: string;
  description: string;
  is_active: boolean;
}

export interface AvailableTime {
  id: number;
  day_of_week: string;
  start_time: string;
  end_time: string;
}

export interface TherapistProfile {
  id: number;
  user_id: number | null;
  name: string;
  title: string;
  license_number: string;
  education: string;
  experience: string;
  specialties: Specialty[];
  specialties_display: string;
  specialties_by_category: Record<string, string[]>;
  specialties_text: string;
  beliefs: string;
  publications: string[];
  photo: string | null;
  available_times: AvailableTime[];
  consultation_modes: string[];
  pricing: Record<string, number>;
  created_at: string;
}

// 獲取所有心理師
export async function getTherapists(): Promise<TherapistProfile[]> {
  return apiRequest<TherapistProfile[]>('/api/therapists/profiles/');
}

// 獲取單一心理師詳情
export async function getTherapist(id: number): Promise<TherapistProfile> {
  return apiRequest<TherapistProfile>(`/api/therapists/profiles/${id}/`);
}

// 獲取專業領域分類
export async function getSpecialtyCategories(): Promise<SpecialtyCategory[]> {
  return apiRequest<SpecialtyCategory[]>('/api/therapists/specialty-categories/');
}

// 獲取專業領域
export async function getSpecialties(): Promise<Specialty[]> {
  return apiRequest<Specialty[]>('/api/therapists/specialties/');
}

// 搜索心理師（支持多種篩選條件）
export async function searchTherapists(params: {
  search?: string;
  specialties?: number[];
  specialties__category?: number;
  consultation_modes?: string;
}): Promise<TherapistProfile[]> {
  const queryParams = new URLSearchParams();
  
  if (params.search) {
    queryParams.append('search', params.search);
  }
  
  if (params.specialties?.length) {
    params.specialties.forEach(id => queryParams.append('specialties', id.toString()));
  }
  
  if (params.specialties__category) {
    queryParams.append('specialties__category', params.specialties__category.toString());
  }
  
  if (params.consultation_modes) {
    queryParams.append('consultation_modes', params.consultation_modes);
  }
  
  const endpoint = `/api/therapists/profiles/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  return apiRequest<TherapistProfile[]>(endpoint);
}

// 根據單一專業領域篩選心理師
export async function getTherapistsBySpecialty(specialtyId: number): Promise<TherapistProfile[]> {
  return searchTherapists({ specialties: [specialtyId] });
}

// 預約相關 API

export interface PreferredPeriod {
  date: string;
  periods: ('morning' | 'afternoon' | 'evening')[];
}

export interface AppointmentCreateRequest {
  email: string;
  id_number: string;
  consultation_type: 'online' | 'offline';
  therapist?: number;
  specialty?: number;
  preferred_periods?: PreferredPeriod[];
  name?: string;
  phone?: string;
  main_concerns?: string;
  previous_therapy?: boolean;
  urgency?: 'low' | 'medium' | 'high';
  special_needs?: string;
}

// 預約詳細資訊介面
export interface AppointmentDetail {
  name: string;
  phone: string;
  main_concerns: string;
  previous_therapy: boolean;
  urgency: 'low' | 'medium' | 'high';
  special_needs: string;
  specialty_requested?: number;
}

// 偏好時段介面
export interface PreferredPeriodResponse {
  id: number;
  date: string;
  period: 'morning' | 'afternoon' | 'evening';
  period_display: string;
}

// 可用時段介面
export interface AvailableSlotResponse {
  id: number;
  slot_time: string;
}

// 完整的預約回應介面（匹配後端新格式）
export interface AppointmentResponse {
  id: number;
  user: string;                                    // 用戶Email
  therapist: string;                               // 心理師姓名
  slot: AvailableSlotResponse | null;              // 確認的時段資訊
  consultation_type: string;                       // 諮商方式代碼
  consultation_type_display: string;               // 諮商方式中文顯示
  price: string;                                   // 費用
  status: string;                                  // 狀態代碼
  status_display: string;                          // 狀態中文顯示
  created_at: string;                              // 建立時間
  confirmed_at?: string;                           // 確認時間
  confirmed_datetime?: string;                     // 確認的具體時間
  preferred_periods: PreferredPeriodResponse[];    // 偏好時段列表
  detail: AppointmentDetail;                       // 預約詳細資訊
}

// 建立預約
export async function createAppointment(data: AppointmentCreateRequest): Promise<AppointmentResponse> {
  return apiRequest<AppointmentResponse>('/api/appointments/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// 查詢預約（使用 Email + 身分證字號）
export async function queryAppointments(email: string, id_number: string): Promise<AppointmentResponse[]> {
  return apiRequest<AppointmentResponse[]>('/api/appointments/query/', {
    method: 'POST',
    body: JSON.stringify({ email, id_number }),
  });
}

// 心理測驗相關 API

export interface AssessmentTest {
  code: string;
  name: string;
  description: string;
}

export interface AssessmentChoice {
  id: number;
  text: string;
  score: number;
}

export interface AssessmentQuestion {
  id: number;
  order: number;
  text: string;
  choices: AssessmentChoice[];
}

export interface AssessmentResponseItem {
  question: number;
  choice: number;
}

export interface AssessmentCreateRequest {
  items: AssessmentResponseItem[];
}

export interface AssessmentResult {
  id: number;
  test: string;
  created_at: string;
  total_score: number;
  risk_level: string;
  items: {
    question: number;
    choice: number;
    score: number;
  }[];
}

// 獲取所有測驗
export async function getAssessmentTests(): Promise<AssessmentTest[]> {
  return apiRequest<AssessmentTest[]>('/api/assessments/tests/');
}

// 獲取測驗題目
export async function getAssessmentQuestions(testCode: string): Promise<AssessmentQuestion[]> {
  return apiRequest<AssessmentQuestion[]>(`/api/assessments/tests/${testCode}/questions/`);
}

// 提交測驗答案
export async function submitAssessment(testCode: string, data: AssessmentCreateRequest): Promise<AssessmentResult> {
  return apiRequest<AssessmentResult>(`/api/assessments/tests/${testCode}/responses/`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// 獲取測驗結果歷史
export async function getAssessmentResults(): Promise<AssessmentResult[]> {
  try {
    return await apiRequest<AssessmentResult[]>('/api/assessments/results/');
  } catch (error) {
    // 如果是認證錯誤（用戶未登入），返回空數組
    if (error instanceof Error && error.message.includes('401')) {
      return [];
    }
    throw error;
  }
}

// 文章相關 API

export interface Article {
  id: number;
  title: string;
  content: string;
  tags: string[];
  author: number | null;
  published_at: string;
}

// 獲取所有文章
export async function getArticles(): Promise<Article[]> {
  return apiRequest<Article[]>('/api/articles/articles/');
}

// 獲取單一文章詳情
export async function getArticle(id: number): Promise<Article> {
  return apiRequest<Article>(`/api/articles/articles/${id}/`);
}

// 創建文章（需要管理員或心理師權限）
export async function createArticle(data: Omit<Article, 'id' | 'published_at' | 'author'>): Promise<Article> {
  return apiRequest<Article>('/api/articles/articles/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// 更新文章（需要管理員或心理師權限）
export async function updateArticle(id: number, data: Partial<Article>): Promise<Article> {
  return apiRequest<Article>(`/api/articles/articles/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

// 刪除文章（需要管理員或心理師權限）
export async function deleteArticle(id: number): Promise<void> {
  return apiRequest<void>(`/api/articles/articles/${id}/`, {
    method: 'DELETE',
  });
}