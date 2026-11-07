# Claude Code Game Studios -- Game Studio Agent Architecture

Indie game development managed through 49 coordinated Claude Code subagents.
Each agent owns a specific domain, enforcing separation of concerns and quality.

## Technology Stack

- **Game**: Grovewatch: Sanctuary Siege, an original tower defense + village builder, in `game/`
- **Engine**: Phaser 3.80.1 (browser, WebGL/Canvas). Not one of the framework's
  Godot/Unity/Unreal presets, so `engine:` in `project.yaml` is intentionally unset
- **Language**: TypeScript 5.6 (strict)
- **Build System**: Vite 5 (`cd game && npm run build`, dev server `npm run dev`)
- **Tests**: Vitest (`cd game && npm test`); headless Playwright checks in `game/scripts/*.mjs`
- **Balance tools**: `npx vite-node scripts/balance.ts [runs] [levelIndex,...]` and friends (see `game/PROGRESS.md`)
- **Assets**: procedural: textures drawn in `game/src/scenes/BootScene.ts`, WebAudio SFX/music in `game/src/systems/`
- **Version Control**: Git with trunk-based development

> **Read `game/PROGRESS.md` first.** It is the design log, backlog and balance notes.
> Code root is `game/src` (data in `src/data`, pure sim in `src/systems`, Phaser scenes in `src/scenes`);
> keep game rules in the renderer-free sims (`BattleSim`, `RaidSim`) so they stay unit-testable.

## Project Structure

@.claude/docs/directory-structure.md

## Engine Version Reference

<!-- ENGINE-REFERENCE-IMPORT: Phaser is not a framework preset, so no
     docs/engine-reference import is loaded. The pinned version is in
     game/package.json (phaser 3.80.1). -->

## Technical Preferences

`project.yaml` at the repo root is the primary config store — engine, specialists,
naming, platform, performance, modes. Skills resolve it via `resolve_config`
(see `.claude/docs/config-resolution.md`).

`.claude/docs/technical-preferences.md` is the **legacy fallback**, read on demand
when a key is absent from `project.yaml`. It is not imported here: before
`/setup-engine` runs it is almost entirely `[TO BE CONFIGURED]` placeholders, and
after it runs `project.yaml` holds the real values.

## Coordination Rules

@.claude/docs/coordination-rules.md

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**
Every task follows: **Question -> Options -> Decision -> Draft -> Approval**

- Agents MUST ask "May I write this to [filepath]?" before using Write/Edit tools
  (exempt: `active.md` appends, agent memory, a subagent's new file at the path
  its orchestrating skill named; see `.claude/rules/agent-memory.md`)
- Agents MUST show drafts or summaries before requesting approval
- Multi-file changes require explicit approval for the full changeset
- No commits without user instruction
- A skipped or dismissed question is not an answer: act on nothing, re-ask in
  plain text and wait
- Started outside this file's folder? Warn first: hooks, deny rules and the
  ask-first mode load only when Claude Code starts here

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for full protocol and examples.

> **First session?** If the project has no engine configured and no game concept,
> run `/start` to begin the guided onboarding flow.

## Coding Standards

@.claude/docs/coding-standards.md

## Context Management

Read `.claude/docs/context-management.md` on demand — it is a reference, not
session context. Two of its conventions are load-bearing and cited by name
elsewhere in the repo, so they are restated here rather than lost:

- **`production/session-state/active.md` is the session checkpoint.** The file is
  the memory, not the conversation. Read it first after any compaction, crash, or
  `/clear`.
- **Helpers in `.claude/scripts/` emit observations, never verdicts.** A script
  that scores or judges will eventually contradict a mode or override it cannot
  see. (Cited by `artifact-check.sh` and `adr-dep-graph.sh`.)
