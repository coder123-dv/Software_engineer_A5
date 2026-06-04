<template>
  <div class="knowledge-view">
    <!-- 页头 -->
    <header class="page-header">
      <div>
        <h1>知识库管理</h1>
        <p>管理景区讲解词、文史资料与常见问答</p>
      </div>
      <div class="header-actions">
        <button class="zen-btn secondary" @click="showAdd = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
          手动添加
        </button>
        <button class="zen-btn primary" @click="showUpload = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          上传文档
        </button>
      </div>
    </header>

    <!-- 文档列表 -->
    <div class="doc-grid">
      <div v-for="doc in documents" :key="doc.id" class="doc-card">
        <div class="doc-icon">
          {{ categoryIcons[doc.category] || '📄' }}
        </div>
        <div class="doc-info">
          <h4>{{ doc.title }}</h4>
          <div class="doc-meta">
            <span class="doc-tag">{{ categoryMap[doc.category] || doc.category }}</span>
            <span class="doc-chunks">{{ doc.chunk_count }} 块</span>
            <span :class="['doc-status', doc.is_active ? 'active' : 'inactive']">
              {{ doc.is_active ? '启用' : '停用' }}
            </span>
          </div>
        </div>
        <button class="doc-delete" @click="handleDelete(doc.id)" title="删除">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
          </svg>
        </button>
      </div>

      <div v-if="!documents.length && !loading" class="empty-state">
        <span class="empty-icon">📚</span>
        <p>知识库为空</p>
        <span>上传文档以构建景区知识库</span>
      </div>
    </div>

    <!-- 上传对话框 -->
    <el-dialog v-model="showUpload" title="上传文档" width="480px" :append-to-body="true">
      <div class="upload-form">
        <div class="upload-zone" @dragover.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
          <input ref="fileInput" type="file" accept=".docx,.xlsx,.txt" @change="handleFileSelect" hidden />
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p v-if="!selectedFile">点击或拖拽文件到此处</p>
          <p v-else class="file-name">{{ selectedFile.name }}</p>
          <span class="upload-hint">支持 .docx / .xlsx / .txt</span>
        </div>

        <div class="form-row">
          <label>标题</label>
          <input v-model="uploadForm.title" placeholder="留空则使用文件名" class="zen-input" />
        </div>
        <div class="form-row">
          <label>分类</label>
          <select v-model="uploadForm.category" class="zen-input">
            <option value="scenic_intro">景点介绍</option>
            <option value="history">历史文化</option>
            <option value="faq">常见问题</option>
            <option value="route">游览路线</option>
            <option value="general">通用</option>
          </select>
        </div>
      </div>
      <template #footer>
        <button class="zen-btn secondary" @click="showUpload = false">取消</button>
        <button class="zen-btn primary" @click="handleUpload" :disabled="!selectedFile">上传</button>
      </template>
    </el-dialog>

    <!-- 手动添加对话框 -->
    <el-dialog v-model="showAdd" title="添加知识" width="600px" :append-to-body="true">
      <div class="upload-form">
        <div class="form-row">
          <label>标题</label>
          <input v-model="addForm.title" class="zen-input" placeholder="输入知识标题" />
        </div>
        <div class="form-row">
          <label>分类</label>
          <select v-model="addForm.category" class="zen-input">
            <option value="scenic_intro">景点介绍</option>
            <option value="history">历史文化</option>
            <option value="faq">常见问题</option>
            <option value="route">游览路线</option>
            <option value="general">通用</option>
          </select>
        </div>
        <div class="form-row">
          <label>内容</label>
          <textarea v-model="addForm.content" class="zen-input textarea" rows="8" placeholder="输入知识内容..."></textarea>
        </div>
      </div>
      <template #footer>
        <button class="zen-btn secondary" @click="showAdd = false">取消</button>
        <button class="zen-btn primary" @click="handleAdd">保存</button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listKnowledge, uploadKnowledge, createKnowledge, deleteKnowledge, type KnowledgeDoc } from '@/api/knowledge'

const documents = ref<KnowledgeDoc[]>([])
const loading = ref(false)
const showUpload = ref(false)
const showAdd = ref(false)
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()

const uploadForm = ref({ title: '', category: 'general' })
const addForm = ref({ title: '', category: 'general', content: '' })

const categoryMap: Record<string, string> = {
  scenic_intro: '景点介绍', history: '历史文化', culture: '文化',
  faq: '常见问题', route: '游览路线', general: '通用',
}

const categoryIcons: Record<string, string> = {
  scenic_intro: '🏛️', history: '📜', culture: '🎭',
  faq: '❓', route: '🗺️', general: '📄',
}

