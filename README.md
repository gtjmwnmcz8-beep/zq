# zq

## 科研 Agent Skills

项目安装了以下六个 Skill，位于 `.agents/skills/<name>/SKILL.md`，保留完整上游目录：

| Skill | 使用场景 |
| --- | --- |
| literature-review | 文献检索策略、筛选、证据综合、引用核验 |
| scientific-writing | 科研写作、来源追踪、署名和稿件一致性检查 |
| scientific-visualization | 科研图表、配色、出版导出和图像元数据检查 |
| experimental-design | 随机化、区组、因子设计和实验规划 |
| scientific-critical-thinking | 偏倚、混杂因素和证据质量评价 |
| statistical-analysis | 检验选择、假设诊断、效应量和统计报告 |

来源：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)，固定 commit `a1043ef544e3a100c28e70a736b6cf32554d0677`。MIT 许可证副本见 [.agents/skills/UPSTREAM-LICENSE.md](.agents/skills/UPSTREAM-LICENSE.md)，逐文件 SHA-256 见 [.agents/skills/UPSTREAM.json](.agents/skills/UPSTREAM.json)。没有安装其他 Skills。

在本项目目录启动新的 Codex 会话，查看 Skill 列表，或显式请求：

- `使用 $literature-review 制定催化剂稳定性文献综述的检索策略。`
- `使用 $experimental-design，为三个温度和两种催化剂制定可复现的因子实验。`
- `使用 $scientific-critical-thinking 评价这项研究的混杂因素和证据局限。`
- `使用 $statistical-analysis 检查合成示例数据的分析假设。`
- `使用 $scientific-visualization 生成含误差说明的科研图表。`
- `使用 $scientific-writing 修改稿件，并保留每项结论的证据来源。`

静态发现条件已验证；当前聊天不会保证动态刷新 Skill 清单。新会话的实际加载仍需按上述方法检查。Skill 中的 `scripts/...`、`references/...`、`assets/...` 路径均以该 Skill 的目录为基准；在项目根目录执行时请使用完整 `.agents/skills/<name>/...` 路径。

### 安装依赖与测试

纯文字指导无需安装 Python 包。完整 Python 工具环境使用 Python 3.12、uv 和已固定版本的依赖文件（包含可选绘图和贝叶斯依赖）：

```bash
# 从项目根目录执行；虚拟环境和缓存放在仓库外
export UV_CACHE_DIR=/tmp/zq-uv-cache
uv venv --python 3.12 /workspace/skill-environments/zq-science
uv pip install --python /workspace/skill-environments/zq-science/bin/python \
  --only-binary :all: -r tools/scientific-skills-requirements.txt
PYTHONDONTWRITEBYTECODE=1 /workspace/skill-environments/zq-science/bin/python tools/validate_scientific_skills.py
PYTHONDONTWRITEBYTECODE=1 /workspace/skill-environments/zq-science/bin/python tools/smoke_scientific_skills.py
```

其他机器可将虚拟环境绝对路径替换为仓库外的可写目录。已存在环境无需重新执行 `uv venv`；直接安装固定依赖即可。依赖文件固定了当前成功解析的全部包版本，但没有提供包文件哈希锁。下载保留 HTTPS 验证，限定 wheel，不执行上游安装脚本。

静态测试核验六个目录、frontmatter、来源哈希、Python 语法和本地 Markdown 文件链接；离线功能测试使用合成数据，验证稿件模板生成、PNG/PDF 导出、可复现随机分组、因子设计、统计输入验证及文献 PDF 渲染。测试输出放在系统临时目录，运行结束自动删除；不会上传实验数据。PDF 测试需要 Pandoc 和 XeLaTeX；Plotly 静态导出另需兼容 Chromium/Chrome。

完整依赖、凭据、域名、审查范围、可选缺失功能及验证结果见 [科研 Skills 安装审查](docs/scientific-skills-review.md)。
