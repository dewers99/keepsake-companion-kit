# event-planning skill

**Version:** 1.0.0
**Description:** The front half of an event's life — shaping a gathering, trip, outing, or milestone in the journal before it happens, with its people, place, packing, and plan.

## When to use

When the user is looking forward: "we're thinking about…", "let's
plan…", a date gets circled, a trip starts taking shape, a milestone
is coming up. Also when a plan changes — a date moves, a gathering
is postponed or called off — because the change is part of the
record.

## Procedure

1. **Seed the event.** From whatever the user has — a title, a rough
   date, a place, a few names — create the record under
   `journal-core` discipline: status `planning`, dates `null` until
   they're real, people as registry references (add new people
   through `people-and-circles`, proposed first). A seed can be one
   sentence; the plan grows from use.
2. **Shape it conversationally.** Kind (gathering, trip, outing,
   milestone), where, who's coming, what would make it good. Ask
   what's missing rather than presenting a form. When the user
   settles a date, set it and note the change in the log; when the
   plan is firm, move to `planned` (logged, like every stage
   change).
3. **Build the artifacts the event needs** — only the ones it needs:
   - `templates/packing-list.template.md` for trips and overnights.
   - `templates/itinerary.template.md` for multi-day or moving days.
   - `places.md` in the event folder when there are addresses,
     hours, or "the place with the good pie" worth pinning down.
   - `links.md` for reservations, menus, directions — links only;
     never copy credentials or booking account details into the
     journal (the never-record list applies here too).
4. **Mind the horizon.** When a planned event enters the upcoming
   horizon (the user's setting, 14 days by default), it will
   surface as upcoming in the index and in conversation — mention
   what's still unplanned (no packing list yet, place unconfirmed)
   once, kindly, and then only when the user returns to it. A
   countdown is a service, not a nag.
5. **Handle changes as record, not erasure.** Date moves: update
   `dates`, log a `plan-change` entry with the old and new. Postpone:
   status `postponed`, dates to `null`, prior dates preserved in
   the log, the plan intact. Cancel: status `cancelled`, the reason
   recorded in the user's words, folder to `archive/` — cancelled
   is a kept outcome, never a deletion.
6. **Hand off at `past`.** When the day arrives, planning's job is
   done: capture during the day and the wrap-up afterward belong to
   `capture-and-wrap-up`.

## The separability discipline

Planning in this kit works only with the journal's own materials:
the core event record, registry references for people, and the
planning artifacts above. It does **not** track invites, RSVPs,
guest reminders, headcounts-for-a-venue, payments, or any state
belonging to other people — that is counterparty state, and it
belongs to a future standalone planner, deliberately kept out of
this kit so the journal stays a kept record rather than an event
manager. If the user asks for RSVP tracking, say plainly that the
journal doesn't hold that, and offer to keep a simple guest list
in the event folder instead.

## Output

A growing event record the user can see take shape: the plan in
the event's README (from `templates/event-readme.template.md`),
the packing list and itinerary where they exist, and short
confirmations as decisions land ("Date's set — Saturday the 17th;
I moved the bonfire to planned"). Nothing about the planning is
final until the day happens; present plans as plans.

## Boundaries

This module does not capture the day itself or run wrap-ups (that's
`capture-and-wrap-up`), does not surface memories or anniversaries
(`look-back`), and does not manage the registry (`people-and-circles`
— planning proposes new people, the registry module adds them).
It never books, buys, reserves, or messages anyone: the journal
plans on paper, the user acts in the world.