async function loadData() {
  loading.value = true
  try { documents.value = await listKnowledge() }
  finally { loading.value = false }
}

function triggerFileInput() { fileInput.value?.click() }

function handleFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files?.[0]) selectedFile.value = input.files[0]
}

function handleDrop(e: DragEvent) {
  const file = e.dataTransfer?.files[0]
  if (file) selectedFile.value = file
}

async function handleUpload() {
  if (!selectedFile.value) return
  try {
    await uploadKnowledge(selectedFile.value, uploadForm.value.title, uploadForm.value.category)
    ElMessage.success('上传成功')
    showUpload.value = false
    selectedFile.value = null
    loadData()
  } catch { ElMessage.error('上传失败') }
}

async function handleAdd() {
  if (!addForm.value.title || !addForm.value.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }
  try {
    await createKnowledge(addForm.value)
    ElMessage.success('添加成功')
    showAdd.value = false
    addForm.value = { title: '', category: 'general', content: '' }
    loadData()
  } catch { ElMessage.error('添加失败') }
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定删除？删除后将无法恢复。', '确认', { type: 'warning' })
  try { await deleteKnowledge(id); ElMessage.success('已删除'); loadData() }
  catch { ElMessage.error('删除失败') }
}

onMounted(loadData)
</script>

<style scoped lang="scss">
.knowledge-view {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 28px;

  h1 { font-family: var(--font-display); font-size: 24px; font-weight: 700; color: var(--zen-cloud); }
  p { font-size: 13px; color: rgba(255, 255, 255, 0.4); margin-top: 4px; }

  .header-actions {
    display: flex;
    gap: 10px;
  }
}

/* === 按钮 === */
.zen-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  font-family: var(--font-body);
  cursor: pointer;
  border: none;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);

  &.primary {
    background: var(--zen-gold);
    color: var(--zen-ink);

    &:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(197, 165, 90, 0.3); }
  }

  &.secondary {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);

    &:hover { border-color: var(--zen-gold); color: var(--zen-gold); }
  }

  &:disabled { opacity: 0.4; cursor: not-allowed; }
}

/* === 文档网格 === */
.doc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.doc-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  transition: all 0.25s ease;

  &:hover {
    border-color: rgba(197, 165, 90, 0.2);
    background: rgba(255, 255, 255, 0.05);
  }

  .doc-icon {
    font-size: 28px;
    flex-shrink: 0;
  }

  .doc-info {
    flex: 1;
    min-width: 0;

    h4 {
      font-size: 14px;
      font-weight: 600;
      color: var(--zen-cloud);
      margin-bottom: 6px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .doc-meta {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 12px;
    }

    .doc-tag {
      background: rgba(197, 165, 90, 0.1);
      color: var(--zen-gold);
      padding: 2px 8px;
      border-radius: 20px;
    }

    .doc-chunks { color: rgba(255, 255, 255, 0.4); }

    .doc-status {
      &.active { color: var(--zen-jade-light); }
      &.inactive { color: rgba(255, 255, 255, 0.3); }
    }
  }

  .doc-delete {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
    padding: 6px;
    border-radius: 8px;
    transition: all 0.2s;

    &:hover {
      color: var(--zen-danger);
      background: rgba(232, 93, 93, 0.1);
    }
  }
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 64px 20px;
  color: rgba(255, 255, 255, 0.3);

  .empty-icon { font-size: 48px; display: block; margin-bottom: 12px; }
  p { font-size: 16px; color: rgba(255, 255, 255, 0.5); margin-bottom: 6px; }
}

/* === 表单 === */
.upload-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.upload-zone {
  border: 2px dashed rgba(197, 165, 90, 0.2);
  border-radius: 14px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  color: rgba(255, 255, 255, 0.5);

  &:hover {
    border-color: var(--zen-gold);
    background: rgba(197, 165, 90, 0.04);
  }

  p { margin-top: 10px; font-size: 14px; }
  .file-name { color: var(--zen-gold); font-weight: 600; }
  .upload-hint { font-size: 12px; color: rgba(255, 255, 255, 0.3); display: block; margin-top: 6px; }
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;

  label { font-size: 13px; color: rgba(255, 255, 255, 0.6); font-weight: 500; }
}

.zen-input {
  width: 100%;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: var(--zen-cloud);
  font-size: 14px;
  font-family: var(--font-body);
  outline: none;
  transition: border-color 0.3s;

  &:focus { border-color: var(--zen-gold); }
  &::placeholder { color: rgba(255, 255, 255, 0.25); }

  &.textarea { resize: vertical; min-height: 120px; line-height: 1.6; }
}

select.zen-input {
  appearance: none;
  cursor: pointer;
}
</style>
