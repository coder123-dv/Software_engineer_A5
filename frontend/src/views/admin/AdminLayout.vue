<template>
  <div class="admin-layout">
    <el-container style="height: 100vh">
      <el-aside width="200px">
        <div class="logo">🏛️ 管理后台</div>
        <el-menu :default-active="activeMenu" router>
          <el-menu-item index="/admin">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据大屏</span>
          </el-menu-item>
          <el-menu-item index="/admin/knowledge">
            <el-icon><Document /></el-icon>
            <span>知识库管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/avatar">
            <el-icon><Avatar /></el-icon>
            <span>数字人管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/analytics">
            <el-icon><TrendCharts /></el-icon>
            <span>感受度报告</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header>
          <span>景区导览服务AI数字人 · 管理系统</span>
          <el-button size="small" @click="logout">退出登录</el-button>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { DataAnalysis, Document, Avatar, TrendCharts } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

function logout() {
  localStorage.removeItem('token')
  router.push('/admin/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  height: 100vh;

  .el-aside {
    background: #304156;

    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 16px;
      font-weight: bold;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .el-menu {
      border-right: none;
      background: #304156;

      .el-menu-item {
        color: #bfcbd9;
        &:hover, &.is-active {
          background: #263445;
          color: #409eff;
        }
      }
    }
  }

  .el-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #eee;
    font-weight: 500;
  }

  .el-main {
    background: #f0f2f5;
    padding: 20px;
  }
}
</style>
