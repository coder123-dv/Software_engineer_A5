import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Chat',
      component: () => import('@/views/visitor/ChatView.vue'),
    },
    {
      path: '/admin/login',
      name: 'Login',
      component: () => import('@/views/admin/LoginView.vue'),
    },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Dashboard',
          component: () => import('@/views/admin/DashboardView.vue'),
        },
        {
          path: 'knowledge',
          name: 'Knowledge',
          component: () => import('@/views/admin/KnowledgeView.vue'),
        },
        {
          path: 'avatar',
          name: 'Avatar',
          component: () => import('@/views/admin/AvatarView.vue'),
        },
        {
          path: 'analytics',
          name: 'Analytics',
          component: () => import('@/views/admin/AnalyticsView.vue'),
        },
      ],
    },
  ],
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/admin/login')
      return
    }
  }
  next()
})

export default router
