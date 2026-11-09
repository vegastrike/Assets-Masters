#!/usr/bin/env python3
"""
migrate_legacy_svn_history.py for Assets-Masters:
Maps Subversion release tags to Git commits and reconstructs legacy
release tags (legacy_<tag>) for master textures and assets.

Uses Git plumbing (git write-tree, git commit-tree, git tag) to create
tags without modifying the active working tree or index.
"""

import sys
import os
import subprocess
import argparse
import tempfile

# Specification of Branches, Steps, and Legacy Tags for Assets-Masters
MIGRATION_PLAN = [
    {
        "branch": "0.5.x",
        "description": "0.5 Asset Master Release Line (0.5.0 to 0.5.2alpha-archive)",
        "steps": [
            {
                "tag": "legacy_0.5.0",
                "base_commit": "2fe5066",
                "svn_tag_dir": "0.5.0",
                "author": "ace123 <ace123@users.sourceforge.net>",
                "date": "2008-05-08T23:13:36Z",
                "replay_diffs": True
            },
            {
                "tag": "legacy_vegastrike_0_5_1_beta1",
                "base_commit": "3521c07",
                "svn_tag_dir": "vegastrike_0_5_1_beta1",
                "author": "klaussfreire <klaussfreire@users.sourceforge.net>",
                "date": "2011-03-09T01:52:19Z",
                "replay_diffs": True
            },
            {
                "tag": "legacy_vegastrike_0_5_1_beta2",
                "base_commit": "0597fdf",
                "svn_tag_dir": "vegastrike_0_5_1_beta2",
                "author": "klaussfreire <klaussfreire@users.sourceforge.net>",
                "date": "2012-01-30T05:09:59Z",
                "replay_diffs": True
            },
            {
                "tag": "legacy_vegastrike_0_5_1_r1",
                "base_commit": "bc0b3ff",
                "svn_tag_dir": "vegastrike_0_5_1_r1",
                "author": "klaussfreire <klaussfreire@users.sourceforge.net>",
                "date": "2012-04-01T00:56:09Z",
                "replay_diffs": True
            },
            {
                "tag": "legacy_0.5.2alpha-archive",
                "base_commit": "4263828",
                "svn_tag_dir": "0.5.2alpha-archive",
                "author": "pyramid3d <pyramid@openteq.lan>",
                "date": "2020-02-06T14:18:57Z",
                "replay_diffs": True
            }
        ]
    }
]

def run_cmd(cmd, git_dir, env=None):
    res = subprocess.run(cmd, cwd=git_dir, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(cmd)}\n{res.stderr}")
    return res.stdout.strip()

def get_full_commit(short_rev, git_dir):
    return run_cmd(["git", "rev-parse", short_rev], git_dir)

def resolve_svn_tags_dir(svn_path):
    if not svn_path:
        return None
    abs_path = os.path.abspath(os.path.expanduser(svn_path))
    tags_subdir = os.path.join(abs_path, "tags")
    if os.path.isdir(tags_subdir):
        return tags_subdir
    if os.path.isdir(abs_path):
        return abs_path
    return None

def find_default_svn_dir(repo_dir):
    env_dir = os.environ.get("VEGA_SVN_DIR") or os.environ.get("SVN_DIR")
    if env_dir:
        resolved = resolve_svn_tags_dir(env_dir)
        if resolved:
            return resolved

    candidates = [
        os.path.join(repo_dir, "..", "research", "vegastrike-code"),
        os.path.join(repo_dir, "..", "..", "research", "vegastrike-code"),
        os.path.join(repo_dir, "..", "vegastrike-code"),
    ]
    for cand in candidates:
        resolved = resolve_svn_tags_dir(cand)
        if resolved:
            return resolved
    return None

def find_masters_dir_in_svn(svn_tags_dir, svn_tag_subpath):
    base_tag_dir = os.path.join(svn_tags_dir, svn_tag_subpath)
    for sub in ["masters"]:
        cand = os.path.join(base_tag_dir, sub)
        if os.path.isdir(cand):
            return cand
    if os.path.isdir(base_tag_dir):
        return base_tag_dir
    return None

def create_tree_from_svn(svn_path, git_dir, temp_index):
    if os.path.exists(temp_index):
        os.remove(temp_index)
        
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = temp_index
    env["GIT_DIR"] = os.path.join(git_dir, ".git")
    env["GIT_WORK_TREE"] = svn_path
    
    run_cmd(["git", "add", "-A"], git_dir, env=env)
    tree_sha = run_cmd(["git", "write-tree"], git_dir, env=env)
    
    if os.path.exists(temp_index):
        os.remove(temp_index)
        
    return tree_sha

