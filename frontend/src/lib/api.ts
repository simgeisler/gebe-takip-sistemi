const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit & { query?: Record<string, string> } = {}
  ): Promise<T> {
    let url = `${this.baseURL}${endpoint}`;
    
    // Add query parameters
    if (options.query) {
      const searchParams = new URLSearchParams(options.query);
      url += `?${searchParams.toString()}`;
    }
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Remove query from config to avoid passing it to fetch
    const { query, ...fetchOptions } = config;

    // Add auth token if available
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchOptions.headers = {
        ...fetchOptions.headers,
        'Authorization': `Bearer ${token}`,
      };
    }

    let response: Response;
    try {
      response = await fetch(url, fetchOptions);
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      throw new Error(
        msg === "Failed to fetch"
          ? "Sunucuya bağlanılamadı. Backend çalışıyor mu kontrol edin (ör. http://127.0.0.1:8000/healthz)."
          : msg
      );
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      let detail = (error as { detail?: unknown; message?: string }).detail ?? (error as { message?: string }).message ?? 'Request failed';
      if (Array.isArray(detail)) {
        detail = detail
          .map((row: { msg?: string; loc?: unknown }) => row.msg || JSON.stringify(row))
          .join('; ');
      }
      throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
    }

    return response.json();
  }

  // Auth endpoints
  async login(email: string, password: string) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(data: {
    name: string;
    email: string;
    password: string;
    sat?: string;
    kilo: number;
  }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  // Dashboard endpoints
  async getDashboard() {
    return this.request('/dashboard');
  }

  async getPregnancyStatus() {
    return this.request('/pregnancy/status');
  }

  // Health tracking endpoints
  async getMeasurements() {
    return this.request('/measurements/');
  }

  async createMeasurement(data: any) {
    return this.request('/measurements/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Calendar endpoints
  async getCalendarEvents() {
    return this.request('/calendar/events');
  }

  async createCalendarEvent(data: any) {
    return this.request('/calendar/events', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async deleteCalendarEvent(eventId: number) {
    return this.request(`/calendar/events/${eventId}`, {
      method: 'DELETE',
    });
  }

  // Forum endpoints
  async getForumPosts() {
    return this.request('/forum');
  }

  async createForumPost(data: any) {
    return this.request('/forum', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Chat endpoints
  async sendMessage(message: string) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // Health extended endpoints
  async getHealthSummary(limit: number = 3) {
    return this.request('/health/measurements/summary', {
      method: 'GET',
      query: { limit: limit.toString() }
    });
  }

  async getHealthTrends(trendType: string, limit: number = 6) {
    return this.request(`/health/measurements/trends/${trendType}`, {
      method: 'GET',
      query: { limit: limit.toString() }
    });
  }

  // Forum extended endpoints
  async getForumQuestions(category?: string) {
    const query = category ? { category } : {};
    return this.request('/forum/questions', {
      method: 'GET',
      query
    });
  }

  async createForumQuestion(data: any) {
    return this.request('/forum/questions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async likeForumQuestion(questionId: number) {
    return this.request(`/forum/questions/${questionId}/likes`, {
      method: 'POST',
    });
  }

  async unlikeForumQuestion(questionId: number) {
    return this.request(`/forum/questions/${questionId}/likes`, {
      method: 'DELETE',
    });
  }

  async deleteForumQuestion(questionId: number) {
    return this.request(`/forum/questions/${questionId}`, {
      method: 'DELETE',
    });
  }

  async getForumQuestion(questionId: number) {
    return this.request(`/forum/questions/${questionId}`, {
      method: 'GET',
    });
  }

  async listForumReplies(questionId: number) {
    return this.request(`/forum/questions/${questionId}/replies`, {
      method: 'GET',
    });
  }

  async createForumReply(questionId: number, data: any) {
    return this.request(`/forum/questions/${questionId}/replies`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async listForumLikes(questionId: number) {
    return this.request(`/forum/questions/${questionId}/likes`, {
      method: 'GET',
    });
  }

  // Library extended endpoints
  async getLibraryArticles(search?: string, category?: string) {
    const query: any = {};
    if (search) query.search = search;
    if (category) query.category = category;
    
    return this.request('/library/articles', {
      method: 'GET',
      query
    });
  }

  async getLibraryArticle(articleId: number) {
    return this.request(`/library/articles/${articleId}`, {
      method: 'GET',
    });
  }

  async likeLibraryArticle(articleId: number) {
    return this.request(`/library/articles/${articleId}/likes`, {
      method: 'POST',
    });
  }

  async unlikeLibraryArticle(articleId: number) {
    return this.request(`/library/articles/${articleId}/likes`, {
      method: 'DELETE',
    });
  }

  async listLibraryLikes(articleId: number) {
    return this.request(`/library/articles/${articleId}/likes`, {
      method: 'GET',
    });
  }

  // Content endpoints
  async getLibraryContent() {
    return this.request('/content');
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
