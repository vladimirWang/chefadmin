-- 私厨-系统文章菜单与权限（PostgreSQL）
-- 执行前请确认 menu_id 不与现有数据冲突，或在「菜单管理」中手动配置等价项。

-- 目录：私厨管理
INSERT INTO sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
) VALUES (
  2100, '私厨管理', 0, 6, 'chef', NULL, '', 1, 0, 'M', '0', '0', '', 'guide',
  'admin', NOW(), '', NULL, '私厨业务菜单'
) ON CONFLICT (menu_id) DO NOTHING;

-- 菜单：系统文章
INSERT INTO sys_menu (
  menu_id, menu_name, parent_id, order_num, path, component, route_name,
  is_frame, is_cache, menu_type, visible, status, perms, icon,
  create_by, create_time, update_by, update_time, remark
) VALUES (
  2101, '系统文章', 2100, 1, 'dish', 'chef/dish/index', 'ChefDish', 1, 0, 'C', '0', '0', 'chef:dish:list', 'documentation',
  'admin', NOW(), '', NULL, '管理员推送系统文章'
) ON CONFLICT (menu_id) DO NOTHING;

-- 按钮权限
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, create_by, create_time)
VALUES
  (2102, '文章查询', 2101, 1, '#', '', 1, 0, 'F', '0', '0', 'chef:dish:query', 'admin', NOW()),
  (2103, '文章发布', 2101, 2, '#', '', 1, 0, 'F', '0', '0', 'chef:dish:add', 'admin', NOW()),
  (2104, '文章编辑', 2101, 3, '#', '', 1, 0, 'F', '0', '0', 'chef:dish:edit', 'admin', NOW()),
  (2105, '文章删除', 2101, 4, '#', '', 1, 0, 'F', '0', '0', 'chef:dish:remove', 'admin', NOW())
ON CONFLICT (menu_id) DO NOTHING;

-- 给超级管理员角色（role_id=1）授权
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT 1, m.menu_id FROM sys_menu m WHERE m.menu_id BETWEEN 2100 AND 2105
ON CONFLICT DO NOTHING;
