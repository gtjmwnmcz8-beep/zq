# 科研 Skills 安装审查

## 来源与范围

来源 https://github.com/K-Dense-AI/scientific-agent-skills ，固定提交 `a1043ef544e3a100c28e70a736b6cf32554d0677`，2026-10-14 审查。六个 `skills/<name>/SKILL.md` 均实际存在，YAML 可解析、name 与目录匹配，description 为非空字符串且不超过 1024 字符。

复制六个完整目录，共 84 个文件（含 24 个 Python 文件），不包含其他 Skill、上游项目管理依赖或测试框架。来源仓库未修改。上游 MIT License 允许复制，保留版权及免责声明。已检查目录中没有符号链接或额外嵌套许可证；本次审查不构成对 Python 第三方依赖的完整许可证或漏洞审计。

## 依赖与外部访问

| 功能 | Python 包 / 其他依赖 | 密钥与网络 |
| --- | --- | --- |
| 文献指导、离线检索结果格式化 | 标准库；DOI 核验及 AI 绘图用 requests 2.34.2 | 核验：doi.org、api.crossref.org，外部 URL 会重定向到出版商域名 |
| 文献数据库 | API 或浏览器 | eutils.ncbi.nlm.nih.gov、pubmed.ncbi.nlm.nih.gov、export.arxiv.org、arxiv.org、api.biorxiv.org、api.semanticscholar.org、api.openalex.org、scholar.google.com；不同服务认证与限额需按当前文档确认 |
| 稿件本地工具 | Python >=3.11 标准库 | 无密钥，无网络 |
| 图表及元数据 | matplotlib 3.11.2、seaborn 0.13.2、Pillow 12.3.0、pypdf 6.19.0 | 本地工具无密钥、无网络 |
| 可选交互/静态图表 | plotly 7.1.0、kaleido 1.4.0，兼容 Chromium/Chrome | 本地合成图静态导出无需密钥；用户设置的 CDN/地图/MathJax 可能需要额外域名 |
| 实验设计 | numpy 2.5.3、pandas 3.0.6、pydoe 1.5.0，Python >=3.12 | 本地运行无密钥 |
| 批判性思考 | 无 Python 依赖 | 指导无需网络；可选引用资料需要相应文献网站 |
| 统计分析 | scipy 1.18.1、statsmodels 0.15.0、pingouin 0.7.0、numpy、pandas、matplotlib、seaborn | 本地运行无密钥 |
| 可选贝叶斯工具 | pymc 6.3.2、arviz 1.3.0 | 本地运行无密钥；Bambi/CmdStanPy 仅为文档介绍，未安装 |
| PDF | Pandoc、XeLaTeX 及 TeX 包 | 本地合成输入渲染无需密钥 |
| 可选 AI 示意图 | requests；上游自带生成器 | OPENROUTER_API_KEY；openrouter.ai；会发送提示词与图像，可能产生费用，未调用 |
| 可选 Parallel 检索 | parallel-web-tools[cli]==0.9.3，独立工具安装 | PARALLEL_API_KEY 或 Parallel 登录；api.parallel.ai、docs.parallel.ai；需认证，未安装/未调用 |
| 安装及来源获取 | uv、Python；验证工具另用 PyYAML | pypi.org、files.pythonhosted.org、github.com；PR API 需要 api.github.com |

安装前已检查上述依赖。API Key 仅检查变量是否存在，未读取或输出值：当前 OPENROUTER_API_KEY、PARALLEL_API_KEY 均未设置。无需为离线工具提供密钥；可选功能启用时通过安全环境配置提供，不要提交 `.env`，也不要在聊天中填写密钥。

所需网络域名与实际验证访问不同：仅来源 Git 获取和 Python 包安装已成功；未批量访问科研接口，未修改环境网络策略。GitHub API 请求返回 HTTP 403，GitHub CLI 认证检查失败；Git 代理读取成功不能证明 PR API 有权限。

`network-domains.json` 列出这六个目录所有静态 HTTP(S) 文档链接的域名，供按功能配置使用；它包含参考文献网站，不是建议整体加入 allowlist，也不能覆盖用户 URL 重定向或第三方工具动态请求。

## 脚本与指令风险审查

