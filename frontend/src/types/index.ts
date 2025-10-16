export interface BusinessInsights {
  industry?: string;
  company_size?: string;
  location?: string;
  usp?: string;
  products_services?: string;
  target_audience?: string;
  contact_info?: {
    emails?: string[];
    phones?: string[];
    social_media?: string[];
  };
}

export interface AnalyzeResponse {
  url: string;
  insights: BusinessInsights;
  timestamp: string;
}

export interface ChatResponse {
  response: string;
  timestamp: string;
}

export interface ConversationMessage {
  id: string;
  query: string;
  response: string;
  timestamp: string;
}

export interface ApiError {
  error: string;
  detail?: string;
}
