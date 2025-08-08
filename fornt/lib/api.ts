// API 基礎配置
// 直接連接到Django後端，避免代理問題
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

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
        const responseText = await response.text();
        try {
          const errorData = JSON.parse(responseText);
          errorDetail = JSON.stringify(errorData, null, 2);
          console.error('API Error Details:', errorData);
        } catch {
          errorDetail = responseText;
          console.error('API Error Text:', errorDetail);
        }
      } catch (readError) {
        errorDetail = 'Unable to read error response';
        console.error('Failed to read error response:', readError);
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

export interface Specialty {
  id: number;
  name: string;
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
  specialties_list: string[];
  specialties_text: string;
  beliefs: string;
  // publications: string[];  // 暫時移除
  photo: string | null;
  available_times: AvailableTime[];
  consultation_modes?: string[];  // 設為可選，防止錯誤
  pricing?: { [key: string]: number };  // 設為可選，防止錯誤
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

// 獲取專業領域
export async function getSpecialties(): Promise<Specialty[]> {
  return apiRequest<Specialty[]>('/api/therapists/specialties/');
}

// 搜索心理師（支持多種篩選條件）
export async function searchTherapists(params: {
  search?: string;
  specialties?: number[];
  consultation_modes?: string;
}): Promise<TherapistProfile[]> {
  const queryParams = new URLSearchParams();
  
  if (params.search) {
    queryParams.append('search', params.search);
  }
  
  if (params.specialties?.length) {
    params.specialties.forEach(id => queryParams.append('specialties', id.toString()));
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

export interface ArticleImage {
  id: number;
  image: string;
  image_url: string;
  caption: string;
  order: number;
  created_at: string;
}

export interface Article {
  id: number;
  title: string;
  excerpt: string;
  content: string;
  tags: string[];
  author: number | null;
  author_name: string;
  published_at: string;
  is_published: boolean;
  featured_image: string | null;
  featured_image_url: string | null;
  images: ArticleImage[];
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

// 公告相關 API

export interface AnnouncementCategory {
  id: number;
  name: string;
  description: string;
  color: string;
  is_active: boolean;
  order: number;
  announcements_count: number;
  created_at: string;
}

export interface AnnouncementImage {
  id: number;
  image: string;
  image_url: string;
  caption: string;
  order: number;
  created_at: string;
}

export interface AnnouncementAuthor {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

export interface Announcement {
  id: number;
  title: string;
  summary: string;
  content: string;
  category?: AnnouncementCategory;
  featured_image_url?: string;
  additional_images: AnnouncementImage[];
  priority: 'low' | 'medium' | 'high';
  priority_display: string;
  status: 'draft' | 'published' | 'archived';
  status_display: string;
  is_pinned: boolean;
  show_on_homepage: boolean;
  publish_date: string;
  expire_date?: string;
  author: AnnouncementAuthor;
  views_count: number;
  likes_count: number;
  can_display: boolean;
  is_expired: boolean;
  created_at: string;
  updated_at: string;
}

export interface AnnouncementListResponse {
  count: number;
  next?: string;
  previous?: string;
  results: Announcement[];
}

export interface AnnouncementHomepageData {
  pinned_announcements: Announcement[];
  recent_announcements: Announcement[];
}

export interface AnnouncementStats {
  total_published: number;
  total_categories: number;
  monthly_announcements: number;
}

// 獲取公告列表
export async function getAnnouncements(params?: {
  search?: string;
  category?: string;
  priority?: string;
  page?: number;
}): Promise<Announcement[]> {
  const queryParams = new URLSearchParams();
  
  if (params?.search) queryParams.append('search', params.search);
  if (params?.category) queryParams.append('category', params.category);
  if (params?.priority) queryParams.append('priority', params.priority);
  if (params?.page) queryParams.append('page', params.page.toString());
  
  const endpoint = `/api/announcements/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  return apiRequest<Announcement[]>(endpoint);
}

// 獲取單一公告詳情
export async function getAnnouncement(id: number): Promise<Announcement> {
  return apiRequest<Announcement>(`/api/announcements/${id}/`);
}

// 獲取公告分類列表
export async function getAnnouncementCategories(): Promise<AnnouncementCategory[]> {
  return apiRequest<AnnouncementCategory[]>('/api/announcements/categories/');
}

// 獲取首頁公告
export async function getHomepageAnnouncements(): Promise<AnnouncementHomepageData> {
  return apiRequest<AnnouncementHomepageData>('/api/announcements/homepage/');
}

// 獲取公告統計
export async function getAnnouncementStats(): Promise<AnnouncementStats> {
  return apiRequest<AnnouncementStats>('/api/announcements/stats/');
}

// 為公告點讚
export async function likeAnnouncement(id: number): Promise<{ success: boolean; likes_count: number }> {
  return apiRequest<{ success: boolean; likes_count: number }>(`/api/announcements/${id}/like/`, {
    method: 'POST',
  });
}