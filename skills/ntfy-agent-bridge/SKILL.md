---
name: ntfy-agent-bridge
description: Delegate tasks to a remote autonomous agent via a private ntfy topic. Use whenever the user says "tell the agent to...", "ask my remote agent to...", "send this to <agent-name>", or when a task should be handed off to an out-of-session agent that has its own tools (email, calendar, drive, telegram, web search, persistent memory, shell). The remote agent polls the ntfy topic and replies out-of-band (Telegram, email, etc.).
---

# ntfy Agent Bridge

Pattern for delegating work from an in-session coding agent (like OpenCode, Claude Code, Cursor) to a **separate, out-of-session agent** you run yourself. Communication is one-way, via a private [ntfy.sh](https://ntfy.sh) topic: the in-session agent publishes an instruction, the remote agent polls the topic and executes autonomously. Results are delivered out-of-band (Telegram bot, email, etc.) — they do **not** come back into the current chat session.

This is useful when:

- You have a personal agent with tools the current session doesn't have (Gmail, Calendar, Telegram, persistent memory, server shell, etc.).
- You want to hand off a long-running or asynchronous task without blocking the current session.
- You want a durable record of the delegated task in your remote agent's own logs/memory.

## Setup (one-time)

1. **Pick a private ntfy topic name** — use enough entropy that it can't be guessed. Example:
   ```bash
   openssl rand -hex 8
   # -> a1b2c3d4e5f6a7b8
   ```
   Prefix it with something memorable so you recognise it in your ntfy client. e.g. `myagent-a1b2c3d4e5f6a7b8`.

2. **Configure your remote agent** to subscribe to that topic (`ntfy subscribe <topic>` or the JSON polling endpoint) and act on messages it receives.

3. **Tell your in-session agent the topic**, either by editing this SKILL.md and setting the constant below, or by exporting an environment variable and letting the agent read it:
   ```bash
   export NTFY_AGENT_TOPIC=myagent-a1b2c3d4e5f6a7b8
   ```

4. **Optional**: self-host ntfy at your own domain instead of using ntfy.sh. Replace `ntfy.sh/<topic>` with `ntfy.yourdomain.com/<topic>` in the examples below.

### Configuration

```
NTFY_HOST=ntfy.sh                  # or your self-hosted instance
NTFY_AGENT_TOPIC=<your-topic-here> # keep secret; treat like an API key
```

## Simple text instructions

```bash
curl -d "YOUR INSTRUCTION HERE" "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"
```

## Sending files / large content (up to 15MB on ntfy.sh)

Use `curl -T` to upload a file or piped content. Add a `Message:` header for the instruction and a `Filename:` header to name the attachment.

```bash
# File + instruction
curl -T /path/to/file.txt \
  -H "Message: Summarize this and email it to me" \
  -H "Filename: context.txt" \
  "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"

# Pipe command output
git log --oneline -50 | curl -T - \
  -H "Message: Write release notes from these commits" \
  -H "Filename: commits.txt" \
  "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"

# Just a file (the remote agent decides what to do with it)
curl -T ./report.md \
  -H "Filename: report.md" \
  "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"
```

## Examples

```bash
curl -d "Send me an email summarizing today's commits on <repo>" "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"
curl -d "Remember that the new API base URL is https://example.com/v2" "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"
curl -d "Send me a Telegram message with tomorrow's weather in <city>" "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"
curl -d "Research <topic> and send me a summary" "${NTFY_HOST:-ntfy.sh}/${NTFY_AGENT_TOPIC}"
```

## When to use this

- The user says any of: "tell the agent to...", "ask my remote agent to...", "have it remember...", "send this to <your-agent-name>".
- A task would benefit from the remote agent's tools (Gmail, Calendar, Drive, Telegram, web search, persistent memory, shell, etc.) rather than the current in-session tools.
- You need to hand off data or context (a file, a diff, command output) that should be stored or acted on outside this session.
- The task is long-running and shouldn't block the current chat.

## Important notes

- The remote agent has **no context of the current session**. Include everything it needs in the instruction — repo paths, IDs, prior conversation, whatever matters. Assume it starts from zero every time.
- File/content uploads are capped at **15MB** on public ntfy.sh. Self-hosted instances can raise this.
- Polling cadence depends on the remote agent's implementation; typically ~1 minute. There's no delivery guarantee if the agent is offline for longer than ntfy's message-retention window (default 12h on ntfy.sh).
- Results come back **out-of-band** (Telegram, email, whatever the remote agent is configured for), not into the current chat. Tell the user where to expect the reply.
- The topic URL is a **shared secret** — anyone who knows it can send instructions to your agent. Treat it like an API key: never echo it in logs, PR bodies, screenshots, or committed files. Rotate by generating a new topic name and updating both ends.
- ntfy is unencrypted by default. Don't send secrets, credentials, or private data in the message body unless you're using a self-hosted instance behind TLS + access control.
- After sending, briefly acknowledge to the user that the task was dispatched and remind them where the reply will land.

## Related patterns

- [`ntfy.sh` docs](https://docs.ntfy.sh/publish/) — full publish API (priorities, tags, click actions, attachments).
- Any polling agent framework (LangGraph, custom Python asyncio, home-rolled) can subscribe to an ntfy topic — see [`ntfy subscribe`](https://docs.ntfy.sh/subscribe/cli/) for the CLI or [the HTTP API](https://docs.ntfy.sh/subscribe/api/) for programmatic access.
