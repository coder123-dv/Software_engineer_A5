<template>
  <div class="avatar-view">
    <el-row :gutter="20">
      <!-- 预览区域 -->
      <el-col :span="10">
        <el-card>
          <template #header>🧑‍🏫 数字人预览</template>
          <div class="preview-area">
            <div class="avatar-placeholder">🧑‍🏫</div>
            <p class="greeting">"{{ config.greeting }}"</p>
          </div>
        </el-card>
      </el-col>

      <!-- 配置区域 -->
      <el-col :span="14">
        <el-card>
          <template #header>⚙️ 形象配置</template>
          <el-form :model="config" label-width="100px">
            <el-form-item label="名称">
              <el-input v-model="config.name" />
            </el-form-item>
            <el-form-item label="人设定位">
              <el-input v-model="config.personality" type="textarea" :rows="3" />
            </el-form-item>
            <el-form-item label="开场白">
              <el-input v-model="config.greeting" type="textarea" :rows="2" />
            </el-form-item>
            <el-form-item label="语音音色">
              <el-select v-model="config.voice_id" style="width: 100%">
                <el-option label="晓晓 (女声·温柔)" value="zh-CN-XiaoxiaoNeural" />
                <el-option label="云扬 (男声·稳重)" value="zh-CN-YunyangNeural" />
                <el-option label="晓墨 (女声·活泼)" value="zh-CN-XiaomoNeural" />
              </el-select>
            </el-form-item>
            <el-form-item label="语速">
              <el-slider v-model="config.voice_speed" :min="0.5" :max="2.0" :step="0.1" show-stops />
            </el-form-item>
            <el-form-item label="VRM模型">
              <el-input v-model="config.vrm_model_url" placeholder="/models/guide.vrm" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import client from '@/api/client'

const config = ref({
  id: 0,
  name: '小灵',
  vrm_model_url: '/models/guide.vrm',
  voice_id: 'zh-CN-XiaoxiaoNeural',
  voice_speed: 1.0,
  voice_pitch: 1.0,
  personality: '你是灵山胜境的AI导游小灵，热情友善、知识渊博，善于用生动的语言描述景区特色。',
  greeting: '您好！我是灵山胜境的AI导游小灵，很高兴为您服务！有什么想了解的吗？',
  is_default: true,
})

onMounted(async () => {
  try {
    const res = await client.get('/avatar/default')
    Object.assign(config.value, res.data)
  } catch {
    // 使用默认值
  }
})

async function handleSave() {
  try {
    if (config.value.id) {
      await client.put(`/avatar/${config.value.id}`, config.value)
    }
    ElMessage.success('保存成功')
  } catch {
    ElMessage.error('保存失败')
  }
}
</script>

<style scoped lang="scss">
.avatar-view {
  .preview-area {
    text-align: center;
    padding: 40px 20px;

    .avatar-placeholder {
      font-size: 100px;
      margin-bottom: 20px;
    }

    .greeting {
      color: #606266;
      font-style: italic;
    }
  }
}
</style>
