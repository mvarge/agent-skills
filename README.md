# mvarge/agent-skills

A small collection of [agent skills](https://skills.sh) I've extracted from my own setup and generalised for public use.

## Skills

### [`ntfy-agent-bridge`](skills/ntfy-agent-bridge/)

Delegate tasks from an in-session coding agent (OpenCode, Claude Code, Cursor, etc.) to a **separate, out-of-session agent** you run yourself, via a private [ntfy.sh](https://ntfy.sh) topic. The remote agent polls the topic, executes autonomously, and replies out-of-band (Telegram, email, whatever it's configured for).

Useful if you have a personal agent with tools the current coding session doesn't (Gmail, Calendar, Drive, persistent memory, server shell) and want to hand off work to it without switching contexts.

## Install

Install a specific skill:

```bash
npx skills add mvarge/agent-skills --skill ntfy-agent-bridge
```

Install all skills in this repo:

```bash
npx skills add mvarge/agent-skills
```

Or clone `skills/<name>/SKILL.md` directly into your agent's skills directory (e.g. `~/.agents/skills/`, `~/.claude/skills/`).

## License

[MIT](LICENSE)
