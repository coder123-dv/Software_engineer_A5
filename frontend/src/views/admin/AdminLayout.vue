<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-brand">
        <span class="brand-symbol">☸</span>
        <div class="brand-info">
          <span class="brand-name">灵山胜境</span>
          <span class="brand-tag">管理后台</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-item" :class="{ active: route.path === '/admin' }">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/>
            <rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/>
          </svg>
          <span>数据大屏</span>
        </router-link>

        <router-link to="/admin/knowledge" class="nav-item" :class="{ active: route.path === '/admin/knowledge' }">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>
          </svg>
          <span>知识库</span>
        </router-link>

        <router-link to="/admin/avatar" class="nav-item" :class="{ active: route.path === '/admin/avatar' }">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/>
          </svg>
          <span>数字人</span>
        </router-link>

        <router-link to="/admin/analytics" class="nav-item" :class="{ active: route.path === '/admin/analytics' }">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/>
          </svg>
          <span>情感报告</span>
        </router-link>
      </nav>

      <!-- 底部 -->
      <div class="sidebar-footer">
        <button class="nav-item visitor-link" @click="$router.push('/')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/>
          </svg>
          <span>游客端</span>
        </button>

        <button class="nav-item logout" @click="logout">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          <span>退出</span>
        </button>
      </div>
    </aside>

    <!-- 主内容 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

function logout() {
  localStorage.removeItem('token')
  router.push('/admin/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  height: 100vh;
  background: #0d0d1a;
  overflow: hidden;
}

/* === 侧边栏 === */
.sidebar {
  width: 220px;
  background: rgba(15, 15, 28, 0.95);
  border-right: 1px solid rgba(197, 165, 90, 0.1);
  display: flex;
  flex-direction: column;
  padding: 24px 12px;
  flex-shrink: 0;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  margin-bottom: 32px;

  .brand-symbol {
    font-size: 28px;
    animation: breathe 6s ease-in-out infinite;
  }

  .brand-info {
    display: flex;
    flex-direction: column;

    .brand-name {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 700;
      color: var(--zen-cloud);
      letter-spacing: 1px;
    }

    .brand-tag {
      font-size: 11px;
      color: var(--zen-gold);
      margin-top: 2px;
    }
  }
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  font-family: var(--font-body);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);

  svg {
    flex-shrink: 0;
    opacity: 0.6;
    transition: opacity 0.25s;
  }

  &:hover {
    color: var(--zen-cloud);
    background: rgba(255, 255, 255, 0.04);

    svg { opacity: 0.9; }
  }

  &.active {
    color: var(--zen-gold);
    background: rgba(197, 165, 90, 0.08);
    border: 1px solid rgba(197, 165, 90, 0.15);

    svg {
      opacity: 1;
      stroke: var(--zen-gold);
    }
  }
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 16px;
  margin-top: 16px;

  .visitor-link {
    color: var(--zen-jade-light);
  }

  .logout {
    color: rgba(232, 93, 93, 0.7);

    &:hover {
      color: #e85d5d;
      background: rgba(232, 93, 93, 0.08);
    }
  }
}

/* === 主内容 === */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 32px;
  background:
    radial-gradient(ellipse 60% 40% at 80% 10%, rgba(197, 165, 90, 0.03), transparent),
    radial-gradient(ellipse 40% 60% at 20% 80%, rgba(91, 140, 111, 0.03), transparent),
    #0d0d1a;
}

/* === 页面过渡 === */
.page-enter-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.page-leave-active {
  transition: all 0.2s ease-in;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@keyframes breathe {
  0%, 100% { opacity: 0.7; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
}
</style>
