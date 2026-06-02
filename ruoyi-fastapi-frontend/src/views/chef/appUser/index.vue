<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="queryParams.email"
          placeholder="请输入邮箱"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList" />
    </el-row>

    <el-table v-loading="loading" :data="userList">
      <el-table-column label="ID" align="center" prop="id" width="80" />
      <el-table-column label="头像" align="center" width="80">
        <template #default="scope">
          <el-avatar v-if="scope.row.avatarUrl" :src="scope.row.avatarUrl" :size="40" />
          <el-avatar v-else :size="40">{{ displayInitial(scope.row) }}</el-avatar>
        </template>
      </el-table-column>
      <el-table-column label="昵称" align="center" min-width="120" :show-overflow-tooltip="true">
        <template #default="scope">
          <span>{{ displayNickname(scope.row) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="邮箱" align="center" prop="email" min-width="200" :show-overflow-tooltip="true" />
      <el-table-column label="发帖数" align="center" prop="postCount" width="90" />
      <el-table-column label="获赞数" align="center" prop="likeCount" width="90" />
      <el-table-column label="操作" align="center" width="100" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            link
            type="primary"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['chef:appUser:edit']"
          >编辑</el-button>
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

    <el-dialog title="编辑 C 端用户" v-model="open" width="520px" append-to-body>
      <el-form ref="userRef" :model="form" :rules="rules" label-width="88px">
        <el-form-item label="用户ID">
          <el-input v-model="form.id" disabled />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" disabled />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称" maxlength="32" show-word-limit />
        </el-form-item>
        <el-form-item label="头像" prop="avatarUrl">
          <image-upload v-model="avatarUrlStr" :limit="1" />
        </el-form-item>
        <el-form-item label="获赞数" prop="likeCount">
          <el-input-number v-model="form.likeCount" :min="0" :max="999999999" controls-position="right" />
        </el-form-item>
        <el-form-item label="发帖数">
          <el-input v-model="form.postCount" disabled />
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

<script setup name="ChefAppUser">
import { listAppUser, getAppUser, updateAppUser } from '@/api/chef/appUser'

const { proxy } = getCurrentInstance()

const userList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const total = ref(0)
const avatarUrlStr = ref('')

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    email: undefined
  },
  rules: {
    likeCount: [{ required: true, message: '获赞数不能为空', trigger: 'blur' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

function displayNickname(row) {
  const name = row.nickname?.trim()
  if (name) return name
  const email = row.email || ''
  if (email.includes('@')) return email.split('@')[0]
  return email || '-'
}

function displayInitial(row) {
  const name = displayNickname(row)
  return name ? name.slice(0, 1).toUpperCase() : '?'
}

function getList() {
  loading.value = true
  listAppUser(queryParams.value).then(response => {
    userList.value = response.rows
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
    email: undefined,
    nickname: undefined,
    avatarUrl: undefined,
    likeCount: 0,
    postCount: 0
  }
  avatarUrlStr.value = ''
  proxy.resetForm('userRef')
}

function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

function resetQuery() {
  proxy.resetForm('queryRef')
  handleQuery()
}

function handleUpdate(row) {
  reset()
  getAppUser(row.id).then(response => {
    form.value = {
      ...response.data,
      likeCount: response.data.likeCount ?? 0,
      postCount: response.data.postCount ?? 0
    }
    avatarUrlStr.value = response.data.avatarUrl || ''
    open.value = true
  })
}

function submitForm() {
  proxy.$refs['userRef'].validate(valid => {
    if (!valid) return
    const payload = {
      id: form.value.id,
      nickname: form.value.nickname?.trim() || null,
      avatarUrl: avatarUrlStr.value?.trim() || null,
      likeCount: form.value.likeCount ?? 0
    }
    updateAppUser(payload).then(() => {
      proxy.$modal.msgSuccess('更新成功')
      open.value = false
      getList()
    })
  })
}

getList()
</script>
