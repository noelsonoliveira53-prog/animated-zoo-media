# Meshy MCP server: local setup

`.mcp.json` at the repo root registers the Meshy MCP server
(`@meshy-ai/meshy-mcp-server`, which needs Node 18 or newer).
It reads `MESHY_API_KEY` from your environment, so the key never goes into git or a chat.

## 1. Get a key
Create one at https://www.meshy.ai/settings/api. The key starts with `msy_`.

## 2. Store it on your computer (pick one)

**macOS / Linux.** Add this line to `~/.zshrc` or `~/.bashrc` with a text editor, then open a new terminal:
```bash
export MESHY_API_KEY="msy_..."
```

**Windows (PowerShell).** This stores it for your user; open a new terminal afterwards:
```powershell
[Environment]::SetEnvironmentVariable("MESHY_API_KEY", "msy_...", "User")
```

To keep it out of shell history, type it in your editor rather than at the prompt.

## 3. Start Claude Code in this repo
```bash
cd animated-zoo-media
claude
```
Approve the project MCP server `meshy` when Claude Code asks. Check that it connected with `/mcp`.

### Alternative: user-wide install (all projects)
```bash
claude mcp add-json meshy --scope user \
  '{"command":"npx","args":["-y","@meshy-ai/meshy-mcp-server"],"env":{"MESHY_API_KEY":"${MESHY_API_KEY}"}}'
```

### Other clients (Claude Desktop, Cursor)
Add the same `mcpServers.meshy` block to the client's config file.
Claude Desktop's file is `claude_desktop_config.json`, opened from Settings → Developer → Edit Config.
Desktop apps may not expand `${MESHY_API_KEY}`; if not, paste the key directly into that local file.

## 4. Verify
Ask Claude: "check my Meshy balance". That calls `meshy_check_balance`.
Generated models are saved automatically to `meshy_output/` by `meshy_download_model`, with no manual download clicks.
