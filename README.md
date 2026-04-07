# OpenClaw System Configuration

This repository contains configuration files and scripts for the OpenClaw AI Agent system.

## Contents

- **TOOL_ROUTING.md** - Tool routing rules for optimal AI tool selection
- **JULES_MONITOR_RULES.md** - Automated Jules task monitoring rules
- **AGENTS.md** - Workspace agent rules and guidelines

## Scripts (Local Only)

The following scripts contain API keys and are NOT committed:

- `supabase/scripts/heartbeat_logger.py`
- `supabase/scripts/comfyui_logger.py`
- `supabase/scripts/jules_controller.py`
- `supabase/scripts/migrate_memory.py`

These scripts read API keys from `~/.openclaw/.env`

## Setup

```bash
# Clone this repo
git clone https://github.com/zoelin0911/openclaw-system.git

# API keys are stored locally in ~/.openclaw/.env
# Format: KEY_NAME=your_key_here
```

## Tools Integrated

| Tool | Purpose |
|------|---------|
| v0 | React code generation |
| Context7 | API documentation search |
| n2-stitch | UI design |
| Jules | Autonomous coding |
| Supabase | Data storage |
| Tavily | Web search |

## License

Private - All rights reserved
