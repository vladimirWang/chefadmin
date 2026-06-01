import request from '@/utils/request'

export function listDish(query) {
  return request({
    url: '/chef/dish/list',
    method: 'get',
    params: query
  })
}

export function getDish(id) {
  return request({
    url: '/chef/dish/' + id,
    method: 'get'
  })
}

export function addDish(data) {
  return request({
    url: '/chef/dish',
    method: 'post',
    data
  })
}

export function updateDish(data) {
  return request({
    url: '/chef/dish',
    method: 'put',
    data
  })
}

export function delDish(ids) {
  return request({
    url: '/chef/dish/' + ids,
    method: 'delete'
  })
}
