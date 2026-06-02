import request from '@/utils/request'

export function listAppUser(query) {
  return request({
    url: '/chef/appUser/list',
    method: 'get',
    params: query
  })
}

export function getAppUser(id) {
  return request({
    url: '/chef/appUser/' + id,
    method: 'get'
  })
}

export function updateAppUser(data) {
  return request({
    url: '/chef/appUser',
    method: 'put',
    data
  })
}