安装前对所有待复制 Python 文件做 AST 解析和导入/调用扫描，并检查涉及网络、进程启动、动态导入、读写、输出覆盖和凭据的代码路径。此为静态审查及有限合成测试，不能证明所有路径安全或科学结论正确。

- 没有执行上游安装脚本。选中目录没有安装入口；没有发现 shell=True、eval、pickle 加载或递归删除。可视化动态导入限定为随附的 `assets/color_palettes.py`，该文件也已纳入审查和哈希记录。
- `generate_schematic*.py` 会从环境或当前/父目录 `.env` 读取 OpenRouter key，通过 HTTPS 向 OpenRouter 发送提示词及迭代图像；可能产生费用。未执行生成或凭据读取路径。不要发送未授权的未发表数据。
- `verify_citations.py` 会发 DOI/Crossref 请求以及对稿件中的任意 URL 发 HEAD 请求并跟随重定向。使用前审查 URL，避免内部地址、敏感链接及不受信任输入。
- PDF 生成调用 Pandoc/XeLaTeX，使用参数列表而非 shell。Markdown、TeX、模板和资源仍需可信；它们能触发资源读取或格式处理风险，不应把生成器当作不可信文档的隔离沙箱。
- 文件生成器向指定路径写入；部分代码拒绝覆盖，部分支持覆盖或替换。只选择专用输出目录。图像/PDF 解析有资源消耗风险，不应仅凭扩展名信任输入。
- 写作 CLIs 只做本地验证；不能自动证实引文、作者贡献或报告结论。科研工具的结果仍需人工方法学审查。
- 上游六个 Skill 均包含“Always cite”其自有论文的指令。本次原样保留以便溯源；它不等于该论文与每项研究都相关，使用时应按实际贡献及目标期刊规范判断，不能让第三方文档覆盖项目/用户要求。

## 引用与 Codex 发现

84 个来源文件保持逐字节一致；24 条相对 Markdown 文件链接存在，Python 文件语法有效。六个入口均位于 Codex 项目级 `.agents/skills/<name>/SKILL.md` 路径。新会话实际发现需用户按 README 验证，未声称当前会话已重新加载。

Markdown 链接检查不意味着所有代码块示例路径适用于新布局：执行 `scripts/...` 时应切换到相应 Skill 目录，或改用项目根目录完整路径。实验设计/统计指南中建议的虚拟环境目录可移到项目外。上游有 Python 3.13 的示例命令，本次在符合最低版本要求的 Python 3.12.14 上测试本地工具。

`scientific-critical-thinking/SKILL.md` 的可选命令 `skills/scientific-schematics/scripts/generate_schematic.py` 指向未选中 Skill，在本项目不存在，不能直接执行。其他对 statistical-power、peer-review、statsmodels、pymc 等 Skill 的提及也仅是外部建议，没有安装这些目录。核心批判性思考、实验设计和本地统计功能不依赖这些额外 Skills。

## 当前实例验证

- 静态检查通过：六个入口、84 个 SHA-256、24 条本地 Markdown 链接、全部 Python 语法。
- 合成离线功能测试通过：写作脚手架、Matplotlib PNG/PDF、24 单位平衡随机化与种子可复现、六组合因子设计、统计缺失值/恒定输入处理、Pandoc/XeLaTeX PDF。
- 所有固定 Python 依赖安装成功，存放在仓库外 `/workspace/skill-environments/zq-science`；虚拟环境及缓存不提交。
- 可选 PyMC/ArviZ/Pingouin 导入通过。Plotly/Kaleido/Chromium 静态导出失败：JavaScript `ReferenceError: kaleido_scopes is not defined`。检查随包 JS 文件存在并禁用 MathJax CDN 后重试仍失败；原因未完全确定，不宣称该导出路径可用，Matplotlib 导出已通过。
- 付费 AI 绘图、认证检索、真实文献搜索、真实实验数据分析未执行。文字指导类 Skill 没有可执行测试，不能从静态检查推断科研评价正确。

提交仅包含 Skills、许可证、溯源、依赖版本、验证脚本及说明，不含实验数据、凭据、虚拟环境或生成图像。PR 创建结果由最终交付报告说明。
