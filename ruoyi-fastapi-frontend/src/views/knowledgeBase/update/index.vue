<template>
  <div class="app-container knowledge-upload">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>上传知识库文件</span>
          <el-button link type="primary" @click="goList">返回列表</el-button>
        </div>
      </template>

      <el-alert
        title="支持 txt、pdf、doc、docx、html 等文本类文件；相同 MD5 的文件不会重复入库。"
        type="info"
        :closable="false"
        show-icon
        class="mb16"
      />

      <el-upload
        ref="uploadRef"
        drag
        :limit="1"
        :auto-upload="false"
        :disabled="uploading"
        :on-change="handleFileChange"
        :on-remove="handleFileRemove"
        accept=".txt,.pdf,.doc,.docx,.html,.htm,.xls,.xlsx,.ppt,.pptx"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">将文件拖到此处，或<em>点击选择</em></div>
        <template #tip>
          <div class="el-upload__tip">一次上传一个文件，提交后写入知识库</div>
        </template>
      </el-upload>

      <div class="actions">
        <el-button type="primary" :loading="uploading" @click="submitUpload" v-hasPermi="['knowledgeBase:upload']">
          提交上传
        </el-button>
        <el-button @click="resetUpload">重置</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup name="KnowledgeBaseUpdate">
import { getToken } from '@/utils/auth'
import { UploadFilled } from '@element-plus/icons-vue'

const { proxy } = getCurrentInstance()
const router = useRouter()

const uploadRef = ref()
const uploading = ref(false)
const selectedFile = ref(null)

function handleFileChange(file) {
  selectedFile.value = file.raw
}

function handleFileRemove() {
  selectedFile.value = null
}

function resetUpload() {
  uploadRef.value?.clearFiles()
  selectedFile.value = null
}

function goList() {
  router.push('/knowledgeBase/list')
}

async function submitUpload() {
  if (!selectedFile.value) {
    proxy.$modal.msgError('请先选择文件')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  uploading.value = true
  try {
    const resp = await fetch(import.meta.env.VITE_APP_BASE_API + '/knowledgeBase/upload', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + getToken()
      },
      body: formData
    })
    const data = await resp.json()
    if (data.code === 200) {
      proxy.$modal.msgSuccess(data.msg || '上传成功')
      resetUpload()
      router.push('/knowledgeBase/list')
    } else {
      proxy.$modal.msgError(data.msg || '上传失败')
    }
  } catch (e) {
    proxy.$modal.msgError('上传失败')
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.knowledge-upload .card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.knowledge-upload .mb16 {
  margin-bottom: 16px;
}

.knowledge-upload .actions {
  margin-top: 20px;
}
</style>
