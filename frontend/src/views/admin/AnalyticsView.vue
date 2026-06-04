<template>
  <div class="analytics-view">
    <header class="page-header">
      <div>
        <h1>游客感受度报告</h1>
        <p>基于对话情感分析的服务质量评估</p>
      </div>
      <div class="period-select">
        <button
          v-for="p in periods" :key="p.value"
          class="period-btn" :class="{ active: period === p.value }"
          @click="period = p.value; loadReport()"
        >{{ p.label }}</button>
      </div>
    </header>

    <!-- 情感分布 -->
    <div class="sentiment-grid">
      <div class="sentiment-card positive">
        <div class="card-visual">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path class="circle-fg" :stroke-dasharray="`${report.positive_ratio * 100}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          </svg>
          <span class="card-emoji">😊</span>
        </div>
        <div class="card-info">
          <span class="card-value">{{ (report.positive_ratio * 100).toFixed(1) }}%</span>
          <span class="card-label">积极反馈</span>
        </div>
      </div>

      <div class="sentiment-card neutral">
        <div class="card-visual">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path class="circle-fg" :stroke-dasharray="`${report.neutral_ratio * 100}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          </svg>
          <span class="card-emoji">😐</span>
        </div>
        <div class="card-info">
          <span class="card-value">{{ (report.neutral_ratio * 100).toFixed(1) }}%</span>
          <span class="card-label">中性反馈</span>
        </div>
      </div>

      <div class="sentiment-card negative">
        <div class="card-visual">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path class="circle-fg" :stroke-dasharray="`${report.negative_ratio * 100}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          </svg>
          <span class="card-emoji">😞</span>
        </div>
        <div class="card-info">
          <span class="card-value">{{ (report.negative_ratio * 100).toFixed(1) }}%</span>
          <span class="card-label">消极反馈</span>
        </div>
      </div>
    </div>

    <!-- AI 建议 -->
    <div class="suggestions-card">
      <h3>💡 AI 改进建议</h3>
      <div class="suggestions-list">
        <div v-for="(s, i) in report.suggestions" :key="i" class="suggestion-item">
          <span class="suggestion-number">{{ i + 1 }}</span>
          <p>{{ s }}</p>
        </div>
        <div v-if="!report.suggestions.length" class="empty-text">
          暂无数据，有对话记录后将自动生成建议
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSentimentReport } from '@/api/analytics'

const periods = [
  { label: '7天', value: 7 },
  { label: '30天', value: 30 },
  { label: '90天', value: 90 },
]

const period = ref(7)
const report = ref({
  positive_ratio: 0,
  neutral_ratio: 1,
  negative_ratio: 0,
  suggestions: [] as string[],
})

async function loadReport() {
  try { report.value = await getSentimentReport(period.value) }
  catch { /* keep defaults */ }
}

onMounted(loadReport)
</script>

<style scoped lang="scss">
.analytics-view {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 28px;

  h1 { font-family: var(--font-display); font-size: 24px; font-weight: 700; color: var(--zen-cloud); }
  p { font-size: 13px; color: rgba(255, 255, 255, 0.4); margin-top: 4px; }
}

.period-select {
  display: flex;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 3px;
}

.period-btn {
  padding: 6px 16px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  font-family: var(--font-body);
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.25s;

  &.active {
    background: var(--zen-gold);
    color: var(--zen-ink);
    font-weight: 600;
  }

  &:hover:not(.active) {
    color: var(--zen-cloud);
  }
}

/* === 情感卡片 === */
.sentiment-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.sentiment-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 18px;
  padding: 28px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  }

  &.positive { border-color: rgba(91, 140, 111, 0.2); .circle-fg { stroke: var(--zen-jade); } }
  &.neutral { border-color: rgba(197, 165, 90, 0.2); .circle-fg { stroke: var(--zen-gold); } }
  &.negative { border-color: rgba(232, 93, 93, 0.2); .circle-fg { stroke: var(--zen-danger); } }

  .card-visual {
    position: relative;
    width: 72px;
    height: 72px;
    flex-shrink: 0;

    .card-emoji {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
    }
  }

  .circular-chart {
    width: 72px;
    height: 72px;
    transform: rotate(-90deg);

    .circle-bg {
      fill: none;
      stroke: rgba(255, 255, 255, 0.06);
      stroke-width: 3;
    }

    .circle-fg {
      fill: none;
      stroke-width: 3;
      stroke-linecap: round;
      animation: progress 1s ease-out forwards;
    }
  }

  .card-info {
    .card-value {
      display: block;
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 700;
      color: var(--zen-cloud);
    }
    .card-label {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.4);
      margin-top: 4px;
    }
  }
}

@keyframes progress {
  from { stroke-dasharray: 0, 100; }
}

/* === 建议卡 === */
.suggestions-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 18px;
  padding: 24px;

  h3 {
    font-size: 15px;
    font-weight: 600;
    color: var(--zen-gold);
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;

  .suggestion-number {
    width: 24px;
    height: 24px;
    border-radius: 8px;
    background: rgba(197, 165, 90, 0.1);
    color: var(--zen-gold);
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  p {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.5;
  }
}

.empty-text {
  text-align: center;
  padding: 24px;
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
}
</style>
