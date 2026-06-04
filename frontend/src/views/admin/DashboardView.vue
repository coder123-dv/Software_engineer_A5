<template>
  <div class="dashboard">
    <!-- 页头 -->
    <header class="page-header">
      <div>
        <h1>数据大屏</h1>
        <p>服务运营实时概览</p>
      </div>
      <div class="header-time">{{ currentTime }}</div>
    </header>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="(stat, idx) in stats" :key="idx" :style="{ animationDelay: `${idx * 0.1}s` }">
        <div class="stat-icon" :style="{ background: stat.color }">
          <span>{{ stat.icon }}</span>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
        <div class="stat-accent" :style="{ background: stat.color }"></div>
      </div>
    </div>

    <!-- 图表行 -->
    <div class="charts-row">
      <!-- 趋势图 -->
      <div class="chart-card main-chart">
        <div class="card-header">
          <h3>📈 近7天服务趋势</h3>
        </div>
        <div class="chart-body">
          <div class="mini-chart">
            <div
              v-for="(day, idx) in data.daily_trend"
              :key="idx"
              class="chart-bar"
              :style="{
                height: `${Math.max(10, (day.count / maxTrend) * 100)}%`,
                animationDelay: `${0.6 + idx * 0.08}s`
              }"
            >
              <span class="bar-value">{{ day.count }}</span>
              <span class="bar-label">{{ day.date.slice(5) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 热门问答 -->
      <div class="chart-card side-card">
        <div class="card-header">
          <h3>🔥 热门问题</h3>
        </div>
        <div class="questions-list">
          <div v-for="(q, idx) in data.top_questions.slice(0, 5)" :key="idx" class="question-item">
            <span class="q-rank">{{ idx + 1 }}</span>
            <span class="q-text">{{ q.question }}</span>
          </div>
          <div v-if="!data.top_questions.length" class="empty-state">
            暂无数据
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getDashboard, type DashboardData } from '@/api/analytics'

const data = ref<DashboardData>({
  total_conversations: 0,
  total_messages: 0,
  today_conversations: 0,
  avg_sentiment: 0,
  avg_response_time_ms: 0,
  satisfaction_score: 0,
  top_questions: [],
  daily_trend: [],
})

const currentTime = ref('')
let timer: number

const stats = computed(() => [
  { icon: '💬', label: '总服务人次', value: data.value.total_conversations, color: 'rgba(197, 165, 90, 0.15)' },
  { icon: '📅', label: '今日服务', value: data.value.today_conversations, color: 'rgba(91, 140, 111, 0.15)' },
  { icon: '📝', label: '总对话数', value: data.value.total_messages, color: 'rgba(100, 140, 200, 0.15)' },
  { icon: '⭐', label: '满意度', value: `${data.value.satisfaction_score.toFixed(1)}分`, color: 'rgba(200, 130, 90, 0.15)' },
])

const maxTrend = computed(() => {
  const max = Math.max(...data.value.daily_trend.map(d => d.count), 1)
  return max
})

function updateTime() {
  currentTime.value = new Date().toLocaleString('zh-CN', {
    month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit',
  })
}

onMounted(async () => {
  updateTime()
  timer = window.setInterval(updateTime, 1000)

  try {
    data.value = await getDashboard()
  } catch {
    // 使用默认值
  }
})

onUnmounted(() => clearInterval(timer))
</script>

<style scoped lang="scss">
.dashboard {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* === 页头 === */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 28px;

  h1 {
    font-family: var(--font-display);
    font-size: 24px;
    font-weight: 700;
    color: var(--zen-cloud);
  }

  p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
    margin-top: 4px;
  }

  .header-time {
    font-size: 13px;
    color: var(--zen-gold);
    font-family: var(--font-mono);
    opacity: 0.7;
  }
}

/* === 统计卡片 === */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  position: relative;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  overflow: hidden;
  animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
  transition: all 0.3s ease;

  &:hover {
    border-color: rgba(197, 165, 90, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  }

  .stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }

  .stat-info {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .stat-value {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 700;
      color: var(--zen-cloud);
    }

    .stat-label {
      font-size: 12px;
      color: rgba(255, 255, 255, 0.4);
    }
  }

  .stat-accent {
    position: absolute;
    top: -50%;
    right: -20%;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.3;
  }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* === 图表行 === */
.charts-row {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 16px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  overflow: hidden;
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;

  .card-header {
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);

    h3 {
      font-size: 14px;
      font-weight: 600;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

/* === 柱状图 === */
.chart-body {
  padding: 24px 20px;
  height: 260px;
}

.mini-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 100%;
  gap: 8px;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  position: relative;
  background: linear-gradient(to top, rgba(197, 165, 90, 0.4), rgba(197, 165, 90, 0.1));
  border-radius: 6px 6px 0 0;
  min-height: 10%;
  animation: growUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  transition: background 0.3s;

  &:hover {
    background: linear-gradient(to top, rgba(197, 165, 90, 0.6), rgba(197, 165, 90, 0.2));
  }

  .bar-value {
    position: absolute;
    top: -22px;
    font-size: 11px;
    color: var(--zen-gold);
    font-weight: 600;
  }

  .bar-label {
    position: absolute;
    bottom: -22px;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.4);
    white-space: nowrap;
  }
}

@keyframes growUp {
  from { height: 0 !important; opacity: 0; }
}

/* === 热门问题 === */
.questions-list {
  padding: 16px 20px;
}

.question-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);

  &:last-child { border-bottom: none; }

  .q-rank {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    background: rgba(197, 165, 90, 0.1);
    color: var(--zen-gold);
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .q-text {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
}
</style>
