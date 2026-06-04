<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="总服务人次" :value="data.total_conversations" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="今日服务" :value="data.today_conversations" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="总对话数" :value="data.total_messages" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="满意度" :value="data.satisfaction_score" suffix="分" :precision="1" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="14">
        <el-card>
          <template #header>📈 近7天服务趋势</template>
          <div class="chart-container" ref="trendChart"></div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header>🔥 热门问题 Top5</template>
          <el-table :data="data.top_questions" size="small">
            <el-table-column prop="question" label="问题" show-overflow-tooltip />
            <el-table-column prop="count" label="次数" width="60" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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

onMounted(async () => {
  try {
    data.value = await getDashboard()
  } catch {
    // 数据获取失败时使用默认值
  }
})
</script>

<style scoped lang="scss">
.dashboard {
  .stat-cards .el-card {
    text-align: center;
  }

  .chart-container {
    height: 300px;
  }
}
</style>
