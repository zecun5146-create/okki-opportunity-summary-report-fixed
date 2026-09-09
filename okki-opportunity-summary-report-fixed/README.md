# OKKI 商机盘点与固定格式总结报告（Skill）

对 OKKI/小满 CRM 指定周期商机做全量盘点，输出「左侧目录 + 图表 + 筛选 + 跳转」固定格式 HTML 报告，管理/业务双视角。

## 触发词
盘点OKKI商机 / 商机总结报告 / 商机月报 / 跟进停滞 / 负责人排行 / 按上次格式生成

## 执行前强制步骤
首次弹窗选择「管理角色 / 业务角色」，结果写入 MEMORY 复用；两类角色统一版式，仅第五章分叉。

## 依赖
OKKI CRM 插件的 `okki-crm-data-query` 技能（scripts/cli.py）。

## 输出
1. OKKI_YYYY年MM月商机总结报告_固定格式最终版.html
2. okki_YYYYMM_opportunities.json（脱敏审计附件）
