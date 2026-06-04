/**
 * 数据分析 API
 */
import client from './client'

export interface DashboardData {
  total_conversations: number
  total_messages: number
  today_conversations: number
  avg_sentiment: number
  avg_response_time_ms: number
  satisfaction_score: number
  top_questions: Array<{ question: string; count: number }>
  daily_trend: Array<{ date: string; count: number }>
}

export async function getDashboard(): Promise<DashboardData> {
  const response = await client.get<DashboardData>('/analytics/dashboard')
  return response.data
}

export async function getSentimentReport(days: number = 7): Promise<any> {
  const response = await client.get('/analytics/sentiment', { params: { days } })
  return response.data
}
