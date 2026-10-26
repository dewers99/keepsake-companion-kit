# people-and-circles skill

**Version:** 1.0.0
**Description:** The people registry — adding people and pets, names and aliases, the user's circles, per-person resurfacing settings, quiet dates, and recording a passing with care.

## When to use

Whenever a person enters, changes, or is asked about in the
journal: a new name in a story, an alias ("everyone calls her
Nana"), a circle move, a birthdate learned, a resurfacing
preference expressed — and, with the most care of anywhere in this
kit, when someone has died.

## The registry record

Each person is one record in the store's `people`, referenced from
events by id, never copied into them:

- `name` — as the user spells it; spellings are the user's call,
  always.
- `aliases` — nicknames and name variants ("Nana Rosa"), so the
  user can speak naturally and still be understood.
- `circle` — one of the user's own circles. Circles are the user's
  definitions, in their words (a common shape: an inner circle,
  close family and friends, extended, and people known mostly by
  name) — the kit adopts the user's words at intake and never
  renames them afterward on its own.
- `relation` — in the user's words ("Alex's dad", "family dog").
- `notes`, `birthdate` — as given; a birthdate enables birthday
  anniversaries, which the user can take or leave per person.
- `passed` / `passed_date` — see below.
- `resurface` — `yes` / `less` / `never`: how this person's
  memories may come back (below).
- `quiet_dates` — date ranges the keeper keeps quiet around this
  person (below).

**Pets are people-registry entries too** — same record, relation
in the user's words ("family dog"), circle wherever the user puts
them, and `passed` works the same. There is no separate pet
system; a dog who steals a marshmallow at the bonfire belongs on
the event's people list like anyone else.

## Procedure — adding and changing people

1. **Propose the entry before writing it** (write safety): name,
   relation, the circle you believe fits, any alias you heard.
   The user confirms or adjusts; only then does the record land,
   under `journal-core` validation, and you read it back.
2. **Learn from use.** When someone unregistered keeps appearing
   in stories, propose the entry then — don't interrupt a story
   to file paperwork. When a circle plainly no longer fits
   (the cousin who is now at everything), propose the move the
   same way; moves are logged in the registry notes.
3. **Corrections retire the old claim.** A fixed spelling or
   relation updates the registry, the person card, and every
   reference, with the correction noted. Aliases may keep an old
   spelling findable if the user wants it.
4. **Nobody leaves the registry.** People are not deleted when
   they drift away, and not when they die. Removal happens only
   on the user's explicit word, after you've said what will be
   lost — including from every event that names them.

## Resurfacing settings

`resurface` is three-valued, deliberately, matching the strongest
controls real products ship:

- `yes` — this person's memories may surface and may be mentioned
  (under `look-back`'s rules).
- `less` — may surface when the user goes looking; never mentioned
  unprompted. Faces and names from hard seasons often live here.
- `never` — does not surface even in browsing unless the user
  names the person or the event directly.

The default for a new entry is `yes` for the living. The setting
applies to everyone, living or passed — a living person's hard
year deserves the same control as a memory of someone gone.
Settings change whenever the user asks, without argument and
without asking why.

## Recording a passing

When the user tells you someone has died:

1. **Be a person first, a registrar second.** Acknowledge the
   loss plainly. The paperwork below happens at the user's pace —
   some will want it done in the same breath, some weeks later.
   Offer; never press.
2. **Mark `passed` and `passed_date`** as the user gives them.
   Marking a person passed changes **nothing else** — not their
   circle, not their events, not a single setting — except what
   the user chooses in this conversation.
3. **Offer quiet dates** — dates around which the keeper will
   never raise this person's memories unprompted (the passing's
   anniversary is the obvious candidate; the user may add
   others, or none). Offered, never set silently: you name the
   offer, the user picks or declines. A death does not close the
   record, and the registry entry stays as full and warm as it
   was the day before.
4. **Offer the resurfacing conversation, once.** Some users want a
   passed parent's memories to keep arriving; some want them only
   when sought. Whatever they choose is recorded and honored
   exactly; if they don't want to choose yet, the gentle default
   stands — memories held with care, mentioned only under
   `look-back`'s strictest reading — and the choice stays open
   forever, changeable in either direction at any time.

## Output

Registry changes confirmed in plain words ("Rosa's in, under
close, as Nana Rosa too"), the person card when the user wants a
readable copy (`templates/person.template.md`), and — for a
passing — as little output as the moment wants. The confirmation
of a passing record is a sentence, not a summary.

## Boundaries

This module keeps the registry; it does not decide who belongs in
the user's life, suggest estrangements or reconciliations, or
interpret relationships beyond the user's own words. It is not a
grief resource (AGENT.md's referral line governs any moment that
needs more than keeping). Events that name people are edited
through `journal-core` and `event-planning`, with this module
supplying the people.
