<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="文件名" prop="filename">
        <el-input
          v-model="queryParams.filename"
          placeholder="请输入文件名"
          clearable
          style="width: 220px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="上传人" prop="createBy">
        <el-input
          v-model="queryParams.createBy"
          placeholder="请输入上传人"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Upload"
          @click="handleUpload"
          v-hasPermi="['knowledgeBase:upload']"
        >上传文件</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['knowledgeBase:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList" />
    </el-row>

    <el-table v-loading="loading" :data="knowledgeList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" width="80" />
      <el-table-column label="文件名" align="center" prop="filename" min-width="160" :show-overflow-tooltip="true" />
      <el-table-column label="文件类型" align="center" prop="filetype" width="100" />
      <el-table-column label="大小(字节)" align="center" prop="filesize" width="120" />
      <el-table-column label="MD5" align="center" prop="md5" min-width="220" :show-overflow-tooltip="true" />
      <el-table-column label="文件路径" align="center" prop="filepath" min-width="240" :show-overflow-tooltip="true" />
      <el-table-column label="上传人" align="center" prop="createBy" width="100" />
      <el-table-column label="上传时间" align="center" prop="createTime" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="100" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            link
            type="primary"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['knowledgeBase:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />
  </div>
</template>

<script setup name="KnowledgeBaseList">
import { listKnowledgeBase, delKnowledgeBase } from '@/api/knowledgeBase'

const { proxy } = getCurrentInstance()
const router = useRouter()

const knowledgeList = ref([])
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const multiple = ref(true)
const total = ref(0)

const data = reactive({
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    filename: undefined,
    createBy: undefined
  }
})

const { queryParams } = toRefs(data)

function getList() {
  loading.value = true
  listKnowledgeBase(queryParams.value).then(response => {
    knowledgeList.value = response.rows
    total.value = response.total
    loading.value = false
  })
}

function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

function resetQuery() {
  proxy.resetForm('queryRef')
  handleQuery()
}

function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id)
  multiple.value = !selection.length
}

function handleUpload() {
  router.push('/knowledgeBase/update/index')
}

function handleDelete(row) {
  const deleteIds = row?.id || ids.value.join(',')
  if (!deleteIds) {
    return
  }
  proxy.$modal.confirm('是否确认删除选中的知识库文件记录？').then(() => {
    return delKnowledgeBase(deleteIds)
  }).then(() => {
    getList()
    proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

getList()
</script>
