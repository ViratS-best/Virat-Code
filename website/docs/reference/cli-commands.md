---
sidebar_position: 1
title: "CLI Commands Reference"
description: "Comprehensive reference for all Virat-Code CLI commands and slash commands"
---

# CLI Commands Reference

## Terminal Commands

These are commands you run from your shell.

### Core Commands

| Command | Description |
|---------|-------------|
| `Virat-Code` | Start interactive chat (default) |
| `virat-code chat -q "Hello"` | Single query mode (non-interactive) |
| `virat-code chat --continue` / `-c` | Resume the most recent session |
| `virat-code chat -c "my project"` | Resume a session by name (latest in lineage) |
| `virat-code chat --resume <id>` / `-r <id>` | Resume a specific session by ID or title |
| `virat-code chat --model <name>` | Use a specific model |
| `virat-code chat --provider <name>` | Force a provider (`nous`, `openrouter`, `zai`, `kimi-coding`, `minimax`, `minimax-cn`) |
| `virat-code chat --toolsets "web,terminal"` / `-t` | Use specific toolsets |
| `virat-code chat --verbose` | Enable verbose/debug output |
| `virat-code --worktree` / `-w` | Start in an isolated git worktree (for parallel agents) |
| `virat-code --checkpoints` | Enable filesystem checkpoints before destructive file operations |

### Provider & Model Management

| Command | Description |
|---------|-------------|
| `virat-code model` | Switch provider and model interactively |
| `virat-code login` | OAuth login to a provider (use `--provider` to specify) |
| `virat-code logout` | Clear provider authentication |

### Configuration

| Command | Description |
|---------|-------------|
| `Virat-Code setup` | Full setup wizard (provider, terminal, messaging) |
| `Virat-Code config` | View current configuration |
| `Virat-Code config edit` | Open config.yaml in your editor |
| `Virat-Code config set KEY VAL` | Set a specific value |
| `Virat-Code config check` | Check for missing config (useful after updates) |
| `Virat-Code config migrate` | Interactively add missing options |
| `virat-code tools` | Interactive tool configuration per platform |
| `virat-code status` | Show configuration status (including auth) |
| `virat-code doctor` | Diagnose issues |

### Maintenance

| Command | Description |
|---------|-------------|
| `Virat-Code update` | Update to latest version |
| `virat-code uninstall` | Uninstall (can keep configs for later reinstall) |
| `virat-code version` | Show version info |

### Gateway (Messaging + Cron)

| Command | Description |
|---------|-------------|
| `Virat-Code gateway` | Run gateway in foreground |
| `Virat-Code gateway setup` | Configure messaging platforms interactively |
| `Virat-Code gateway install` | Install as system service (Linux/macOS) |
| `Virat-Code gateway start` | Start the service |
| `Virat-Code gateway stop` | Stop the service |
| `Virat-Code gateway restart` | Restart the service |
| `Virat-Code gateway status` | Check service status |
| `Virat-Code gateway uninstall` | Uninstall the system service |
| `Virat-Code whatsapp` | Pair WhatsApp via QR code |

### Skills

| Command | Description |
|---------|-------------|
| `virat-code skills browse` | Browse all available skills with pagination (official first) |
| `virat-code skills search <query>` | Search skill registries |
| `virat-code skills install <identifier>` | Install a skill (with security scan) |
| `virat-code skills inspect <identifier>` | Preview before installing |
| `virat-code skills list` | List installed skills |
| `virat-code skills list --source hub` | List hub-installed skills only |
| `virat-code skills audit` | Re-scan all hub skills |
| `virat-code skills uninstall <name>` | Remove a hub skill |
| `virat-code skills publish <path> --to github --repo owner/repo` | Publish a skill |
| `virat-code skills snapshot export <file>` | Export skill config |
| `virat-code skills snapshot import <file>` | Import from snapshot |
| `virat-code skills tap add <repo>` | Add a custom source |
| `virat-code skills tap remove <repo>` | Remove a source |
| `virat-code skills tap list` | List custom sources |

### Cron & Pairing

| Command | Description |
|---------|-------------|
| `virat-code cron list` | View scheduled jobs |
| `virat-code cron status` | Check if cron scheduler is running |
| `virat-code cron tick` | Manually trigger a cron tick |
| `virat-code pairing list` | View pending + approved users |
| `virat-code pairing approve <platform> <code>` | Approve a pairing code |
| `virat-code pairing revoke <platform> <user_id>` | Remove user access |
| `virat-code pairing clear-pending` | Clear all pending pairing requests |

### Sessions

