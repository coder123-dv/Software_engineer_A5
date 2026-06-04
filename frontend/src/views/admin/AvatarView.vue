<template>
  <div class="avatar-view">
    <header class="page-header">
      <div>
        <h1>数字人管理</h1>
        <p>配置AI导游的外观、声音与人格</p>
      </div>
    </header>

    <div class="avatar-grid">
      <!-- 预览 -->
      <div class="preview-card">
        <div class="preview-scene">
          <div class="preview-glow"></div>
          <div class="preview-avatar">
            <span>🧑‍🏫</span>
          </div>
          <div class="preview-ring"></div>
        </div>
        <div class="preview-info">
          <h3>{{ config.name }}</h3>
          <p class="greeting-preview">"{{ config.greeting }}"</p>
        </div>
      </div>

      <!-- 配置表单 -->
      <div class="config-card">
        <div class="config-section">
          <h3 class="section-title">基础信息</h3>
          <div class="form-row">
            <label>名称</label>
            <input v-model="config.name" class="zen-input" />
          </div>
          <div class="form-row">
            <label>人设定位</label>
            <textarea v-model="config.personality" class="zen-input textarea" rows="3" placeholder="描述数字人的性格特点..."></textarea>
          </div>
          <div class="form-row">
            <label>开场白</label>
            <textarea v-model="config.greeting" class="zen-input textarea" rows="2" placeholder="游客第一次看到数字人时的欢迎语..."></textarea>
          </div>
        </div>

        <div class="config-section">
          <h3 class="section-title">语音配置</h3>
          <div class="form-row">
            <label>音色</label>
            <div class="voice-options">
              <label
                v-for="voice in voices" :key="voice.id"
                class="voice-card" :class="{ active: config.voice_id === voice.id }"
              >
                <input type="radio" :value="voice.id" v-model="config.voice_id" hidden />
                <span class="voice-icon">{{ voice.icon }}</span>
                <span class="voice-name">{{ voice.name }}</span>
                <span class="voice-desc">{{ voice.desc }}</span>
              </label>
            </div>
          </div>
          <div class="form-row">
            <label>语速 <span class="value-badge">{{ config.voice_speed.toFixed(1) }}x</span></label>
            <input type="range" v-model.number="config.voice_speed" min="0.5" max="2.0" step="0.1" class="zen-slider" />
          </div>
        </div>

        <div class="config-section">
          <h3 class="section-title">模型文件</h3>
          <div class="form-row">
            <label>VRM 模型路径</label>
            <input v-model="config.vrm_model_url" class="zen-input" placeholder="/models/guide.vrm" />
          </div>
        </div>

        <button class="zen-btn primary save-btn" @click="handleSave">
          保存配置
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import client from '@/api/client'

const voices = [
  { id: 'zh-CN-XiaoxiaoNeural', name: '晓晓', desc: '温柔女声', icon: '🎀' },
  { id: 'zh-CN-YunyangNeural', name: '云扬', desc: '稳重男声', icon: '🎩' },
  { id: 'zh-CN-XiaomoNeural', name: '晓墨', desc: '活泼女声', icon: '🌸' },
]

const config = ref({
  id: 0,
  name: '小灵',
  vrm_model_url: '/models/guide.vrm',
  voice_id: 'zh-CN-XiaoxiaoNeural',
  voice_speed: 1.0,
  voice_pitch: 1.0,
  personality: '你是灵山胜境的AI导游小灵，热情友善、知识渊博，善于用生动的语言描述景区特色。',
  greeting: '您好！我是灵山胜境的AI导游小灵，很高兴为您服务！',
  is_default: true,
})

onMounted(async () => {
  try {
    const res = await client.get('/avatar/default')
    Object.assign(config.value, res.data)
  } catch { /* use defaults */ }
})

async function handleSave() {
  try {
    if (config.value.id) {
      await client.put(`/avatar/${config.value.id}`, config.value)
    }
    ElMessage.success('配置已保存')
  } catch { ElMessage.error('保存失败') }
}
</script>

<style scoped lang="scss">
.avatar-view {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.page-header {
  margin-bottom: 28px;
  h1 { font-family: var(--font-display); font-size: 24px; font-weight: 700; color: var(--zen-cloud); }
  p { font-size: 13px; color: rgba(255, 255, 255, 0.4); margin-top: 4px; }
}

.avatar-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  align-items: start;
}

/* === 预览卡 === */
.preview-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  overflow: hidden;
  position: sticky;
  top: 28px;

  .preview-scene {
    position: relative;
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at center, rgba(197, 165, 90, 0.05), transparent);

    .preview-glow {
      position: absolute;
      width: 160px;
      height: 160px;
      background: radial-gradient(circle, rgba(197, 165, 90, 0.15), transparent 70%);
      border-radius: 50%;
      animation: breathe 4s ease-in-out infinite;
    }

    .preview-avatar {
      font-size: 100px;
      z-index: 1;
      animation: float 5s ease-in-out infinite;
    }

    .preview-ring {
      position: absolute;
      width: 180px;
      height: 180px;
      border: 1.5px solid rgba(197, 165, 90, 0.2);
      border-radius: 50%;
      animation: breathe 5s ease-in-out infinite;
    }
  }

  .preview-info {
    padding: 20px;
    text-align: center;
    border-top: 1px solid rgba(255, 255, 255, 0.05);

    h3 {
      font-family: var(--font-display);
      font-size: 18px;
      color: var(--zen-gold);
      margin-bottom: 8px;
    }

    .greeting-preview {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.5);
      font-style: italic;
      line-height: 1.5;
    }
  }
}

/* === 配置表单 === */
.config-card {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.config-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 24px;

  .section-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--zen-gold);
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
}

.form-row {
  margin-bottom: 16px;

  &:last-child { margin-bottom: 0; }

  label {
    display: block;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 8px;
    font-weight: 500;

    .value-badge {
      display: inline-block;
      background: rgba(197, 165, 90, 0.1);
      color: var(--zen-gold);
      padding: 1px 8px;
      border-radius: 10px;
      font-size: 12px;
      margin-left: 6px;
    }
  }
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
  &.textarea { resize: vertical; min-height: 60px; line-height: 1.6; }
}

.voice-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.voice-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 10px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s;

  .voice-icon { font-size: 24px; }
  .voice-name { font-size: 13px; color: var(--zen-cloud); font-weight: 600; }
  .voice-desc { font-size: 11px; color: rgba(255, 255, 255, 0.4); }

  &:hover { border-color: rgba(197, 165, 90, 0.3); }

  &.active {
    border-color: var(--zen-gold);
    background: rgba(197, 165, 90, 0.08);
    .voice-name { color: var(--zen-gold); }
  }
}

.zen-slider {
  width: 100%;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  outline: none;

  &::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--zen-gold);
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(197, 165, 90, 0.4);
  }
}

.zen-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: var(--font-body);
  cursor: pointer;
  border: none;
  transition: all 0.25s;

  &.primary {
    background: var(--zen-gold);
    color: var(--zen-ink);
    &:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(197, 165, 90, 0.3); }
  }
}

.save-btn { align-self: flex-end; }

@keyframes breathe {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
</style>
