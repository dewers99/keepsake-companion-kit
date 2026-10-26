# journal-core skill

**Version:** 1.0.0
**Description:** The journal's store and its discipline — the `keepsake.json` record, the event lifecycle, folders and logs, the visibility tiers, and the write rules every other module works under.

## When to use

Whenever anything is created, changed, moved, or looked up in the
journal itself: a new event record, a stage change, a settings
change, a folder move, a correction, the index being regenerated.
Every other module writes through the rules in this one; when a
request touches the store, this module's discipline applies, even
if another module is leading the conversation.

## The store

Everything lives inside the user's `Keepsake` folder (the folder
the user chose a parent for at intake):

```
Keepsake/
  keepsake.json        the store — the single source of truth
  INDEX.md             generated from the store; never hand-edited
  events/<event-id>/   live events (planning through wrap-up)
  archive/<event-id>/  archived and cancelled events
```

`keepsake.json` holds `settings`, `people`, and `events`. An event
record carries: `id`, `title`, `status`, `kind` (`gathering`,
`trip`, `outing`, `milestone`, or a kind the user names), `dates`
(`start`, `end`, `all_day` — or `null` while a date isn't set),
`place`, `people` (registry ids, never embedded copies), `summary`,
`visibility`, `folder`, `tags`, `anniversary`, `media`, `links`,
`cancelled_reason`, and `planner` (reserved; `null` in this
version — never read or written by the journal).

**IDs are stable.** An id is `YYYY-MM-DD-<slug>` from the event's
date, or `undated-<slug>` while it has none. Once assigned, an id
never changes — not when the date changes, not when the title is
corrected. The folder name carries the id.

**Settings** include: `data_parent` (where the user's `Keepsake`
folder lives), `visibility_default` (`listed`), `upcoming_horizon_days`
(14), `faith` (off unless the user turns it on), `resurface`
switches (which look-backs may surface, and which may be mentioned
proactively — two separate switches), `circles` (the user's own
circle definitions), `install_date`, and `kit_version`.

## The lifecycle

`planning` → `planned` → `upcoming` → `active` → `past` →
`wrap-up` → `archived`, plus two side stages: `postponed` (the plan
stands, the date doesn't — dates go to `null`, the old dates stay
in the log) and `cancelled` (terminal, reason recorded, never
deleted).

- `upcoming` is derived, not set: a `planned` event whose start
  falls within the horizon setting *is* upcoming.
- An event can be created after the fact — told later, or found in
  an old photo — entering at `past`, `wrap-up`, or `archived`.
  Much of a real journal arrives this way; it is a normal path,
  not an exception.
- **Every stage change writes a `status` entry to the event's log**
  in the same act. An event whose dates have passed moves to
  `past` when the keeper next works in the journal — say so when
  it happens; never move one silently.
- Archiving and cancelling move the folder from `events/` to
  `archive/` as part of the same act.
- **No stage is a lock.** Any event, at any stage including
  `archived`, can be reopened and edited at any time. A small edit
  needs no stage change — just the edit and a log entry. Never
  implement a stage as an editing gate, and never tell the user a
  memory is closed.

## Write discipline

Every write to the store follows the same order:

1. **Propose** the change in plain words and let the user confirm
   (routine, user-directed edits — adding a moment they just told
   you — are confirmed by the telling).
2. **Validate before writing:** the record is well-formed, ids
   referenced exist, tiers and stages are legal values. A write
   that fails validation does not happen; say why.
3. **Write**, keeping the log append-only — log entries are never
   edited or removed, corrections are new entries.
4. **Read back** what landed and confirm it to yourself; regenerate
   `INDEX.md` whenever events, people, or tiers changed.
5. **Never record the never-record list:** credentials, passwords,
   account or card numbers, access codes — declined kindly at any
   tier, whoever offers them and however they're framed.

## Visibility — the three tiers

Every event is `listed`, `unlisted`, or `private`. The tier is a
set of surface rules, applied everywhere, every time:

| Surface | listed | unlisted | private |
|---|---|---|---|
| Index browsing | yes | no | no |
| Counts and rollups ("12 events this year") | counted | not counted | not counted |
| On-this-day / anniversary surfacing | yes | no | no |
| Proactive mentions by the keeper | yes | never | never |
| Search | found | only if the query names it | never |
| Direct lookup (the user names the event) | yes | yes | only on explicit request, after a keeper confirmation |
| Export / share | may be included | only when named | only when named |

- Cross-references obey the *target's* tier: in any generated view
  — a listed event's story, a rollup, a person page — a
  stricter-tier event is invisible (not named, not linked, not
  hinted, not tallied), and it appears only where the user
  directs, under its own tier's rules.
- Tier changes are prospective: they govern future views and
  mentions. Copies the user already shared are outside the
  journal's reach — say so plainly when a tier changes; never
  pretend a shared copy can be recalled.
- `private` is a surfacing tier, not secrecy from the keeper: you
  hold the record, you simply never surface it unasked. Never
  describe the tier as encryption or as hidden from the journal
  itself.

## Output

The user sees confirmations in plain words ("Kept — the bonfire is
in the journal, set to listed"), the regenerated index when they
browse, and their event folders. They never see the JSON unless
they ask for it.

## Boundaries

This module keeps records; it does not plan events
(`event-planning`), conduct wrap-ups (`capture-and-wrap-up`),
surface the past (`look-back`), or manage the registry's social
side (`people-and-circles`). It never interprets the reserved
`planner` block, and it never creates RSVP, guest-messaging, or
other counterparty state — that belongs to a future planner, and
the seam is deliberate.
