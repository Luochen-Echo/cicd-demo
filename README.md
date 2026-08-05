# 手把手学会 GitHub Actions —— CI/CD 实战教程

这是一个**一步一步引导你学会 GitHub Actions 常用操作**的教程。我们会用一个真实的 Python 小项目，从零开始把它接入 CI（持续集成），每一步都能在 GitHub 上看到效果。

> 本仓库本身就是一个可运行的示例：`math_utils` 是一个最小的 Python 数学工具包，配好了 `uv` + `ruff` + `pytest`，以及位于 `.github/workflows/ci.yml` 的 GitHub Actions 流水线。

[![CI](https://github.com/你的用户名/你的仓库名/actions/workflows/ci.yml/badge.svg)](https://github.com/你的用户名/你的仓库名/actions/workflows/ci.yml)

> ⬆️ 上面的徽章是**状态徽章**，教程第 5 步会教你怎么生成真实地址替换它。

---

## 目录

1. [前置准备：环境与仓库](#1-前置准备环境与仓库)
2. [GitHub Actions 核心概念](#2-github-actions-核心概念)
3. [第一个 workflow：跑通测试](#3-第一个-workflow跑通测试)
4. [逐步进阶：lint、矩阵、缓存](#4-逐步进阶lint矩阵缓存)
5. [状态徽章：把 CI 结果贴到 README](#5-状态徽章把-ci-结果贴到-readme)
6. [常见操作与排错](#6-常见操作与排错)

---

## 1. 前置准备：环境与仓库

### 1.1 确认本机工具

这个项目用 `uv` 管理 Python。检查是否已安装：

```bash
uv --version      # 例如 uv 0.11.18
python3 --version # 例如 Python 3.13.x
```

如果还没有 uv，用 Homebrew 安装：

```bash
brew install uv
```

### 1.2 在本地跑通项目

克隆本仓库后（或直接在本地该目录），创建虚拟环境并安装依赖：

```bash
uv sync                      # 创建 .venv 并安装依赖（含 dev 依赖）
uv run ruff check .          # 本地 lint 检查
uv run pytest                # 本地运行测试
```

预期输出：`All checks passed!` 和 `5 passed`。**本地能跑通，是 CI 能跑通的前提。**

### 1.3 登录 GitHub CLI

用 `gh` 命令登录（浏览器授权）：

```bash
gh auth login
```

验证是否登录成功：

```bash
gh auth status
```

### 1.4 创建 GitHub 远程仓库并关联

打开 [github.com/new](https://github.com/new)，创建一个**空的**远程仓库（不要勾选自动生成 README/.gitignore），然后：

```bash
# 仓库名假设叫 cicd-demo，替换成你自己的
git remote add origin git@github.com:<你的用户名>/cicd-demo.git
git push -u origin main
```

> 远程仓库建好后，先把目前已有的 workflow 推上去，让第 3 步直接有东西可看。**这一步之后，每次 push 都会触发 GitHub Actions。**

---

## 2. GitHub Actions 核心概念

GitHub Actions 的核心是放在 `.github/workflows/` 目录下的 YAML 文件，叫 **workflow**。一个 workflow 里最常用的三个层级：

| 概念 | 中文 | 大白话 |
|---|---|---|
| **Workflow** | 工作流 | 一个自动化流程，对应一个 YAML 文件 |
| **Job** | 作业 | 流程里的一个阶段，跑在独立的机器（runner）上 |
| **Step** | 步骤 | Job 里的一小步：跑一条命令或一个现成的 Action |

用这张图记：

```
Workflow (ci.yml)
 ├── Job: lint      → Step 1: checkout → Step 2: 装 uv → Step 3: 跑 ruff
 └── Job: test      → Step 1: checkout → Step 2: 装 Python → Step 3: 跑 pytest
```

几个关键术语：

- **Trigger / 触发事件（`on`）**：什么时候跑。最常见是 `push` 和 `pull_request`。
- **Runner**：跑 workflow 的机器。`ubuntu-latest` 是 GitHub 托管的最常用选择。
- **Action**：一段别人写好的可复用步骤，用 `uses:` 引用。最常用的是 `actions/checkout`（把代码拉下来）和 `actions/setup-xxx`（装环境）。
- **Matrix / 矩阵**：用一个 job 在多个配置下重复跑（比如多个 Python 版本）。
- **Expressions / 表达式**：`${{ ... }}`，在 YAML 里引用上下文，比如 `${{ matrix.python-version }}`。

现在脑子里有了概念，去看第 3 步的实例。

---

## 3. 第一个 workflow：跑通测试

**目标**：写一个最小可用的 workflow，push 后自动运行 pytest。

### 3.1 创建文件

在 `.github/workflows/ci.yml` 写入最简版本：

```yaml
name: CI                    # workflow 的名字，显示在 GitHub 的 Actions 页面

on: push                    # 触发条件：一有 push 就跑

jobs:
  test:                     # 一个名为 test 的 job
    runs-on: ubuntu-latest  # 跑在 Ubuntu 上
    steps:
      - name: 检出代码
        uses: actions/checkout@v4   # 把仓库代码拉取到 runner

      - name: 安装 uv
        uses: astral-sh/setup-uv@v5 # 安装 uv（uv 的官方 action）

      - name: 安装依赖
        run: uv sync                # 与本地一样的安装命令

      - name: 运行测试
        run: uv run pytest
```

### 3.2 push 并观察

```bash
git add .
git commit -m "add first ci workflow"
git push
```

然后打开仓库的 **Actions** 标签页，你会看到一个名为 `CI` 的 workflow 正在运行：

- 点击它 → 点 `test` job → 点每个 step 看日志。
- 勾号（✓）= 通过，红叉（✗）= 失败。

> 关键理解：**GitHub Actions 就是在 GitHub 的云端机器上，把你本地做过的命令再自动跑一遍。**

---

## 4. 逐步进阶：lint、矩阵、缓存

第一个 workflow 能跑了，现在把它升级成我们仓库里的完整版（`.github/workflows/ci.yml`）。每一处新增都解释了原因。

### 4.1 触发条件

```yaml
on:
  push:
    branches: [main]   # 只在 push 到 main 时跑
  pull_request:        # 有 PR 时也跑
  workflow_dispatch:   # 允许在 Actions 页面手动点"Run workflow"
```

- `push: branches: [main]`：限制分支，避免每个人 push 任意分支都触发。
- `pull_request`：PR 合入前自动检查，这是团队协作 CI 的核心用法。
- `workflow_dispatch`：调试神器，没有新提交也能手动触发。

### 4.2 分成两个 job：lint 和 test

把"检查代码风格"和"跑测试"拆开，职责清晰、互不干扰：

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run ruff check .     # 代码风格检查

  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv python install ${{ matrix.python-version }}  # 安装矩阵中指定的 Python 版本
      - run: uv sync
      - run: uv run pytest
```

### 4.3 矩阵（Matrix）：一个 job 跑多版本

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
```

- 含义：`test` job 会在 **3 个 Python 版本**下各跑一遍。
- `${{ matrix.python-version }}` 是表达式，每次取矩阵里的一个值。
- `fail-fast: false`：一个版本失败**不中断**其他版本（默认 true 会停掉）。学习阶段设为 false 能一次看到所有版本的完整结果。

### 4.4 缓存（Cache）

`astral-sh/setup-uv@v5` 默认会缓存 `uv` 的依赖下载缓存，不需要额外配置。想验证缓存生效：第二次运行后，看 step "安装 uv" 的日志里会有一行 `Cache restored`，说明依赖没有重新下载，流水线明显变快。

> 对于其他生态（如 Node），通常用 `actions/cache` 手动配置缓存；uv 的 action 已内置，是它省心的原因之一。

### 4.5 完整版

仓库里的 `.github/workflows/ci.yml` 就是上面全部合起来的版本。改完 push 一次，去 Actions 页面确认：**lint job 1 个 + test job 3 个（3 个 Python 版本）= 4 个绿色勾号。**

---

## 5. 状态徽章：把 CI 结果贴到 README

每次 push 后都想一眼看到 CI 是否通过？用徽章。

### 5.1 获取徽章地址

仓库页面 → **Actions** → 选择你的 workflow（`CI`）→ 点右上角 `⋯` 菜单 → **Create status badge** → 复制 Markdown。

它会生成类似这样的地址：

```markdown
[![CI](https://github.com/<你的用户名>/<你的仓库名>/actions/workflows/ci.yml/badge.svg)](https://github.com/<你的用户名>/<你的仓库名>/actions/workflows/ci.yml)
```

### 5.2 贴到 README 顶部

把本文件开头的徽章链接替换成你复制到的地址，然后 push。之后 README 顶部就会实时显示 CI 的绿/红状态。

---

## 6. 常见操作与排错

### 6.1 查看运行日志

仓库 → **Actions** → 点击失败的运行 → 点 `job` → 点红叉的 step，日志会显示具体错误行。CI 里的报错和本地跑几乎一样，最有效的排查方法往往是**把出错的那条命令在本地原样跑一遍**。

### 6.2 手动触发（workflow_dispatch）

如果 workflow 里写了 `workflow_dispatch`，Actions 页面右上角就有 **Run workflow** 按钮，选分支点运行，不用 push 也能测。调试新 workflow 时非常有用。

### 6.3 失败排查套路

1. 看是哪个 job、哪个 step 红了。
2. 点开 step 日志，找错误堆栈/退出码。
3. 在本地复现该命令，比如 `uv run pytest` 报错就先在本地跑。
4. 修好 → push → 看新一次运行。

### 6.4 常用的 Action 一览

| Action | 用途 |
|---|---|
| `actions/checkout` | 把仓库代码拉取到 runner，几乎所有 workflow 第一步 |
| `astral-sh/setup-uv` | 安装 uv，内置缓存 |
| `actions/setup-python` | 装指定版本的 Python（不用 uv 时的选择） |
| `actions/setup-node` | 装指定版本的 Node.js |
| `actions/upload-artifact` / `download-artifact` | job 之间或流程结束后传产物 |
| `actions/cache` | 手动缓存依赖、构建结果 |

### 6.5 其他常用触发事件

```yaml
on:
  schedule:
    - cron: "0 2 * * *"   # 每天凌晨 2 点定时跑（配合爬虫/定时任务）
  push:
    tags: ["v*"]          # 打 v1.0.0 这样的 tag 时触发（配合发布流程）
  issues:
    types: [opened]       # 有 issue 打开时触发
```

---

## 完成之后

现在你应该能：

- 看懂一个 `.github/workflows/*.yml` 的结构（workflow / job / step / 触发）
- 给自己的项目加一个「push 自动 lint + test」的 CI
- 用矩阵跑多个版本、读懂状态徽章、定位失败的 step

**下一步建议**：把 `on.pull_request` 用起来，练习开分支 → 提 PR → 看 Actions 在 PR 上自动跑检查 → 通过后合并。这是日常开发最标准的 CI 工作流。
