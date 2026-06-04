<template>
  <div class="analytics-view">
    <el-card>
      <template #header>
        <div class="header">
          <span>📊 游客感受度报告</span>
          <el-select v-model="period" size="small" @change="loadReport">
            <el-option label="近7天" :value="7" />
            <el-option label="近30天" :value="30" />
            <el-option label="近90天" :value="90" />
          </el-select>
        </div>
      </template>

      <!-- 情感分布 -->
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="sentiment-card positive">
            <h3>😊 积极</h3>
            <p class="value">{{ (report.positive_ratio * 100).toFixed(1) }}%</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="sentiment-card neutral">
            <h3>😐 中性</h3>
            <p class="value">{{ (report.neutral_ratio * 100).toFixed(1) }}%</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="sentiment-card negative">
            <h3>😞 消极</h3>
            <p class="value">{{ (report.negative_ratio * 100).toFixed(1) }}%</p>
          </div>
        </el-col>
      </el-row>

      <!-- 改进建议 -->
      <div class="suggestions" style="margin-top: 24px">
        <h4>💡 AI改进建议</h4>
        <ul>
          <li v-for="(s, i) in report.suggestions" :key="i">{{ s }}</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getSentimentReport } from '@/api/analytics'

const period = ref(7)
const report = ref({
  positive_ratio: 0,
  neutral_ratio: 0,
  negative_ratio: 0,
  suggestions: [] as string[],
})

async function loadReport() {
  try {
    const data = await getSentimentReport(period.value)
    report.value = data
  } catch {
    // 保持默认值
  }
}

onMounted(loadReport)
</script>

<style scoped lang="scss">
.analytics-view {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .sentiment-card {
    text-align: center;
    padding: 24px;
    border-radius: 8px;

    &.positive { background: #f0f9eb; }
    &.neutral { background: #f4f4f5; }
    &.negative { background: #fef0f0; }

    h3 { font-size: 16px; margin-bottom: 8px; }
    .value { font-size: 28px; font-weight: bold; }
  }

  .suggestions {
    h4 { margin-bottom: 12px; }
    ul { padding-left: 20px; }
    li { margin-bottom: 8px; color: #606266; }
  }
}
</style>
