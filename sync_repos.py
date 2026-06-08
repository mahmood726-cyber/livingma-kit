"""Propagate the livingma-kit shared bundle into every sibling *_LivingMeta repo.

Copies this kit's assets/ and configs/ into each `../*_LivingMeta` repo, only
writing files whose content differs (idempotent). NEVER touches a repo's
unique *_REVIEW.html or any non-shared file.

Usage:
    python sync_repos.py --dry-run     # report what would change
    python sync_repos.py               # write differing files
    python sync_repos.py --only assets # sync just one subtree
"""
from __future__ import annotations
import argparse, filecmp, glob, hashlib, os, shutil, sys

KIT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(KIT)
SUBTREES = ("assets",)


def _md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", choices=SUBTREES)
    args = ap.parse_args()
    subtrees = (args.only,) if args.only else SUBTREES

    repos = sorted(d for d in glob.glob(os.path.join(PARENT, "*LivingMeta"))
                   if os.path.isdir(d) and os.path.basename(d) != "livingma-kit")
    print(f"{'DRY-RUN' if args.dry_run else 'SYNC'}  {len(repos)} *_LivingMeta repos\n")

    total_written = total_repos = 0
    for repo in repos:
        written = 0
        for sub in subtrees:
            src_root = os.path.join(KIT, sub)
            if not os.path.isdir(src_root):
                continue
            for root, _dirs, files in os.walk(src_root):
                rel = os.path.relpath(root, KIT)
                dst_dir = os.path.join(repo, rel)
                for f in files:
                    src = os.path.join(root, f)
                    dst = os.path.join(dst_dir, f)
                    if os.path.isfile(dst) and _md5(src) == _md5(dst):
                        continue
                    written += 1
                    if not args.dry_run:
                        os.makedirs(dst_dir, exist_ok=True)
                        shutil.copy2(src, dst)
        if written:
            total_repos += 1
            total_written += written
            print(f"  {os.path.basename(repo):34} {written} file(s) {'would change' if args.dry_run else 'updated'}")
    print(f"\n{'Would update' if args.dry_run else 'Updated'} {total_written} files across {total_repos} repos "
          f"({len(repos) - total_repos} already in sync).")


if __name__ == "__main__":
    main()
