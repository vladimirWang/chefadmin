import request from '@/utils/request'

export function listKnowledgeBase(query) {
  return request({
    url: '/knowledgeBase/list',
    method: 'get',
    params: query
  })
}

export function uploadKnowledgeBase(data) {
  return request({
    url: '/knowledgeBase/upload',
    method: 'post',
    data,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function updateKnowledgeBase(data) {
  return request({
    url: '/knowledgeBase/update',
    method: 'post',
    data
  })
}

export function delKnowledgeBase(ids) {
  return request({
    url: '/knowledgeBase/' + ids,
    method: 'delete'
  })
}
