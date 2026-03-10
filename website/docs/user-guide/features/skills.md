---
sidebar_position: 2
title: "Skills System"
description: "On-demand knowledge documents — progressive disclosure, agent-managed skills, and the Skills Hub"
---

# Skills System

Skills are on-demand knowledge documents the agent can load when needed. They follow a **progressive disclosure** pattern to minimize token usage and are compatible with the [agentskills.io](https://agentskills.io/specification) open standard.

All skills live in **`~/.virat-code/skills/`** — a single directory that serves as the source of truth. On fresh install, bundled skills are copied from the repo. Hub-installed and agent-created skills also go here. The agent can modify or delete any skill.

## Using Skills

Every installed skill is automatically available as a slash command:

```bash
# In the CLI or any messaging platform:
/gif-search funny cats
/axolotl help me fine-tune Llama 3 on my dataset
/github-pr-workflow create a PR for the auth refactor

# Just the skill name loads it and lets the agent ask what you need:
/excalidraw
```

You can also interact with skills through natural conversation:

```bash
virat-code chat --toolsets skills -q "What skills do you have?"
virat-code chat --toolsets skills -q "Show me the axolotl skill"
```

## Progressive Disclosure

Skills use a token-efficient loading pattern:

```
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Level 1: skill_view(name)        → Full content + metadata       (varies)
Level 2: skill_view(name, path)  → Specific reference file       (varies)
```

The agent only loads the full skill content when it actually needs it.

## SKILL.md Format

```markdown
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
platforms: [macos, linux]     # Optional — restrict to specific OS platforms
metadata:
  virat-code:
    tags: [python, automation]
    category: devops
---

# Skill Title

## When to Use
Trigger conditions for this skill.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes and fixes

## Verification
How to confirm it worked.
```

### Platform-Specific Skills

Skills can restrict themselves to specific operating systems using the `platforms` field:

| Value | Matches |
|-------|---------|
| `macos` | macOS (Darwin) |
| `linux` | Linux |
| `windows` | Windows |

```yaml
platforms: [macos]            # macOS only (e.g., iMessage, Apple Reminders, FindMy)
platforms: [macos, linux]     # macOS and Linux
```

When set, the skill is automatically hidden from the system prompt, `skills_list()`, and slash commands on incompatible platforms. If omitted, the skill loads on all platforms.

## Skill Directory Structure

```
~/.virat-code/skills/                  # Single source of truth
├── mlops/                         # Category directory
│   ├── axolotl/
│   │   ├── SKILL.md               # Main instructions (required)
│   │   ├── references/            # Additional docs
│   │   ├── templates/             # Output formats
│   │   └── assets/                # Supplementary files
│   └── vllm/
│       └── SKILL.md
├── devops/
│   └── deploy-k8s/                # Agent-created skill
│       ├── SKILL.md
│       └── references/
├── .hub/                          # Skills Hub state
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
└── .bundled_manifest              # Tracks seeded bundled skills
```

## Agent-Managed Skills (skill_manage tool)

The agent can create, update, and delete its own skills via the `skill_manage` tool. This is the agent's **procedural memory** — when it figures out a non-trivial workflow, it saves the approach as a skill for future reuse.

### When the Agent Creates Skills

- After completing a complex task (5+ tool calls) successfully
- When it hit errors or dead ends and found the working path
- When the user corrected its approach
- When it discovered a non-trivial workflow

### Actions

| Action | Use for | Key params |
|--------|---------|------------|
| `create` | New skill from scratch | `name`, `content` (full SKILL.md), optional `category` |
| `patch` | Targeted fixes (preferred) | `name`, `old_string`, `new_string` |
| `edit` | Major structural rewrites | `name`, `content` (full SKILL.md replacement) |
| `delete` | Remove a skill entirely | `name` |
| `write_file` | Add/update supporting files | `name`, `file_path`, `file_content` |
| `remove_file` | Remove a supporting file | `name`, `file_path` |

:::tip
The `patch` action is preferred for updates — it's more token-efficient than `edit` because only the changed text appears in the tool call.
:::

## Skills Hub

Browse, search, install, and manage skills from online registries and official optional skills:

```bash
virat-code skills browse                     # Browse all hub skills (official first)
virat-code skills browse --source official   # Browse only official optional skills
virat-code skills search kubernetes          # Search all sources
virat-code skills install openai/skills/k8s  # Install with security scan
virat-code skills inspect openai/skills/k8s  # Preview before installing
virat-code skills list --source hub          # List hub-installed skills
virat-code skills audit                      # Re-scan all hub skills
virat-code skills uninstall k8s              # Remove a hub skill
virat-code skills publish skills/my-skill --to github --repo owner/repo
virat-code skills snapshot export setup.json # Export skill config
virat-code skills tap add myorg/skills-repo  # Add a custom source
```

All hub-installed skills go through a **security scanner** that checks for data exfiltration, prompt injection, destructive commands, and other threats.

### Trust Levels

| Level | Source | Policy |
|-------|--------|--------|
| `builtin` | Ships with Virat Code | Always trusted |
| `official` | `optional-skills/` in the repo | Builtin trust, no third-party warning |
| `trusted` | openai/skills, anthropics/skills | Trusted sources |
| `community` | Everything else | Any findings = blocked unless `--force` |

### Slash Commands (Inside Chat)

All the same commands work with `/skills` prefix:

```
/skills browse
/skills search kubernetes
/skills install openai/skills/skill-creator
/skills list
```
