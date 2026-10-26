# Installing the Keepsake Companion Kit

The kit is plain text — `AGENT.md`, the `skills/` folders, and
`templates/`. Anything that can read long instructions can run it.
Pick your tool below. Each guide states its honest limits; platforms
change, so when in doubt, check your tool's docs.

Two ways to get the files: (1) download the kit (ZIP) and attach the
files to your AI chat, or (2) give your AI the repo link or folder
and let it fetch the kit:
https://github.com/dewers99/keepsake-companion-kit. Git users:
`git clone https://github.com/dewers99/keepsake-companion-kit`.

**One thing matters more for Keepsake than for most kits: your
journal is files.** The keeper maintains a real journal — a store
file, an index, and one folder per event — in a place *you* choose
(a folder on your computer, a synced drive) inside a folder named
`Keepsake`. So the real install question is whether your AI tool
can read and write files where your journal lives. The matrix
below is the honest summary; the per-platform notes follow it.

| Platform | Persona persists? | Can the keeper save your journal? | Saved as… |
|---|---|---|---|
| Muse AI | Per the platform's own capabilities | Where your Muse setup supports file storage you control | Files in your chosen place |
| ChatGPT (Projects) | Yes, inside the project | Uploads are read-mostly; the keeper gives you updated files to keep | Files you download and store yourself |
| Claude (Projects) | Yes, inside the project | Project files persist with the project | Files in the project |
| Google Gemini (Gems) | The Gem's instructions persist | No general file store for your journal | Text you copy out and keep |
| Microsoft Copilot | No — re-attach each session | No standing file store | Text you copy out and keep |
| Cursor / coding agents | Yes — files in the workspace | Yes — full read/write in the project folder | Real files, in your workspace |
| Any other AI tool | Varies | Varies — ask the companion what it can actually save | Varies |

**The standing rule, on every platform:** the companion never
pretends it saved something it can't. If your tool can't write
files, the keeper says so plainly and hands you the journal's text
— the store, the index, an event's story — as copy-paste blocks to
keep in your own folder. A journal kept honestly by hand beats a
journal an AI only claimed to keep.

---

## Muse AI (recommended)

1. Share the kit's repo/folder link with your Muse AI assistant, or
   paste in `AGENT.md` plus the `skills/` files.
2. Tell it: "Install this companion kit and start intake with me."
3. During intake, choose where your journal lives — the parent
   location for your `Keepsake` folder — somewhere your setup can
   actually reach and keep.

**Honest limits:** The persona persists per the platform's own
capabilities. What your Muse AI can store depends on the version
you're using — check your tool's docs, or just ask your companion
what it can actually keep. The companion will never pretend it
saved something it can't.

## ChatGPT

Use **Projects**: create a project, upload the kit files (`AGENT.md`,
`skills/`, `templates/`) to the project, and start your conversation
there.

**Honest limits:** Project files are largely read-side — ChatGPT
can read what you upload but keeping the journal *updated* usually
means the keeper hands you revised files (the store, the index) to
download and replace yourself. Context has limits too: very long
projects can lose track of earlier details. Keep your journal files
in the project current, and check your tool's docs for current
limits.

## Claude

Use **Projects**: create a project, upload the kit files to the
project, and chat inside it.

**Honest limits:** Project knowledge persists across conversations,
but each conversation still has a context limit — long threads can
drop earlier details. Uploaded files live with the project; whether
the keeper can write new files into it depends on your surface and
plan. Check your tool's docs for the current limits.

## Google Gemini

Use **Gems**: create a Gem, add the kit's instructions (`AGENT.md`
content and the skills), and save it.

**Honest limits:** A Gem keeps its instructions across sessions,
but Gemini offers no general file store for a journal — the keeper
will work from what you paste in and hand you updated journal text
to keep in your own folder. File handling varies by version and
surface (app vs. web). Check your tool's docs — or ask the
companion what it can actually save.

## Microsoft Copilot

Copilot chats don't keep a standing persona — **you'll need to
re-attach the kit each session.** Paste `AGENT.md` plus the skills
you want at the start of the conversation, then go. Keep your
journal folder yourself, and paste in the store and index at the
start of a session so the keeper is working from your real journal,
not a fresh memory.

**Honest limits:** No standing persona, no persistent memory of
your journal between sessions, and no file store. Everything the
keeper "remembers" is what you bring to the session. It works —
the journal just lives with you, and the keeper visits it.

## Cursor / coding agents

Drop the kit files into your project workspace and point the agent
at `AGENT.md`. Because these tools read and write real files, this
is the most durable setup for Keepsake: point the workspace at (or
inside) the place your journal lives, and the keeper maintains the
actual `Keepsake` folder directly.

**Honest limits:** It's file-based, so everything the companion
"remembers" is in the files — which is exactly how Keepsake is
designed to work. Your journal's privacy is your folder's privacy:
keep the workspace somewhere you control.

## Any other AI tool

Paste `AGENT.md` plus the skills you want into the tool's
system/persona prompt, or attach the files to the conversation.
During intake, be explicit about how the journal will be kept:
files the tool can write, or text you'll keep yourself.

**Honest limits:** Capabilities vary widely. Ask the companion,
early, "what can you actually save, and where?" — and believe its
answer only if it can show you the saved file or text. The keeper
will never pretend it saved something it can't.

---

## Updates

The kit never updates itself silently, and never nags.

- First check: **one week after your recorded install date**; then
  weekly (default), monthly, or off — your choice.
- The keeper compares this repo's `VERSION` file against your
  installed version, shows you exactly what changed, and you apply
  an update by re-running the install message with the new version.
- **Calm moments only** — never mid-planning, never during a
  wrap-up, never near a hard memory. A declined check stays
  declined.
- If you installed by giving your AI the repo link and it re-fetches
  every session, you're already current — no check needed.

Your journal is never part of an update: the kit's files change,
your `Keepsake` folder doesn't. Updates never touch your records.

## Feedback

Two weeks after install, at a calm moment, the keeper offers the
kit's anonymous feedback form once — skippable, never nagging, and
a "no thanks" means never ask again. Any time you mention feedback
or suggestions, the keeper shares the link.

Feedback form: https://tally.so/r/Qoooa7
