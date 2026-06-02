-- 私厨-C端用户菜单与权限（PostgreSQL）
-- 依赖「私厨管理」目录 menu_id=2100（见 chef_dish_menu.sql），请先执行或确保该目录已存在。

-- 菜单：C 端用户
INSERT INTO sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
) VALUES (
  2111, 'C端用户', 2100, 2, 'appUser', 'chef/appUser/index', 'ChefAppUser', 1, 0, 'C', '0', '0', 'chef:appUser:list', 'user',
  'admin', NOW(), '', NULL, 'C端注册用户管理'
) ON CONFLICT (menu_id) DO NOTHING;

-- 按钮权限
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, create_by, create_time)
VALUES
  (2112, '用户查询', 2111, 1, '#', '', 1, 0, 'F', '0', '0', 'chef:appUser:query', 'admin', NOW()),
  (2113, '用户编辑', 2111, 2, '#', '', 1, 0, 'F', '0', '0', 'chef:appUser:edit', 'admin', NOW())
ON CONFLICT (menu_id) DO NOTHING;

-- 给超级管理员角色（role_id=1）授权
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT 1, m.menu_id FROM sys_menu m WHERE m.menu_id BETWEEN 2111 AND 2113
ON CONFLICT DO NOTHING;
