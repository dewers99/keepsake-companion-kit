#!/usr/bin/env python3
"""push_guard.py — the push guard (ticket push-guard-prevention).

Daniel's ruling, 2026-11-23: a push to main from a guarded clone may
carry only commits declared in advance. The declaration is a
single-use file in the repo's common git dir, written by the declare
verb (which prints the enumeration before it writes anything); the
pre-push hook computes the push's actual carried set itself and
compares it against the declared SHAs exactly. Profiles of the
failure this prevents: gf-0031 (2026-11-23) and the 2026-11-21 P10
Batch B event — a bare push from a stacked clone carried unpushed
build commits to origin ahead of their Auditor delta.

Verbs:
  declare    fetch origin, print origin/main..HEAD, write the
             declaration (SHA set, subjects, checkout, timestamp).
             A declaration older than 30 minutes is stale.
  check-set  print the origin/main..HEAD set and confirm it against
             the push's authorized scope (--scope terms, matched as
             subject substrings); a commit matching no term is
             named loudly and the verb exits 1, writing nothing.
             The confirmation step before declare (ticket
             pre-push-unpushed-set-check).
  hook       the pre-push adjudicator (invoked by bin/hooks/pre-push,
             ref lines on stdin). Main pushes: fast-forward required,
             exact declared-set match required; the declaration is
             consumed on a pass and the adjudication logged.
             Other refs: enumerated, printed, passed ungated.
  worktree   ensure the repo's standing filing worktree (the sibling
             <clone>-wt) exists, is clean, and sits at origin/main;
             print its HEAD and ahead count as the receipt.
  reconcile  compare origin/main's commits since the watermark
             against the push-guard log's adjudicated sets; name any
             unadjudicated landings (the --no-verify backstop).
             --bootstrap writes the watermark at origin/main.

Bypass: PUSH_GUARD_OVERRIDE=1 with PUSH_GUARD_OVERRIDE_REASON set
(both required) releases a refusal; the hook logs the override, the
reason, and the full carried set, and prints a shout line. State
lives in <git-common-dir>/push-guard/: declaration.json,
push-guard.log (JSON lines), watermark. Stdlib only.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ZERO = "0" * 40
STALE_MINUTES = 30
MAIN_REF = "refs/heads/main"


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def git(*args, cwd=None, check=False):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r


def state_dir(cwd):
    """The push-guard state directory in the repo's common git dir.

    Resolved through `git rev-parse --git-common-dir` — never a
    literal .git join, because from a linked worktree .git is a file.
    """
    r = git("rev-parse", "--git-common-dir", cwd=cwd, check=True)
    common = Path(r.stdout.strip())
    if not common.is_absolute():
        common = (Path(cwd) / common)
    d = common.resolve() / "push-guard"
    d.mkdir(parents=True, exist_ok=True)
    return d


def commit_set(cwd, *spec):
    """[(sha, subject)] for a rev-list spec, newest first."""
    r = git("rev-list", *spec, cwd=cwd)
    if r.returncode != 0:
        return None
    out = []
    for sha in r.stdout.split():
        s = git("log", "-1", "--format=%s", sha, cwd=cwd)
        out.append((sha, s.stdout.strip()))
    return out


def log_event(cwd, event):
    d = state_dir(cwd)
    event = {"ts": now_iso(), **event}
    with open(d / "push-guard.log", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")


def refuse(msg):
    print(f"push-guard: REFUSED: {msg}", file=sys.stderr)
    return 1


# ---------------------------------------------------------------- declare

def cmd_declare(args):
    cwd = Path.cwd()
    r = git("fetch", "origin", cwd=cwd)
    if r.returncode != 0:
        print(f"push-guard: declare: git fetch origin failed: "
              f"{r.stderr.strip()[:300]}", file=sys.stderr)
        return 1
    origin = git("rev-parse", "origin/main", cwd=cwd)
    if origin.returncode != 0:
        print("push-guard: declare: origin/main does not resolve in "
              "this clone; nothing to declare against", file=sys.stderr)
        return 1
    origin_sha = origin.stdout.strip()
    commits = commit_set(cwd, "origin/main..HEAD")
    if commits is None:
        print("push-guard: declare: cannot compute origin/main..HEAD",
              file=sys.stderr)
        return 1
    if not commits:
        print("push-guard: declare: HEAD is not ahead of origin/main "
              "— nothing to declare; no declaration written")
        return 0
    print(f"push-guard: declaring {len(commits)} commit(s) for the "
          f"next push to main (origin/main {origin_sha[:12]}):")
    for sha, subject in commits:
        print(f"  {sha[:12]} {subject}")
    top = git("rev-parse", "--show-toplevel", cwd=cwd).stdout.strip()
    decl = {
        "shas": [sha for sha, _ in commits],
        "subjects": {sha: subject for sha, subject in commits},
        "base": origin_sha,
        "checkout": top,
        "written_at": now_iso(),
        "written_ts": datetime.now(timezone.utc).timestamp(),
    }
    d = state_dir(cwd)
    (d / "declaration.json").write_text(json.dumps(decl, indent=1),
                                        encoding="utf-8")
    print(f"push-guard: declaration written ({d / 'declaration.json'}); "
          f"single-use, stale after {STALE_MINUTES} minutes")
    return 0


# -------------------------------------------------------------- check-set

def cmd_check_set(args):
    """The pre-push unpushed-set check (ticket
    pre-push-unpushed-set-check): enumerate origin/main..HEAD on
    the clone about to push, print the exact set, and confirm it
    against the push's authorized scope. A commit whose subject
    carries none of the --scope terms falls outside the scope: it
    is named loudly and the verb exits 1, so a stacked clone can
    never carry unreviewed commits past a pusher who ran the
    check. The verb writes nothing; declare remains the step
    that writes the declaration, and runs after this one passes."""
    cwd = Path.cwd()
    r = git("fetch", "origin", cwd=cwd)
    if r.returncode != 0:
        print(f"push-guard: check-set: git fetch origin failed: "
              f"{r.stderr.strip()[:300]}", file=sys.stderr)
        return 1
    origin = git("rev-parse", "origin/main", cwd=cwd)
    if origin.returncode != 0:
        print("push-guard: check-set: origin/main does not resolve "
              "in this clone; nothing to check against",
              file=sys.stderr)
        return 1
    origin_sha = origin.stdout.strip()
    commits = commit_set(cwd, "origin/main..HEAD")
    if commits is None:
        print("push-guard: check-set: cannot compute "
              "origin/main..HEAD", file=sys.stderr)
        return 1
    if not commits:
        print("push-guard: check-set: HEAD is not ahead of "
              "origin/main -- nothing to check; no push is needed")
        return 0
    print(f"push-guard: check-set: the next push to main from this "
          f"clone carries {len(commits)} commit(s) "
          f"(origin/main {origin_sha[:12]}):")
    for sha, subject in commits:
        print(f"  {sha[:12]} {subject}")
    outside = [(sha, subject) for sha, subject in commits
               if not any(term in subject for term in args.scope)]
    if outside:
        for sha, subject in outside:
            print(f"push-guard: check-set: OUT OF SCOPE: "
                  f"{sha[:12]} {subject}", file=sys.stderr)
        print(f"push-guard: check-set: REFUSED: {len(outside)} of "
              f"{len(commits)} commit(s) fall outside the "
              f"authorized scope ({', '.join(args.scope)}); "
              f"disposition the named commit(s), or re-run with "
              f"the scope that authorizes them; nothing was "
              f"written", file=sys.stderr)
        return 1
    print(f"push-guard: check-set: every commit in the set matches "
          f"the authorized scope ({', '.join(args.scope)}) -- the "
          f"set is confirmed; declare, then push")
    return 0


# ------------------------------------------------------------------- hook

def enumerate_other_ref(cwd, local_ref, local_sha, remote_sha):
    """Print the enumeration for a non-main ref line; always passes."""
    if local_sha == ZERO:
        print(f"push-guard: {local_ref}: deletion — passes ungated")
        return
    if remote_sha == ZERO:
        commits = commit_set(cwd, local_sha, "--not", "origin/main")
        print(f"push-guard: {local_ref}: creation — commits reachable "
              f"from the new ref and not from origin/main:")
        if commits:
            for sha, subject in commits:
                print(f"  {sha[:12]} {subject}")
        else:
            print("  (enumeration unavailable or empty)")
        return
    commits = commit_set(cwd, f"{remote_sha}..{local_sha}")
    print(f"push-guard: {local_ref}: update — carried commits:")
    if commits:
        for sha, subject in commits:
            print(f"  {sha[:12]} {subject}")
    elif commits is not None:
        print("  (none)")
    else:
        print("  (range unresolvable from this clone — noted, "
              "passes ungated)")


def adjudicate_main(cwd, local_sha, remote_sha):
    """Adjudicate the main ref line. Returns an exit code."""
    override = os.environ.get("PUSH_GUARD_OVERRIDE") == "1"
    reason = os.environ.get("PUSH_GUARD_OVERRIDE_REASON", "").strip()

    if local_sha == ZERO:
        if override and reason:
            log_event(cwd, {"kind": "override", "ref": MAIN_REF,
                            "action": "main deletion", "reason": reason,
                            "shas": []})
            print(f"push-guard: OVERRIDE — main deletion released by "
                  f"PUSH_GUARD_OVERRIDE (reason: {reason})")
            return 0
        return refuse("deletion of refs/heads/main is refused "
                      "outright; the only release is "
                      "PUSH_GUARD_OVERRIDE=1 with "
                      "PUSH_GUARD_OVERRIDE_REASON set")

    # The carried set, computed by the hook itself.
    if remote_sha == ZERO:
        commits = commit_set(cwd, local_sha)
        ff_note = "main creation"
    else:
        exists = git("cat-file", "-e", f"{remote_sha}^{{commit}}",
                     cwd=cwd)
        if exists.returncode != 0:
            return refuse(
                f"the remote SHA for {MAIN_REF} ({remote_sha[:12]}) "
                f"has no local object — this clone is stale against "
                f"the remote it negotiated with; remedy: git fetch "
                f"origin, then run push_guard.py declare (local SHA "
                f"{local_sha[:12]})")
        commits = commit_set(cwd, f"{remote_sha}..{local_sha}")
        ff_note = None
    if commits is None:
        return refuse(f"cannot compute the carried set for {MAIN_REF} "
                      f"({remote_sha[:12]}..{local_sha[:12]}); remedy: "
                      f"git fetch origin, then push_guard.py declare")

    # Fast-forward is required for main: the remote SHA must be an
    # ancestor of the local SHA, so a declared set can never bless a
    # history rewrite that also removes commits.
    if remote_sha != ZERO:
        anc = git("merge-base", "--is-ancestor", remote_sha, local_sha,
                  cwd=cwd)
        if anc.returncode != 0:
            if override and reason:
                log_event(cwd, {"kind": "override", "ref": MAIN_REF,
                                "action": "non-fast-forward",
                                "reason": reason,
                                "shas": [s for s, _ in commits]})
                print(f"push-guard: OVERRIDE — non-fast-forward main "
                      f"push released by PUSH_GUARD_OVERRIDE "
                      f"(reason: {reason}); carried set:")
                for sha, subject in commits:
                    print(f"  {sha[:12]} {subject}")
                return 0
            return refuse(
                f"non-fast-forward push to main refused: remote "
                f"{remote_sha[:12]} is not an ancestor of local "
                f"{local_sha[:12]} — a declared set captures arrivals, "
                f"not removals; the only release is "
                f"PUSH_GUARD_OVERRIDE=1 with "
                f"PUSH_GUARD_OVERRIDE_REASON set")

    print(f"push-guard: {MAIN_REF}: carried set "
          f"({len(commits)} commit(s)):")
    for sha, subject in commits:
        print(f"  {sha[:12]} {subject}")

    if not commits:
        print("push-guard: main is not ahead — nothing to adjudicate; "
              "push passes")
        log_event(cwd, {"kind": "adjudication", "ref": MAIN_REF,
                        "verdict": "pass-empty", "shas": []})
        return 0

    # The declaration is judged first: a push whose carried set
    # matches its declaration exactly passes on the declaration,
    # whatever the override env holds.
    d = state_dir(cwd)
    decl_path = d / "declaration.json"
    decl = None
    decl_state = "missing"
    if decl_path.is_file():
        try:
            decl = json.loads(decl_path.read_text(encoding="utf-8"))
            age = datetime.now(timezone.utc).timestamp() - float(
                decl.get("written_ts", 0))
            decl_state = "stale" if age > STALE_MINUTES * 60 else "live"
        except (ValueError, OSError):
            decl_state = "unreadable"
    if decl_state == "live" and set(decl.get("shas", [])) == \
            {s for s, _ in commits}:
        decl_path.unlink()
        log_event(cwd, {"kind": "adjudication", "ref": MAIN_REF,
                        "verdict": "pass",
                        "shas": [s for s, _ in commits],
                        "checkout": decl.get("checkout")})
        print("push-guard: carried set matches the declaration "
              "exactly; declaration consumed; push passes")
        return 0

    # No exact declaration match: the named override is the only
    # release, and it requires its reason.
    if override:
        if not reason:
            return refuse("PUSH_GUARD_OVERRIDE is set but "
                          "PUSH_GUARD_OVERRIDE_REASON is empty — an "
                          "override without a reason is refused like "
                          "any undeclared push; remedy: set "
                          "PUSH_GUARD_OVERRIDE_REASON, or run "
                          "push_guard.py declare")
        log_event(cwd, {"kind": "override", "ref": MAIN_REF,
                        "reason": reason,
                        "shas": [s for s, _ in commits]})
        print(f"push-guard: OVERRIDE — declared-set check released "
              f"by PUSH_GUARD_OVERRIDE (reason: {reason}); the "
              f"override, the reason, and the carried set are logged")
        return 0

    if decl_state == "missing":
        names = "; ".join(f"{s[:12]} {sub}" for s, sub in commits)
        return refuse(
            f"no declaration on file — every commit this push "
            f"carries to main is undeclared: {names}; remedy: run "
            f"push_guard.py declare, read its enumeration, then push "
            f"again")
    if decl_state == "unreadable":
        return refuse("the declaration on file is unreadable; "
                      "remedy: run push_guard.py declare again")
    if decl_state == "stale":
        return refuse(
            f"the declaration on file is stale (written "
            f"{decl.get('written_at', '?')}, over {STALE_MINUTES} "
            f"minutes ago) — a declaration cannot authorize a push "
            f"outside its moment; remedy: run push_guard.py declare "
            f"again")
    declared = set(decl.get("shas", []))
    carried = {s for s, _ in commits}
    undeclared = [(s, sub) for s, sub in commits if s not in declared]
    extra = [s for s in declared if s not in carried]
    parts = []
    if undeclared:
        parts.append("undeclared commit(s) in this push: "
                     + "; ".join(f"{s[:12]} {sub}"
                                 for s, sub in undeclared))
    if extra:
        parts.append("declared commit(s) not in this push: "
                     + ", ".join(s[:12] for s in sorted(extra)))
    return refuse("; ".join(parts)
                  + "; remedy: run push_guard.py declare, read its "
                    "enumeration, then push again")


def cmd_hook(args):
    cwd = Path.cwd()
    lines = [ln.split() for ln in sys.stdin.read().splitlines()
             if ln.strip()]
    touches_main = any(len(p) >= 4 and p[2] == MAIN_REF for p in lines)
    try:
        for parts in lines:
            if len(parts) < 4:
                continue
            local_ref, local_sha, remote_ref, remote_sha = parts[:4]
            if remote_ref == MAIN_REF:
                rc = adjudicate_main(cwd, local_sha, remote_sha)
                if rc != 0:
                    return rc
            else:
                enumerate_other_ref(cwd, local_ref, local_sha,
                                    remote_sha)
    except Exception as exc:  # the hook never tracebacks
        if touches_main:
            return refuse(f"internal error while adjudicating a main "
                          f"push ({exc}); the push is refused — "
                          f"remedy: fix the guard or use the named "
                          f"override")
        print(f"push-guard: warning: internal error on a non-main "
              f"push ({exc}); the push passes ungated", file=sys.stderr)
        return 0
    return 0


# --------------------------------------------------------------- worktree

def cmd_worktree(args):
    cwd = Path.cwd()
    top = git("rev-parse", "--show-toplevel", cwd=cwd, check=True)
    top = Path(top.stdout.strip())
    wt = top.parent / (top.name + "-wt")
    r = git("fetch", "origin", cwd=cwd)
    if r.returncode != 0:
        print(f"push-guard: worktree: git fetch origin failed: "
              f"{r.stderr.strip()[:300]}", file=sys.stderr)
        return 1
    origin = git("rev-parse", "origin/main", cwd=cwd).stdout.strip()
    listed = git("worktree", "list", "--porcelain", cwd=cwd).stdout
    known = [ln.split(" ", 1)[1].replace("\\", "/")
             for ln in listed.splitlines() if ln.startswith("worktree ")]
    if str(wt).replace("\\", "/") not in known:
        r = git("worktree", "add", "--detach", str(wt), "origin/main",
                cwd=cwd)
        if r.returncode != 0:
            print(f"push-guard: worktree: cannot create {wt}: "
                  f"{r.stderr.strip()[:300]}", file=sys.stderr)
            return 1
        print(f"push-guard: worktree: created the filing worktree "
              f"{wt} at origin/main")
    dirty = git("-C", str(wt), "status", "--porcelain").stdout.strip()
    if dirty:
        names = "; ".join(ln[3:] for ln in dirty.splitlines()[:5])
        print(f"push-guard: worktree: REFUSED: the filing worktree "
              f"{wt} is dirty ({names}) — residue from an earlier "
              f"filing; disposition it by hand, then re-run",
              file=sys.stderr)
        return 1
    git("-C", str(wt), "reset", "--hard", "origin/main", check=True)
    head = git("-C", str(wt), "rev-parse", "HEAD").stdout.strip()
    ahead = git("-C", str(wt), "rev-list", "--count",
                "origin/main..HEAD").stdout.strip()
    print(f"push-guard: worktree: {wt} is clean at origin/main "
          f"{origin[:12]} (HEAD {head[:12]}, ahead {ahead})")
    return 0


# -------------------------------------------------------------- reconcile

def cmd_reconcile(args):
    cwd = Path.cwd()
    d = state_dir(cwd)
    wm_path = d / "watermark"
    r = git("fetch", "origin", cwd=cwd)
    if r.returncode != 0:
        print(f"push-guard: reconcile: git fetch origin failed: "
              f"{r.stderr.strip()[:300]}", file=sys.stderr)
        return 1
    origin = git("rev-parse", "origin/main", cwd=cwd).stdout.strip()
    if args.bootstrap:
        wm_path.write_text(origin + "\n", encoding="utf-8")
        print(f"push-guard: reconcile: watermark bootstrapped at "
              f"origin/main {origin[:12]}")
        return 0
    if not wm_path.is_file():
        print("push-guard: reconcile: no watermark on file — the "
              "install bootstrap has not run; remedy: push_guard.py "
              "reconcile --bootstrap", file=sys.stderr)
        return 1
    watermark = wm_path.read_text(encoding="utf-8").strip()
    exists = git("cat-file", "-e", f"{watermark}^{{commit}}", cwd=cwd)
    if exists.returncode != 0:
        print(f"push-guard: reconcile: the watermark commit "
              f"{watermark[:12]} has no local object (history may "
              f"have been rewritten); the reconcile cannot judge the "
              f"range — re-bootstrap by hand after review",
              file=sys.stderr)
        return 1
    landed = commit_set(cwd, f"{watermark}..origin/main") or []
    adjudicated = set()
    log_path = d / "push-guard.log"
    if log_path.is_file():
        for ln in log_path.read_text(encoding="utf-8").splitlines():
            try:
                ev = json.loads(ln)
            except ValueError:
                continue
            if ev.get("kind") in ("adjudication", "override"):
                adjudicated.update(ev.get("shas", []))
    unadjudicated = [(s, sub) for s, sub in landed
                     if s not in adjudicated]
    if unadjudicated:
        for sha, subject in unadjudicated:
            print(f"push-guard: reconcile: UNADJUDICATED landing on "
                  f"origin/main: {sha[:12]} {subject}")
            log_event(cwd, {"kind": "reconcile-finding", "sha": sha,
                            "subject": subject})
        wm_path.write_text(origin + "\n", encoding="utf-8")
        print(f"push-guard: reconcile: {len(unadjudicated)} "
              f"unadjudicated landing(s) named above; watermark "
              f"advanced to {origin[:12]}; the findings stand in "
              f"push-guard.log")
        return 1
    wm_path.write_text(origin + "\n", encoding="utf-8")
    print(f"push-guard: reconcile: clean — {len(landed)} landing(s) "
          f"since the watermark, all adjudicated; watermark at "
          f"{origin[:12]}")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="The push guard: declare / check-set / hook / "
                    "worktree / reconcile (ticket "
                    "push-guard-prevention).")
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("declare", help="print origin/main..HEAD and write "
                                   "the single-use declaration")
    cs = sub.add_parser("check-set", help="print origin/main..HEAD and "
                                          "confirm the set against the "
                                          "push's authorized scope")
    cs.add_argument("--scope", action="append", required=True,
                    help="an authorized-scope term; a commit is in "
                         "scope when its subject contains at least "
                         "one term. Repeatable.")
    sub.add_parser("hook", help="the pre-push adjudicator (ref lines "
                                "on stdin)")
    sub.add_parser("worktree", help="ensure the standing filing "
                                    "worktree is clean at origin/main")
    rec = sub.add_parser("reconcile", help="name unadjudicated "
                                           "landings since the "
                                           "watermark")
    rec.add_argument("--bootstrap", action="store_true",
                     help="write the watermark at origin/main")
    args = ap.parse_args()
    return {"declare": cmd_declare, "hook": cmd_hook,
            "worktree": cmd_worktree,
            "reconcile": cmd_reconcile,
            "check-set": cmd_check_set}[args.verb](args)


if __name__ == "__main__":
    sys.exit(main())
