/**
 * 对话 API
 */
import client from './client'

export interface ChatRequest {
  message: string
  conversation_id?: string
  visitor_id?: string
}

export interface VisemeKeyframe {
  time: number
  viseme: string
  weight: number
}

export interface ChatResponse {
  reply: string
  conversation_id: string
  audio_url: string | null
  viseme_timeline: VisemeKeyframe[]
  expression: string
  sentiment: { score: number; label: string }
  sources: string[]
}

export async function sendMessage(data: ChatRequest): Promise<ChatResponse> {
  const response = await client.post<ChatResponse>('/chat', data)
  return response.data
}

export async function textToSpeech(text: string): Promise<Blob | null> {
  try {
    const formData = new FormData()
    formData.append('text', text)
    const response = await client.post('/voice/tts', formData, {
      responseType: 'blob',
    })
    if (String(response.headers['content-type'] || '').includes('audio')) {
      return response.data
    }
    return null
  } catch {
    return null
  }
}
