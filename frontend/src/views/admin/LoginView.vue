<template>
  <div class="login-page">
    <!-- 动态背景 -->
    <div class="login-bg">
      <div class="ink-wash"></div>
      <div class="gold-accent"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-card">
      <div class="card-glow"></div>

      <!-- Logo区 -->
      <div class="login-brand">
        <span class="brand-symbol">☸</span>
        <h1>灵山胜境</h1>
        <p>智慧导览管理系统</p>
      </div>

      <!-- 表单 -->
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>账号</label>
          <div class="input-field">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <input v-model="form.username" type="text" placeholder="请输入用户名" />
          </div>
        </div>

        <div class="form-group">
          <label>密码</label>
          <div class="input-field">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0110 0v4"/>
            </svg>
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'" placeholder="请输入密码" />
            <button type="button" class="pwd-toggle" @click="showPwd = !showPwd">
              <svg v-if="!showPwd" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            </button>
          </div>
        </div>

        <button type="submit" class="login-btn" :class="{ loading }">
          <span v-if="!loading">进入系统</span>
          <span v-else class="btn-loading">
            <span></span><span></span><span></span>
          </span>
        </button>
      </form>

      <p class="login-hint">默认凭据: admin / admin123</p>
    </div>

    <!-- 底部装饰 -->
    <div class="login-footer">
      <span>景区导览服务AI数字人 · 管理平台</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import client from '@/api/client'

const router = useRouter()
const loading = ref(false)
const showPwd = ref(false)
const form = ref({ username: '', password: '' })

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const res = await client.post('/auth/login', form.value)
    localStorage.setItem('token', res.data.access_token)
    ElMessage.success('登录成功')
    router.push('/admin')
  } catch {
    ElMessage.error('用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: #0a0a14;
}

/* === 背景 === */
.login-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;

  .ink-wash {
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse 80% 60% at 20% 80%, rgba(91, 140, 111, 0.15), transparent),
      radial-gradient(ellipse 60% 80% at 80% 20%, rgba(26, 26, 46, 0.8), transparent),
      radial-gradient(ellipse 100% 100% at 50% 50%, rgba(13, 13, 26, 1), transparent);
    animation: breathe 10s ease-in-out infinite;
  }

  .gold-accent {
    position: absolute;
    width: 400px;
    height: 400px;
    top: 10%;
    right: 15%;
    background: radial-gradient(circle, rgba(197, 165, 90, 0.08), transparent 70%);
    border-radius: 50%;
    animation: float 8s ease-in-out infinite;
  }
}

/* === 登录卡片 === */
.login-card {
  position: relative;
  width: 400px;
  padding: 48px 40px;
  background: rgba(20, 20, 35, 0.8);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(197, 165, 90, 0.2);
  border-radius: 24px;
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 1;

  .card-glow {
    position: absolute;
    inset: -1px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(197, 165, 90, 0.1), transparent, rgba(91, 140, 111, 0.1));
    z-index: -1;
    opacity: 0;
    transition: opacity 0.4s;
  }

  &:hover .card-glow {
    opacity: 1;
  }
}

.login-brand {
  text-align: center;
  margin-bottom: 36px;

  .brand-symbol {
    font-size: 42px;
    display: block;
    margin-bottom: 12px;
    animation: breathe 4s ease-in-out infinite;
  }

  h1 {
    font-family: var(--font-display);
    font-size: 26px;
    font-weight: 700;
    color: var(--zen-cloud);
    letter-spacing: 3px;
  }

  p {
    font-size: 13px;
    color: var(--zen-gold);
    margin-top: 6px;
    letter-spacing: 1px;
  }
}

/* === 表单 === */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  label {
    display: block;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 8px;
    font-weight: 500;
  }
}

.input-field {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  height: 48px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);

  svg {
    color: rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
    transition: color 0.3s;
  }

  input {
    flex: 1;
    border: none;
    background: transparent;
    color: var(--zen-cloud);
    font-size: 14px;
    font-family: var(--font-body);
    outline: none;

    &::placeholder {
      color: rgba(255, 255, 255, 0.25);
    }
  }

  .pwd-toggle {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    padding: 4px;
    display: flex;

    &:hover {
      color: var(--zen-gold);
    }
  }

  &:focus-within {
    border-color: var(--zen-gold);
    background: rgba(197, 165, 90, 0.04);
    box-shadow: 0 0 0 3px rgba(197, 165, 90, 0.08);

    svg {
      color: var(--zen-gold);
    }
  }
}

.login-btn {
  margin-top: 8px;
  height: 48px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--zen-gold), #d4a543);
  color: var(--zen-ink);
  font-size: 15px;
  font-weight: 700;
  font-family: var(--font-display);
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);

  &:hover:not(.loading) {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(197, 165, 90, 0.3);
  }

  &:active:not(.loading) {
    transform: translateY(0);
  }

  &.loading {
    opacity: 0.7;
    cursor: wait;
  }

  .btn-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;

    span {
      width: 6px;
      height: 6px;
      background: var(--zen-ink);
      border-radius: 50%;
      animation: bounce 1.2s infinite ease-in-out both;

      &:nth-child(1) { animation-delay: -0.32s; }
      &:nth-child(2) { animation-delay: -0.16s; }
    }
  }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); }
  40% { transform: scale(1.2); }
}

.login-hint {
  text-align: center;
  margin-top: 24px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.25);
}

/* === 底部 === */
.login-footer {
  position: absolute;
  bottom: 24px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.2);
}

/* === 动画 === */
@keyframes breathe {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.02); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
