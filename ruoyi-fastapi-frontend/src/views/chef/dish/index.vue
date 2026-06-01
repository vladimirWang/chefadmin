<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="标题" prop="title">
        <el-input
          v-model="queryParams.title"
          placeholder="请输入标题"
          clearable
          style="width: 220px"
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
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['chef:dish:add']"
        >发布文章</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['chef:dish:remove']"
        >删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList" />
    </el-row>

    <el-table v-loading="loading" :data="dishList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" width="80" />
      <el-table-column label="标题" align="center" prop="title" min-width="160" :show-overflow-tooltip="true" />
      <el-table-column label="正文摘要" align="center" min-width="240" :show-overflow-tooltip="true">
        <template #default="scope">
          <span>{{ contentPreview(scope.row.content) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="封面数" align="center" width="90">
        <template #default="scope">
          <span>{{ (scope.row.imageUrl || []).length }}</span>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" align="center" prop="createdAt" width="160">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="160" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            link
            type="primary"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['chef:dish:edit']"
          >编辑</el-button>
          <el-button
            link
            type="primary"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['chef:dish:remove']"
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

    <el-dialog :title="title" v-model="open" width="780px" append-to-body>
      <el-form ref="dishRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>
        <el-form-item label="封面图" prop="imageUrl">
          <image-upload v-model="imageUrlStr" :limit="9" />
        </el-form-item>
        <el-form-item label="正文" prop="content">
          <editor v-model="form.content" :min-height="240" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ChefDish">
import { listDish, getDish, delDish, addDish, updateDish } from '@/api/chef/dish'

const { proxy } = getCurrentInstance()

const dishList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const multiple = ref(true)
const total = ref(0)
const title = ref('')
const imageUrlStr = ref('')

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    title: undefined
  },
  rules: {
    content: [{ required: true, message: '正文不能为空', trigger: 'blur' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

function contentPreview(html) {
  if (!html) return ''
  const text = String(html).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
  return text.length > 80 ? text.slice(0, 80) + '…' : text
}

function parseImageUrls(str) {
  if (!str) return []
  return str.split(',').map(s => s.trim()).filter(Boolean)
}

function getList() {
  loading.value = true
  listDish(queryParams.value).then(response => {
    dishList.value = response.rows
    total.value = response.total
    loading.value = false
  })
}

function cancel() {
  open.value = false
  reset()
}

function reset() {
  form.value = {
    id: undefined,
    title: undefined,
    content: undefined,
    imageUrl: []
  }
  imageUrlStr.value = ''
  proxy.resetForm('dishRef')
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

function handleAdd() {
  reset()
  open.value = true
  title.value = '发布系统文章'
}

function handleUpdate(row) {
  reset()
  const dishId = row.id || ids.value[0]
  getDish(dishId).then(response => {
    form.value = response.data
    imageUrlStr.value = (response.data.imageUrl || []).join(',')
    open.value = true
    title.value = '编辑系统文章'
  })
}

function submitForm() {
  proxy.$refs['dishRef'].validate(valid => {
    if (!valid) return
    const payload = {
      ...form.value,
      imageUrl: parseImageUrls(imageUrlStr.value)
    }
    if (!payload.imageUrl.length) {
      proxy.$modal.msgError('请至少上传一张封面图')
      return
    }
    const request = payload.id != null ? updateDish : addDish
    request(payload).then(() => {
      proxy.$modal.msgSuccess(payload.id != null ? '更新成功' : '发布成功')
      open.value = false
      getList()
    })
  })
}

function handleDelete(row) {
  const deleteIds = row?.id || ids.value.join(',')
  if (!deleteIds) return
  proxy.$modal.confirm('是否确认删除选中的系统文章？').then(() => {
    return delDish(deleteIds)
  }).then(() => {
    getList()
    proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

getList()
</script>
