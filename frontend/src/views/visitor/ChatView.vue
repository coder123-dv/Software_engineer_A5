<template>
  <div class="chat-view">
    <!-- 水墨山水动态背景 -->
    <div class="bg-layer">
      <div class="mist mist-1"></div>
      <div class="mist mist-2"></div>
      <div class="mist mist-3"></div>
      <div class="mountain-silhouette"></div>
      <div class="particles">
        <span v-for="i in 20" :key="i" class="particle" :style="particleStyle(i)"></span>
      </div>
    </div>

    <!-- 3D 数字人区域 -->
    <div class="avatar-section">
      <div ref="canvasContainer" class="avatar-canvas">
        <!-- Three.js 将在这里渲染 VRM 模型 -->
        <div class="avatar-placeholder" :class="{ speaking: avatarState === 'speaking' }">
          <div class="avatar-ring"></div>
          <div class="avatar-glow"></div>
          <span class="avatar-emoji">🧑‍🏫</span>
        </div>
      </div>

      <!-- 状态指示器 -->
      <div class="avatar-status-bar">
        <div class="status-indicator" :class="avatarState">
          <span class="status-dot"></span>
          <span class="status-text">
            {{ avatarState === 'speaking' ? '正在讲解中...' : '等待您的提问' }}
          </span>
        </div>
      </div>

      <!-- 品牌标识 -->
      <div class="brand-mark">
        <span class="brand-icon">☸</span>
        <span class="brand-text">灵山胜境</span>
        <span class="brand-sub">AI导览</span>
      </div>
    </div>

    <!-- 对话面板 -->
    <div class="chat-panel">
      <!-- 头部 -->
      <header class="chat-header">
        <div class="header-left">
          <h1 class="header-title">灵山胜境</h1>
          <p class="header-subtitle">智慧导览 · AI数字人</p>
        </div>
        <div class="header-right">
          <button class="btn-icon" title="管理后台" @click="$router.push('/admin/login')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 15a3 3 0 100-6 3 3 0 000 6z"/>
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- 消息列表 -->
      <div class="messages-container" ref="messagesRef">
        <div class="messages-inner">
          <!-- 欢迎提示 -->
          <div class="welcome-hint" v-if="messages.length <= 1">
            <div class="hint-grid">
              <button class="hint-card" @click="sendQuick('灵山大佛有什么历史？')">
                <span class="hint-icon">🏛️</span>
                <span class="hint-text">灵山大佛的历史</span>
              </button>
              <button class="hint-card" @click="sendQuick('推荐一条游览路线')">
                <span class="hint-icon">🗺️</span>
                <span class="hint-text">推荐游览路线</span>
              </button>
              <button class="hint-card" @click="sendQuick('梵宫有什么特色？')">
                <span class="hint-icon">✨</span>
                <span class="hint-text">梵宫的特色</span>
              </button>
              <button class="hint-card" @click="sendQuick('今天的开放时间是？')">
                <span class="hint-icon">🕐</span>
                <span class="hint-text">开放时间</span>
              </button>
            </div>
          </div>

          <TransitionGroup name="message">
            <div v-for="(msg, idx) in messages" :key="idx" class="message" :class="msg.role">
              <div class="message-bubble">
                <p class="message-text">{{ msg.content }}</p>
                <div class="message-meta">
                  <span v-if="msg.role === 'assistant' && msg.sources?.length" class="message-source">
                    📖 {{ msg.sources[0] }}
                  </span>
                  <span class="message-time">{{ msg.time }}</span>
                </div>
              </div>
            </div>
          </TransitionGroup>

          <!-- 加载状态 -->
          <div v-if="loading" class="message assistant">
            <div class="message-bubble loading-bubble">
              <div class="typing-dots">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-wrapper">
          <input
            v-model="inputText"
            @keyup.enter="sendMsg"
            :disabled="loading"
            class="chat-input"
            placeholder="输入您想了解的景区信息..."
          />
          <button class="send-btn" @click="sendMsg" :disabled="loading || !inputText.trim()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <p class="input-hint">按 Enter 发送 · AI回答基于灵山胜境知识库</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { sendMessage, type ChatResponse } from '@/api/chat'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  time: string
  sources?: string[]
}

const messages = ref<ChatMessage[]>([
  {
    role: 'assistant',
    content: '您好！我是灵山胜境的AI导游「小灵」✨ 这里是一片融汇千年佛教文化与现代艺术的圣地。请问您想了解哪方面的内容？',
    time: formatTime(),
  },
])
const inputText = ref('')
const loading = ref(false)
const conversationId = ref<string | null>(null)
const avatarState = ref<'idle' | 'speaking'>('idle')
const messagesRef = ref<HTMLElement>()
const canvasContainer = ref<HTMLElement>()