def execute(git_dir, svn_source_dir, temp_index, dry_run=True):
    svn_tags_dir = resolve_svn_tags_dir(svn_source_dir)
    if not svn_tags_dir or not os.path.isdir(svn_tags_dir):
        print(f"Error: Subversion tags directory could not be resolved from: {svn_source_dir}", file=sys.stderr)
        print("Please specify a valid SVN repository root (containing 'tags/') or 'tags/' directory directly via --svn-dir.", file=sys.stderr)
        sys.exit(1)

    print(f"=== Vega Strike Assets-Masters Legacy Migration (Dry Run: {dry_run}) ===\n")
    print(f"  Git Repo: {git_dir}")
    print(f"  SVN Tags: {svn_tags_dir}\n")
    
    for group in MIGRATION_PLAN:
        branch = group["branch"]
        desc = group["description"]
        print(f"==================================================")
        print(f"Processing Series: {desc} (Branch: {branch or 'None'})")
        print(f"==================================================")
        
        current_branch_tip = None
        
        for step in group["steps"]:
            tag_name = step["tag"]
            base_rev = step["base_commit"]
            base_commit = get_full_commit(base_rev, git_dir)
            replay = step["replay_diffs"]
            svn_dir = step["svn_tag_dir"]
            author = step["author"]
            date_str = step["date"]
            
            print(f"\n--- Tag: {tag_name} ---")
            print(f"  Trunk Anchor: {base_commit[:10]} ({base_rev})")
            
            if replay and svn_dir:
                masters_path = find_masters_dir_in_svn(svn_tags_dir, svn_dir)
                if not masters_path or not os.path.exists(masters_path):
                    raise FileNotFoundError(f"Subversion masters path not found for tag: {svn_dir}")
                print(f"  Reading SVN tree from: {os.path.relpath(masters_path, svn_tags_dir)}")
                tree_sha = create_tree_from_svn(masters_path, git_dir, temp_index)
                print(f"  Generated Tree SHA: {tree_sha[:10]}")
                
                base_tree = run_cmd(["git", "rev-parse", f"{base_commit}^{{tree}}"], git_dir)
                parent_commit = current_branch_tip if (branch and current_branch_tip) else base_commit
                
                if tree_sha != base_tree or (branch and current_branch_tip):
                    msg = f"Release {tag_name.replace('legacy_', '')} SVN master asset tree\n\nMirrored from Subversion {os.path.relpath(masters_path, svn_tags_dir)}."
                    
                    env = os.environ.copy()
                    name, email = author.split("<")
                    name = name.strip()
                    email = email.replace(">", "").strip()
                    env["GIT_AUTHOR_NAME"] = name
                    env["GIT_AUTHOR_EMAIL"] = email
                    env["GIT_AUTHOR_DATE"] = date_str
                    env["GIT_COMMITTER_NAME"] = name
                    env["GIT_COMMITTER_EMAIL"] = email
                    env["GIT_COMMITTER_DATE"] = date_str
                    
                    cmd = ["git", "commit-tree", tree_sha, "-p", parent_commit, "-m", msg]
                    if dry_run:
                        sim_id = f"sim_{tag_name}"
                        print(f"  [DRY RUN] Would create commit with tree {tree_sha[:10]} and parent {parent_commit[:10]}")
                        commit_to_tag = sim_id
                    else:
                        new_commit = run_cmd(cmd, git_dir, env=env)
                        print(f"  Created Commit: {new_commit[:10]} (parent: {parent_commit[:10]})")
                        commit_to_tag = new_commit
                else:
                    print(f"  Tree is identical to trunk commit {base_commit[:10]}; no extra commit needed.")
                    commit_to_tag = base_commit
            else:
                commit_to_tag = base_commit
                
            current_branch_tip = commit_to_tag
            
            # Tagging
            tag_msg = f"Legacy Subversion master asset release tag: {tag_name}\n\nMirrored from SVN tag {svn_dir if svn_dir else tag_name}."
            tag_env = os.environ.copy()
            name, email = author.split("<")
            name = name.strip()
            email = email.replace(">", "").strip()
            tag_env["GIT_COMMITTER_NAME"] = name
            tag_env["GIT_COMMITTER_EMAIL"] = email
            tag_env["GIT_COMMITTER_DATE"] = date_str

            if dry_run:
                print(f"  [DRY RUN] Would create tag '{tag_name}' at {commit_to_tag[:10]}")
            else:
                run_cmd(["git", "tag", "-a", "-f", "-m", tag_msg, "--no-sign", tag_name, commit_to_tag], git_dir, env=tag_env)
                print(f"  Created tag '{tag_name}' -> {commit_to_tag[:10]}")
                
        # Update or create branch if configured
        if branch:
            if dry_run:
                print(f"\n  [DRY RUN] Would set branch '{branch}' -> {current_branch_tip[:10]}")
            else:
                run_cmd(["git", "update-ref", f"refs/heads/{branch}", current_branch_tip], git_dir)
                print(f"\n  Updated branch '{branch}' -> {current_branch_tip[:10]}")
                
        print()

if __name__ == "__main__":
    repo_default = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_svn = find_default_svn_dir(repo_default)
    temp_index_default = os.path.join(tempfile.gettempdir(), "vega_masters_migration_git_index")
    
    parser = argparse.ArgumentParser(description="Vega Strike Assets-Masters Legacy Tag Migration Tool")
    parser.add_argument("--git-dir", default=repo_default, help=f"Path to Git repository (default: {repo_default})")
    parser.add_argument(
        "--svn-dir",
        "--svn-tags-dir",
        dest="svn_dir",
        default=default_svn,
        help="Path to SVN repository root (containing 'tags/') or SVN tags directory directly (env: VEGA_SVN_DIR or SVN_DIR)"
    )
    parser.add_argument("--temp-index", default=temp_index_default, help="Temporary index file path")
    parser.add_argument("--execute", action="store_true", help="Perform real changes (default is dry-run)")
    args = parser.parse_args()
    
    execute(
        git_dir=args.git_dir,
        svn_source_dir=args.svn_dir,
        temp_index=args.temp_index,
        dry_run=not args.execute
    )
