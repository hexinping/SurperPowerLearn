# SuperPowers 插件学习指南 - 关键点速查

> 本文件是对 SuperPowers 5.0.7 学习资料的关键点提炼，供 Claude 快速理解和遵循。

## 项目概述

本仓库是 SuperPowers 插件的中文学习资料，包含 5 篇文档：
- `01-基础入门.md` — 插件概览、安装、核心理念
- `02-核心Skills详解.md` — 14 个 Skill 的完整功能说明
- `03-开发工作流实战.md` — 端到端工作流演练
- `04-进阶技巧与最佳实践.md` — 子代理协调、模型选择、性能优化
- `05-快速参考卡.md` — 一页速查

## SuperPowers 是什么

SuperPowers 是 Claude Code 的官方开发工作流插件，提供 **14 个 Skill**，覆盖软件开发全生命周期：

```
构思 → 设计 → 计划 → 实现 → 测试 → 调试 → 审查 → 完成
```

## 四大核心理念

1. **TDD（测试驱动开发）** — 没有失败的测试，就没有生产代码
2. **系统化** — 没有根因分析，就没有修复
3. **证据优于声明** — 没有验证证据，就没有完成声明
4. **YAGNI（复杂性最小化）** — 最简单的方案就是最好的方案

## 三条铁律

```
1. 没有失败的测试，就没有生产代码        (TDD)
2. 没有根因调查，就没有修复              (Debugging)
3. 没有验证证据，就没有完成声明           (Verification)
```

## 14 个 Skill 分类

### 刚性 Skill（必须严格遵循）
| Skill | 说明 |
|-------|------|
| `test-driven-development` | RED-GREEN-REFACTOR 循环，铁律不可违反 |
| `systematic-debugging` | 四阶段根因调查流程，不可跳过 |
| `verification-before-completion` | 必须有证据才能声称完成 |

### 柔性 Skill（原则可灵活适配）
| Skill | 说明 |
|-------|------|
| `brainstorming` | 所有创意工作的起点，生成设计文档 |
| `writing-plans` | 设计转化为分步实施计划（2-5分钟/步） |
| `subagent-driven-development` | 子代理逐任务执行（推荐方式） |
| `executing-plans` | 独立会话中执行计划 |
| `using-git-worktrees` | 创建隔离开发环境 |
| `requesting-code-review` | 使用专业代理审查代码 |
| `receiving-code-review` | 技术评估审查建议，逐条处理 |
| `dispatching-parallel-agents` | 3+ 个独立问题并行处理 |
| `finishing-a-development-branch` | 合并/PR/保留/丢弃 四选一 |
| `writing-skills` | 创建自定义 Skill |
| `using-superpowers` | 系统入口和使用指南 |

## 标准开发流程

```
brainstorming → worktree → writing-plans → subagent-driven-dev → verification → finish-branch
    设计          环境          计划             实施               验证           收尾
```

**不可跳过 worktree 和 finish-branch！** 这是之前犯过的错误：直接在 main 分支开发，跳过了 worktree 隔离和 finish-branch 收尾。正确做法：

1. brainstorming 完成后，**必须**用 `using-git-worktrees` 创建特性分支（如 `feature/xxx`）
2. 所有开发在 worktree 中进行，main 保持干净
3. 全部完成后，**必须**用 `finishing-a-development-branch` 选择合并/PR/保留/丢弃

## 关键工作流规则

### TDD 循环
```
RED    → 写失败测试 → 运行确认失败
GREEN  → 写最少代码 → 运行确认通过
REFACTOR → 清理重构 → 确认仍然通过
```

### 调试四阶段
```
Phase 1: 调查 — 读错误、复现、查变更、收集证据
Phase 2: 分析 — 找工作示例、对比差异
Phase 3: 假设 — 单一假设、最小测试、一次一个变量
Phase 4: 修复 — 写失败测试、单一修复、验证
         ⚠️ 3 次修复都失败 → 质疑架构！
```

### 验证门禁
```
IDENTIFY → RUN → READ → VERIFY → CLAIM
```

### 子代理两阶段审查
1. **规格合规审查**（先）— 代码是否符合计划？
2. **代码质量审查**（后）— 代码质量、架构、命名
   - 顺序不可颠倒：先确认"做对了"，再讨论"做好了"

## 模型选择策略

```
简单实现 (1-2 文件)  → haiku  (快、便宜)
集成任务 (多文件)    → sonnet (平衡)
架构/审查           → opus   (最强)
```

## 优先级规则

```
用户指令 (CLAUDE.md) > SuperPowers Skill > 系统默认行为
```

即使只有 1% 的可能性某个 Skill 适用，也必须调用它。

## 文件保存位置

| 文件类型 | 路径 |
|---------|------|
| 设计规格 | `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` |
| 实施计划 | `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` |

## 插件位置

```
C:\Users\CM640\.claude\plugins\cache\claude-plugins-official\superpowers\5.0.7\
```

## Git 提交规范

- 提交日志使用中文编写
