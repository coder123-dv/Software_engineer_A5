<template>
  <div class="chat-view">
    <!-- 3D 数字人区域 -->
    <div class="avatar-section">
      <div ref="canvasContainer" class="avatar-canvas"></div>
      <div class="avatar-status">
        <span class="status-dot" :class="avatarState"></span>
        {{ avatarState === 'speaking' ? '正在讲解...' : '等待中' }}
      </div>
    </div>

    <!-- 对话区域 -->
    <div class="chat-section">
      <div class="chat-header">
        <h2>🏛️ 灵山胜境 · AI导游</h2>
        <el-button size="small" @click="$router.push('/admin/login')">管理后台</el-button>
      </div>

      <!-- 消息列表 -->
      <div class="messages" ref="messagesRef">
        <div v-for="(msg, idx) in messages" :key="idx" class="message" :class="msg.role">
          <div class="message-avatar">
            {{ msg.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <p>{{ msg.content }}</p>
            <span class="message-time">{{ msg.time }}</span>
          </div>
        </div>
        <div v-if="loading" class="message assistant">
          <div class="message-avatar">🤖</div>
          <div class="message-content typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          placeholder="输入您想了解的景区信息..."
          @keyup.enter="sendMsg"
          :disabled="loading"
          size="large"
        >
          <template #append>
            <el-button @click="sendMsg" :loading="loading" type="primary">
              发送
            </el-button>
          </template>
        </el-input>
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
}

const messages = ref<ChatMessage[]>([
  { role: 'assistant', content: '您好！我是灵山胜境的AI导游小灵 🙋‍♀️ 很高兴为您服务！您想了解什么呢？', time: '刚刚' },
])
const inputText = ref('')
const loading = ref(false)
const conversationId = ref<string | null>(null)
const avatarState = ref<'idle' | 'speaking'>('idle')
const messagesRef = ref<HTMLElement>()
const canvasContainer = ref<HTMLElement>()

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

async function sendMsg() {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: text,
    time: new Date().toLocaleTimeString(),
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
      time: new Date().toLocaleTimeString(),
    })

    // 模拟口型播放时间
    const speakDuration = response.reply.length * 200 // ~200ms/字
    setTimeout(() => {
      avatarState.value = 'idle'
    }, speakDuration)
  } catch (err: any) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，服务暂时不可用，请稍后重试。',
      time: new Date().toLocaleTimeString(),
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  // TODO: 初始化 Three.js 场景加载 VRM 模型
})
</script>

<style scoped lang="scss">
.chat-view {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.avatar-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;

  .avatar-canvas {
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse at center, rgba(255,255,255,0.1) 0%, transparent 70%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 120px;

    &::after {
      content: '🧑‍🏫';
    }
  }

  .avatar-status {
    position: absolute;
    bottom: 20px;
    background: rgba(0,0,0,0.6);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #67c23a;

      &.speaking {
        animation: pulse 1s infinite;
        background: #409eff;
      }
    }
  }
}

.chat-section {
  width: 420px;
  background: white;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 10px rgba(0,0,0,0.1);

  .chat-header {
    padding: 16px 20px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      font-size: 16px;
      color: #303133;
    }
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .message {
    display: flex;
    gap: 10px;

    &.user {
      flex-direction: row-reverse;

      .message-content {
        background: #ecf5ff;
        border-radius: 12px 0 12px 12px;
      }
    }

    &.assistant .message-content {
      background: #f4f4f5;
      border-radius: 0 12px 12px 12px;
    }

    .message-avatar {
      font-size: 24px;
      flex-shrink: 0;
    }

    .message-content {
      padding: 10px 14px;
      max-width: 280px;

      p {
        font-size: 14px;
        line-height: 1.6;
        word-break: break-word;
      }

      .message-time {
        font-size: 11px;
        color: #999;
        margin-top: 4px;
        display: block;
      }

      &.typing {
        display: flex;
        gap: 4px;
        padding: 14px;

        span {
          width: 8px;
          height: 8px;
          background: #999;
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out both;

          &:nth-child(1) { animation-delay: -0.32s; }
          &:nth-child(2) { animation-delay: -0.16s; }
        }
      }
    }
  }

  .input-area {
    padding: 16px;
    border-top: 1px solid #eee;
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
