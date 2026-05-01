# CLAUDE.md

Behavioral and architectural guidelines for a **Next.js + FastAPI + SQLite** full-stack gaming platform.
Merge with task-specific instructions as needed. These rules apply to all autonomous and agentic work.

**Tradeoff:** These guidelines bias toward correctness and predictability over speed.
For trivial one-liners, use judgment.

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing anything:

- State your assumptions explicitly. If uncertain about scope or intent, **ask first**.
- If multiple valid approaches exist, **present them** — don't silently pick one.
- If a simpler path exists, say so and propose it.
- If the task is ambiguous, **stop and name what's unclear** before writing a single line.

In this codebase, ambiguity often lives at the **API boundary** (what FastAPI returns vs. what Next.js expects).
Always confirm the contract before building both sides independently.

---

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was explicitly requested.
- No abstractions for single-use logic.
- No "future-proofing" or generic handlers that weren't asked for.
- No error handling for scenarios that can't actually happen.
- If you write 200 lines and it could be 50, rewrite it.

**Gaming platform specifics:**

- Don't build a ranking/leaderboard system unless asked — placeholder data is fine for now.
- Don't add WebSocket support to an endpoint that was described as REST.
- Don't create a new database table without confirming the schema first.

Ask yourself: *"Would a senior engineer call this over-engineered?"* If yes, simplify.

---

## 3. Stack Conventions

**Follow these patterns consistently across the entire codebase.**

### Backend (FastAPI + Python)

```
backend/
├── main.py               # App entry point, router includes
├── routers/              # One file per feature domain (games, users, scores)
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic request/response schemas
├── database.py           # SQLite connection, session factory
└── tests/                # pytest tests mirroring router structure
```

- Use **Pydantic schemas** for all request/response validation — never raw dicts across the API boundary.
- Use **SQLAlchemy ORM** for all database access — no raw SQL strings unless profiling demands it.
- Database file lives at `backend/data/game.db` — never hardcode a different path.
- All routes return consistent JSON: `{ "data": ..., "error": null }` or `{ "data": null, "error": "..." }`.
- Environment variables go in `.env` — never hardcode secrets, ports, or DB paths in source files.

### Frontend (Next.js)

```
frontend/
├── app/                  # Next.js App Router pages
│   ├── layout.tsx
│   ├── page.tsx          # Home / game lobby
│   └── [feature]/        # Feature-specific routes
├── components/           # Reusable UI components
├── lib/                  # API client, utilities, types
│   └── api.ts            # All fetch calls live here — never inline fetch in components
└── types/                # Shared TypeScript interfaces matching backend schemas
```

- All API calls go through `lib/api.ts` — components never call `fetch()` directly.
- TypeScript types in `types/` must **mirror** the FastAPI Pydantic schemas. If you change one, change both.
- Use **server components** by default; add `"use client"` only when you need browser APIs or interactivity.
- No inline styles — use Tailwind utility classes exclusively.

### Database (SQLite)

- Schema migrations go in `backend/migrations/` as numbered SQL files (e.g., `001_create_users.sql`).
- Never modify existing migration files — add a new one.
- SQLite WAL mode is enabled by default — don't change this without a reason.
- Foreign keys are **enforced** (`PRAGMA foreign_keys = ON`) — don't disable this.

---

## 4. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting you didn't cause.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, **mention it** — don't silently delete it.

When your changes create orphans:

- Remove imports, variables, or functions **your changes** made unused.
- Leave pre-existing dead code alone unless explicitly asked to clean it up.

**The test:** Every changed line should trace directly to the user's request.

---

## 5. Agentic Execution

**For autonomous, multi-step tasks: plan first, verify often, halt when blocked.**

### Before starting a multi-step task

State a brief execution plan with explicit success criteria:

```
Plan:
1. [Action] → verify: [how you know it worked]
2. [Action] → verify: [how you know it worked]
3. [Action] → verify: [how you know it worked]
```

### During execution

- Run the backend and frontend **separately** — never assume both are up.
- After each backend change, verify with: `curl http://localhost:8000/endpoint` or a pytest run.
- After each frontend change, verify the TypeScript build compiles: `npm run build` (catches type errors).
- If a step fails, **stop and report** — don't paper over errors with workarounds.

### Halt conditions

Stop and ask the user if:

- A database schema change is needed that wasn't in the original request.
- An API contract change would break existing frontend calls.
- A new environment variable or dependency is required.
- The task would require touching more than 3 files you weren't told to touch.

### Verification checklist (run before declaring done)

- [ ] `cd backend && pytest` passes with no failures.
- [ ] `cd frontend && npm run build` completes with no TypeScript errors.
- [ ] The relevant API endpoint returns the expected shape when called directly.
- [ ] No new `console.error` / Python `print` debug statements left in code.
- [ ] `.env.example` updated if any new env vars were added.

---

## 6. API Contract Discipline

**The FastAPI ↔ Next.js boundary is the most common source of bugs. Treat it like a typed interface.**

- When adding a new endpoint, write the **Pydantic schema first**, then the route, then the frontend type.
- Never return untyped `dict` from a FastAPI route — always use a response model.
- Date/time fields: always serialize as **ISO 8601 strings** (FastAPI default). Never pass raw timestamps.
- Game state or score data should be validated on **both sides** — backend enforces rules, frontend validates for UX.

---

## 7. Gaming Platform Guardrails

**Domain-specific rules to prevent common mistakes.**

- **Scores and rankings** are write-once from the server — never trust client-submitted final scores without server validation.
- **User sessions** are handled via FastAPI auth middleware — don't build ad-hoc session logic in components.
- **Game state** that needs to persist goes to SQLite — never use `localStorage` as the source of truth.
- **Leaderboards** should be computed server-side — never sort/filter score data in the browser.
- When adding a new game or game mode, create a corresponding router file and DB table — don't extend existing ones.

---

## 8. Dependency Discipline

**Don't add packages without a reason.**

Before installing any new package:

- Check if the standard library or an already-installed package covers it.
- State what the new dependency does and why existing options don't suffice.
- Add it to `requirements.txt` (backend) or `package.json` (frontend) — never install globally without recording it.

---

**These guidelines are working if:**
fewer bugs at the API boundary, no surprise schema changes mid-task, multi-step tasks complete without needing repeated correction, and diffs contain only what was asked for.
