# SSL 证书

管理后台域名：`admin.hetou.vip`

将以下两个文件放在本目录（**不要提交到 Git**）：

| 文件 | 说明 |
|------|------|
| `admin.hetou.vip.pem` | 证书（或完整链） |
| `admin.hetou.vip.key` | 私钥 |

## 从主站复制通配符证书

若已有 `*.hetou.vip` 通配符证书（与 `private_chef_server/nginx/ssl/` 相同），在服务器上执行：

```bash
cd ~/private_chef_admin/nginx/ssl
cp ~/private_chef_server/nginx/ssl/chef.hetou.vip.pem admin.hetou.vip.pem
cp ~/private_chef_server/nginx/ssl/chef.hetou.vip.key admin.hetou.vip.key
```

证书文件名须与 `nginx/conf.d/pg.conf` / `my.conf` 中配置一致。

## 访问方式

| 协议 | 地址 |
|------|------|
| HTTP | `http://admin.hetou.vip:6443` |
| HTTPS | `https://admin.hetou.vip:6444` |

若需标准 443 端口，将 `docker-compose.*.yml` 中 `6444:443` 改为 `443:443`（需确保宿主机 443 未被占用）。