| Command | Description |
|---------|-------------|
| `virat-code sessions list` | Browse past sessions (shows title, preview, last active) |
| `virat-code sessions rename <id> <title>` | Set or change a session's title |
| `virat-code sessions export <id>` | Export a session |
| `virat-code sessions delete <id>` | Delete a specific session |
| `virat-code sessions prune` | Remove old sessions |
| `virat-code sessions stats` | Show session statistics |

### Insights

| Command | Description |
|---------|-------------|
| `virat-code insights` | Show usage analytics for the last 30 days |
| `virat-code insights --days 7` | Analyze a custom time window |
| `virat-code insights --source telegram` | Filter by platform |

---

## Slash Commands (Inside Chat)

Type `/` in the interactive CLI to see an autocomplete dropdown.

### Navigation & Control

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/quit` | Exit the CLI (aliases: `/exit`, `/q`) |
| `/clear` | Clear screen and reset conversation |
| `/new` | Start a new conversation |
| `/reset` | Reset conversation only (keep screen) |

### Tools & Configuration

| Command | Description |
|---------|-------------|
| `/tools` | List all available tools |
| `/toolsets` | List available toolsets |
| `/model [provider:model]` | Show or change the current model (supports `provider:model` syntax to switch providers) |
| `/provider` | Show available providers with auth status |
| `/config` | Show current configuration |
| `/prompt [text]` | View/set custom system prompt |
| `/personality [name]` | Set a predefined personality |

### Conversation

| Command | Description |
|---------|-------------|
| `/history` | Show conversation history |
| `/retry` | Retry the last message |
| `/undo` | Remove the last user/assistant exchange |
| `/save` | Save the current conversation |
| `/compress` | Manually compress conversation context |
| `/title [name]` | Set or show the current session's title |
| `/usage` | Show token usage for this session |
| `/insights [--days N]` | Show usage insights and analytics (last 30 days) |

#### /compress

Manually triggers context compression on the current conversation. This summarizes middle turns of the conversation while preserving the first 3 and last 4 turns, significantly reducing token count. Useful when:

- The conversation is getting long and you want to reduce costs
- You're approaching the model's context limit
- You want to continue the conversation without starting fresh

Requirements: at least 4 messages in the conversation. The configured model (or `compression.summary_model` from config) is used to generate the summary. After compression, the session continues seamlessly with the compressed history.

Reports the result as: `Compressed: X → Y messages, ~N → ~M tokens`.

:::tip
Compression also happens automatically when approaching context limits (configurable via `compression.threshold` in `config.yaml`). Use `/compress` when you want to trigger it early.
:::

### Media & Input

| Command | Description |
|---------|-------------|
| `/paste` | Check clipboard for an image and attach it (see [Vision & Image Paste](/docs/user-guide/features/vision)) |

### Skills & Scheduling

| Command | Description |
|---------|-------------|
| `/cron` | Manage scheduled tasks |
| `/skills` | Browse, search, install, inspect, or manage skills |
| `/platforms` | Show gateway/messaging platform status |
| `/verbose` | Cycle tool progress: off → new → all → verbose |
| `/<skill-name>` | Invoke any installed skill |

### Gateway-Only Commands

These work in messaging platforms (Telegram, Discord, Slack, WhatsApp) but not the interactive CLI:

| Command | Description |
|---------|-------------|
| `/stop` | Stop the running agent (no follow-up message) |
| `/sethome` | Set this chat as the home channel |
| `/status` | Show session info |
| `/reload-mcp` | Reload MCP servers from config |
| `/rollback` | List filesystem checkpoints for the current directory |
| `/rollback <N>` | Restore files to checkpoint #N |
| `/update` | Update Virat Code to the latest version |

---

## Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Alt+Enter` / `Ctrl+J` | New line (multi-line input) |
| `Alt+V` | Paste image from clipboard (see [Vision & Image Paste](/docs/user-guide/features/vision)) |
| `Ctrl+V` | Paste text + auto-check for clipboard image |
| `Ctrl+C` | Clear input/images, interrupt agent, or exit (contextual) |
| `Ctrl+D` | Exit |
| `Tab` | Autocomplete slash commands |

:::tip
Commands are case-insensitive — `/HELP` works the same as `/help`.
:::

:::info Image paste keybindings
`Alt+V` works in most terminals but **not** in VSCode's integrated terminal (VSCode intercepts Alt+key combos). `Ctrl+V` only triggers an image check when the clipboard also contains text (terminals don't send paste events for image-only clipboard). The `/paste` command is the universal fallback. See the [full compatibility table](/docs/user-guide/features/vision#platform-compatibility).
:::
