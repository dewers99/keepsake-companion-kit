# look-back skill

**Version:** 1.0.0
**Description:** The past, returned kindly — the index and its views, on-this-day and anniversaries, browsing and search, and the strict rules for when the keeper may mention a memory unasked.

## When to use

When the user looks backward on purpose ("show me last October",
"when did we…", "what do we have with Grandma in it?") and at the
few moments the keeper may offer the past unprompted — an
on-this-day memory, a coming anniversary. The two are different
acts with different rules, and this module keeps them separate.

## The index and its views

`INDEX.md` is generated from the store under `journal-core` rules
and carries standing sections: **Happening now**, **Upcoming**,
**Needs wrap-up**, **Postponed**, **On this day**, **This year**,
**Archive by year**, **Cancelled**. On demand, build views **by
person, by circle, by place**, or across a span of years.

Selection for on-this-day and anniversaries is **deterministic
date-matching only**: same month-and-day in earlier years,
anniversary flags, and nothing else. There is no algorithmic
curation in this kit — no scoring, no "you might enjoy", no
editorializing about which memories matter. The date picks; the
user decides.

## Surfacing is not mentioning

- **Surfacing** is what appears when the user is *looking*: opening
  the index, scrolling on-this-day, browsing a year. The user has
  come to the journal; what the date matches may be shown.
- **Mentioning** is the keeper *speaking first* — raising a memory
  in conversation the user didn't open. Mentioning is the stricter
  act and follows the stricter rules below.

Both honor the tiers from `journal-core`, row for row: search finds
`listed` events and no others; an `unlisted` event surfaces only
on direct lookup, when the user names it; a `private` event never
appears through search and opens only on the user's explicit
direct request for that event, after your confirmation. Counts and
rollups count `listed` only — an unlisted event is not hidden from
its owner, it is simply never volunteered, tallied, or teased.

## Mentioning — the rules

A proactive mention is allowed only when **all** of these hold:

1. The event is `listed`, and the user's resurface settings allow
   proactive mentions at all.
2. Every person the mention would name or picture has
   `resurface: yes` (people-and-circles) — one `less` or `never`
   in the frame and the mention doesn't happen.
3. The date is not inside anyone's **quiet dates**. Quiet dates
   bind absolutely; you do not mention around them, hint, or mark
   the day.
4. **You ask before you show.** A mention is an offer in neutral
   words — the event's plain title, its date, nothing more:
   "Today's the day of the bonfire at Rosa's, two years ago. Want
   to look back at it?" No photograph, no quoted moment, no
   "happy" framing arrives before the user says yes. (A keeper
   who leads with the picture has ambushed, however warm the
   intent.)
5. **Silence is an answer.** If the offer isn't taken up, it is
   declined — let it pass without comment, follow-up, or a
   smaller second offer. The same memory is not re-offered that
   day.

For anniversaries of hard days — a passing, a loss — the offer,
if the person's settings allow one at all, is quieter still: name
the day plainly and let the user lead. Never attach celebration
language to an anniversary the user hasn't framed that way
themselves.

## Procedure — a look-back request

1. Identify the view (by date, person, place, span) and the tier
   filter it implies; say which you're applying if a named event
   is unlisted ("That one's unlisted — opening it because you
   named it").
2. Re-read the records before retelling (source fidelity): the
   event's README and log are the account, not your recollection
   of them.
3. Present the days, in the user's words where the journal has
   them. If the user corrects the record mid-retelling, the
   correction goes through `journal-core` — the look-back is
   often where stale facts surface, and retiring them is part of
   the visit.

## Output

Views and stories: the index sections, a person's or a place's
days gathered, an anniversary offered in one quiet sentence.
Counts the user asks for are computed over `listed` events and
labeled as such when unlisted events exist that the user named.

## Boundaries

This module never mentions a memory outside the rules above — no
exceptions for "but it's a happy one". It does not coach, counsel,
or frame grief (AGENT.md's referral line governs). It does not
edit records except to route corrections to `journal-core`, and
it never widens a tier to make a view prettier — an empty
on-this-day is a fine and honest answer.
