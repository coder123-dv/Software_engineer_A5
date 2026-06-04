/**
 * 知识库 API
 */
import client from './client'

export interface KnowledgeDoc {
  id: number
  title: string
  category: string
  content?: string
  source_file: string
  is_active: boolean
  created_at: string
  chunk_count: number
}

export async function listKnowledge(category?: string): Promise<KnowledgeDoc[]> {
  const params = category ? { category } : {}
  const response = await client.get<KnowledgeDoc[]>('/knowledge', { params })
  return response.data
}

export async function getKnowledge(id: number): Promise<KnowledgeDoc> {
  const response = await client.get<KnowledgeDoc>(`/knowledge/${id}`)
  return response.data
}

export async function createKnowledge(data: { title: string; category: string; content: string }): Promise<any> {
  const response = await client.post('/knowledge', data)
  return response.data
}

export async function uploadKnowledge(file: File, title: string, category: string): Promise<any> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('title', title)
  formData.append('category', category)
  const response = await client.post('/knowledge/upload', formData)
  return response.data
}

export async function deleteKnowledge(id: number): Promise<void> {
  await client.delete(`/knowledge/${id}`)
}
