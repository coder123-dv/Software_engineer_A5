<template>
  <div class="knowledge-view">
    <el-card>
      <template #header>
        <div class="header">
          <span>📚 知识库管理</span>
          <div>
            <el-button type="primary" @click="showUpload = true">上传文档</el-button>
            <el-button @click="showAdd = true">手动添加</el-button>
          </div>
        </div>
      </template>

      <el-table :data="documents" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ categoryMap[row.category] || row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="source_file" label="来源文件" width="180" show-overflow-tooltip />
        <el-table-column prop="chunk_count" label="分块数" width="80" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 上传文档对话框 -->
    <el-dialog v-model="showUpload" title="上传文档" width="500px">
      <el-form>
        <el-form-item label="文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            accept=".docx,.xlsx,.txt"
            :on-change="handleFileChange"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 .docx / .xlsx / .txt 格式</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="标题">
          <el-input v-model="uploadForm.title" placeholder="留空则使用文件名" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="uploadForm.category">
            <el-option label="景点介绍" value="scenic_intro" />
            <el-option label="历史文化" value="history" />
            <el-option label="常见问题" value="faq" />
            <el-option label="游览路线" value="route" />
            <el-option label="通用" value="general" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUpload = false">取消</el-button>
        <el-button type="primary" @click="handleUpload" :loading="uploading">上传</el-button>
      </template>
    </el-dialog>

    <!-- 手动添加对话框 -->
    <el-dialog v-model="showAdd" title="添加知识" width="600px">
      <el-form>
        <el-form-item label="标题">
          <el-input v-model="addForm.title" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="addForm.category">
            <el-option label="景点介绍" value="scenic_intro" />
            <el-option label="历史文化" value="history" />
            <el-option label="常见问题" value="faq" />
            <el-option label="游览路线" value="route" />
            <el-option label="通用" value="general" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="addForm.content" type="textarea" :rows="8" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAdd = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">保存</el-button>
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
const uploading = ref(false)
const selectedFile = ref<File | null>(null)

const uploadForm = ref({ title: '', category: 'general' })
const addForm = ref({ title: '', category: 'general', content: '' })

const categoryMap: Record<string, string> = {
  scenic_intro: '景点介绍',
  history: '历史文化',
  culture: '文化',
  faq: '常见问题',
  route: '游览路线',
  general: '通用',
}

async function loadData() {
  loading.value = true
  try {
    documents.value = await listKnowledge()
  } finally {
    loading.value = false
  }
}

function handleFileChange(file: any) {
  selectedFile.value = file.raw
}

async function handleUpload() {
  if (!selectedFile.value) {
    ElMessage.warning('请选择文件')
    return
  }
  uploading.value = true
  try {
    await uploadKnowledge(selectedFile.value, uploadForm.value.title, uploadForm.value.category)
    ElMessage.success('上传成功')
    showUpload.value = false
    loadData()
  } catch {
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
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
    loadData()
  } catch {
    ElMessage.error('添加失败')
  }
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定要删除这条知识吗？', '提示', { type: 'warning' })
  try {
    await deleteKnowledge(id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(loadData)
</script>

<style scoped lang="scss">
.knowledge-view {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
