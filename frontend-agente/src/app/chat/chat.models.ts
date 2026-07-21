/** Contratos de la API de Pegasus Dev Assistant. */

export interface SourceResponse {
  source: string;
  heading: string;
  distance: number;
}

export interface ChatRequest {
  question: string;
  session_id?: string;
}

export interface ChatResponse {
  session_id: string;
  answer: string;
  sources: SourceResponse[];
}

export interface HealthResponse {
  status: 'ready' | 'degraded';
  api_key_configured: boolean;
  index_available: boolean;
  prompt_available: boolean;
}

/** Mensaje mostrado en la conversación. */
export interface ChatMessage {
  role: 'user' | 'assistant' | 'error';
  text: string;
  sources: SourceResponse[];
  timestamp: Date;
}