function formatTime() {
  return new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function particleStyle(i: number) {
  const x = Math.random() * 100
  const y = Math.random() * 100
  const size = 2 + Math.random() * 3
  const delay = Math.random() * 6
  const duration = 4 + Math.random() * 4
  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`,
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

function sendQuick(text: string) {
  inputText.value = text
  sendMsg()
}

async function sendMsg() {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  messages.value.push({
    role: 'user',
    content: text,
    time: formatTime(),
  })
  inputText.value = ''
  loading.value = true
  scrollToBottom()

  try {
    const response: ChatResponse = await sendMessage({
      message: text,
      conversation_id: conversationId.value || undefined,
    })

    conversationId.value = response.conversation_id
    avatarState.value = 'speaking'

    messages.value.push({
      role: 'assistant',
      content: response.reply,
      time: formatTime(),
      sources: response.sources,
    })

    const speakDuration = response.reply.length * 180
    setTimeout(() => {
      avatarState.value = 'idle'
    }, speakDuration)
  } catch {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，我暂时无法回答。请检查网络连接或稍后再试。',
      time: formatTime(),
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  // TODO: 初始化 Three.js + VRM 场景
})
</script>

<style scoped lang="scss">
.chat-view {
  display: flex;
  height: 100vh;
  position: relative;
  overflow: hidden;
  background: #0d0d1a;
}

/* === 动态背景层 === */
.bg-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.mist {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: breathe 8s ease-in-out infinite;

  &.mist-1 {
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse, rgba(91, 140, 111, 0.3), transparent);
    top: -10%;
    left: 10%;
    animation-delay: 0s;
  }

  &.mist-2 {
    width: 500px;
    height: 500px;
    background: radial-gradient(ellipse, rgba(197, 165, 90, 0.15), transparent);
    bottom: -20%;
    right: 20%;
    animation-delay: 3s;
  }

  &.mist-3 {
    width: 400px;
    height: 300px;
    background: radial-gradient(ellipse, rgba(91, 140, 111, 0.2), transparent);
    top: 50%;
    left: 40%;
    animation-delay: 5s;
  }
}

.mountain-silhouette {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 30%;
  background: linear-gradient(to top, rgba(13, 13, 26, 0.9), transparent);
  clip-path: polygon(0 100%, 5% 60%, 15% 75%, 25% 45%, 35% 65%, 45% 35%, 55% 55%, 65% 30%, 75% 50%, 85% 40%, 95% 55%, 100% 70%, 100% 100%);
  opacity: 0.4;
}

.particles {
  position: absolute;
  inset: 0;

  .particle {
    position: absolute;
    background: var(--zen-gold);
    border-radius: 50%;
    opacity: 0;
    animation: float 6s ease-in-out infinite, fadeIn 2s ease-out forwards;
  }
}

/* === 数字人区域 === */
.avatar-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.avatar-canvas {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;

  .avatar-emoji {
    font-size: 140px;
    filter: drop-shadow(0 0 40px rgba(197, 165, 90, 0.3));
    transition: transform var(--duration-slow) var(--ease-out-expo);
    animation: float 6s ease-in-out infinite;
  }

  .avatar-ring {
    position: absolute;
    width: 240px;
    height: 240px;
    border: 2px solid rgba(197, 165, 90, 0.2);
    border-radius: 50%;
    animation: breathe 4s ease-in-out infinite;
  }

  .avatar-glow {
    position: absolute;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(197, 165, 90, 0.1), transparent 70%);
    border-radius: 50%;
    animation: breathe 3s ease-in-out infinite;
    animation-delay: 1s;
  }

  &.speaking {
    .avatar-emoji {
      animation: float 2s ease-in-out infinite;
    }

    .avatar-ring {
      border-color: rgba(197, 165, 90, 0.5);
      animation: pulse-ring 2s ease-out infinite;
    }

    .avatar-glow {
      background: radial-gradient(circle, rgba(197, 165, 90, 0.25), transparent 70%);
    }
  }
}

.avatar-status-bar {
  position: absolute;
  bottom: 40px;

  .status-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 20px;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(197, 165, 90, 0.2);
    border-radius: var(--radius-full);

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--zen-jade);
      transition: all var(--duration-normal) var(--ease-out-expo);
    }

    .status-text {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.7);
      font-family: var(--font-body);
    }

    &.speaking {
      border-color: rgba(197, 165, 90, 0.4);

      .status-dot {
        background: var(--zen-gold);
        box-shadow: 0 0 12px var(--zen-gold-glow);
        animation: breathe 1.5s ease-in-out infinite;
      }
    }
  }
}

.brand-mark {
  position: absolute;
  top: 32px;
  left: 32px;
  display: flex;
  align-items: center;
  gap: 10px;

  .brand-icon {
    font-size: 28px;
    animation: breathe 6s ease-in-out infinite;
  }

  .brand-text {
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 700;
    color: var(--zen-gold);
    letter-spacing: 2px;
  }

  .brand-sub {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
    padding-left: 8px;
    border-left: 1px solid rgba(255, 255, 255, 0.15);
  }
}

/* === 对话面板 === */
.chat-panel {
  width: 440px;
  background: rgba(13, 13, 26, 0.85);
  backdrop-filter: blur(30px);
  border-left: 1px solid rgba(197, 165, 90, 0.15);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 2;
}

.chat-header {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(197, 165, 90, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: fadeInUp var(--duration-slow) var(--ease-out-expo);

  .header-title {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 700;
    color: var(--zen-cloud);
    letter-spacing: 1px;
  }

  .header-subtitle {
    font-size: 12px;
    color: var(--zen-gold);
    margin-top: 2px;
    letter-spacing: 0.5px;
  }

  .btn-icon {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--duration-fast) var(--ease-in-out);

    &:hover {
      border-color: var(--zen-gold);
      color: var(--zen-gold);
      background: rgba(197, 165, 90, 0.1);
    }
  }
}

/* === 消息区域 === */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.messages-inner {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 100%;
}

.welcome-hint {
  margin-bottom: 16px;
  animation: fadeInUp 0.6s var(--ease-out-expo) 0.3s both;

  .hint-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .hint-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(197, 165, 90, 0.15);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--duration-fast) var(--ease-in-out);
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    text-align: left;
    font-family: var(--font-body);

    .hint-icon {
      font-size: 18px;
      flex-shrink: 0;
    }

    &:hover {
      background: rgba(197, 165, 90, 0.08);
      border-color: var(--zen-gold);
      color: var(--zen-cloud);
      transform: translateY(-1px);
    }
  }
}

/* === 消息气泡 === */
.message {
  display: flex;
  animation: fadeInUp 0.4s var(--ease-out-expo);

  &.user {
    justify-content: flex-end;

    .message-bubble {
      background: linear-gradient(135deg, rgba(197, 165, 90, 0.2), rgba(197, 165, 90, 0.08));
      border: 1px solid rgba(197, 165, 90, 0.3);
      border-radius: var(--radius-lg) var(--radius-sm) var(--radius-lg) var(--radius-lg);
    }
  }

  &.assistant {
    justify-content: flex-start;

    .message-bubble {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-sm) var(--radius-lg) var(--radius-lg) var(--radius-lg);
    }
  }
}

.message-bubble {
  max-width: 85%;
  padding: 14px 18px;
  backdrop-filter: blur(10px);

  .message-text {
    font-size: 14px;
    line-height: 1.7;
    color: var(--zen-cloud);
    word-break: break-word;
  }

  .message-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    gap: 8px;

    .message-source {
      font-size: 11px;
      color: var(--zen-jade-light);
      opacity: 0.8;
    }

    .message-time {
      font-size: 11px;
      color: rgba(255, 255, 255, 0.3);
      margin-left: auto;
    }
  }

  &.loading-bubble {
    padding: 16px 24px;
  }
}

.typing-dots {
  display: flex;
  gap: 6px;

  span {
    width: 7px;
    height: 7px;
    background: var(--zen-gold);
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;
    opacity: 0.6;

    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
    &:nth-child(3) { animation-delay: 0s; }
  }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

/* === 消息过渡动画 === */
.message-enter-active {
  transition: all 0.4s var(--ease-out-expo);
}
.message-enter-from {
  opacity: 0;
  transform: translateY(16px);
}

/* === 输入区域 === */
.input-area {
  padding: 20px 24px;
  border-top: 1px solid rgba(197, 165, 90, 0.1);
  animation: fadeInUp 0.6s var(--ease-out-expo) 0.5s both;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 165, 90, 0.2);
  border-radius: var(--radius-lg);
  padding: 6px 6px 6px 18px;
  transition: all var(--duration-fast) var(--ease-in-out);

  &:focus-within {
    border-color: var(--zen-gold);
    box-shadow: 0 0 0 3px rgba(197, 165, 90, 0.1);
    background: rgba(255, 255, 255, 0.06);
  }
}

.chat-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--zen-cloud);
  font-size: 14px;
  font-family: var(--font-body);
  outline: none;

  &::placeholder {
    color: rgba(255, 255, 255, 0.3);
  }

  &:disabled {
    opacity: 0.5;
  }
}

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  border: none;
  background: var(--zen-gold);
  color: var(--zen-ink);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--duration-fast) var(--ease-in-out);
  flex-shrink: 0;

  &:hover:not(:disabled) {
    background: var(--zen-gold-light);
    transform: scale(1.05);
    box-shadow: 0 4px 16px rgba(197, 165, 90, 0.3);
  }

  &:active:not(:disabled) {
    transform: scale(0.95);
  }

  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
}

.input-hint {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.25);
  text-align: center;
  margin-top: 10px;
}

/* === 响应式 === */
@media (max-width: 768px) {
  .chat-view {
    flex-direction: column;
  }

  .avatar-section {
    height: 35vh;
  }

  .chat-panel {
    width: 100%;
    flex: 1;
    border-left: none;
    border-top: 1px solid rgba(197, 165, 90, 0.15);
  }

  .brand-mark {
    top: 16px;
    left: 16px;
  }
}
</style>
