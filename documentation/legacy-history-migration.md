# Vega Strike Assets-Masters Legacy History Migration

This document details the mapping, reconstruction, and verification of legacy release branches and tags for the **Assets-Masters** repository (*Vega Strike: Upon the Coldest Sea* master asset and texture repository).

---

## 1. Background & Scope

The `Assets-Masters` repository was created in Subversion on September 14, 2007 (r11333, `73e2ef1`) under `trunk/masters` to manage high-resolution texture masters, source 3D models, audio masters, and media design files separate from packaged game data.

Because this repository was established in late 2007 during the 0.5.x era, it did not exist for versions 0.1.x through 0.4.x. Subversion tags corresponding to project releases in the 0.5.x era preserved master assets under `tags/<release>/masters`.

This migration reconstructs the sequential `0.5.x` maintenance release branch and standardizes all legacy master release tags under the `legacy_<tag_name>` naming scheme.

---

## 2. Release Line & Tag Mapping Table

| Series | Tag Name | Base Anchor Commit | Tree SHA | SVN Tag Path | Original Author | Historical Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0.5.x** | `legacy_0.5.0` | `2fe5066` | `a80b058b` | `tags/0.5.0/masters` | ace123 | 2008-05-08 |
| | `legacy_vegastrike_0_5_1_beta1` | `3521c07` | `cbe9117d` | `tags/vegastrike_0_5_1_beta1/masters` | klaussfreire | 2011-03-09 |
| | `legacy_vegastrike_0_5_1_beta2` | `0597fdf` | `e12de745` | `tags/vegastrike_0_5_1_beta2/masters` | klaussfreire | 2012-01-30 |
| | `legacy_vegastrike_0_5_1_r1` | `bc0b3ff` | `d87c47c9` | `tags/vegastrike_0_5_1_r1/masters` | klaussfreire | 2012-04-01 |
| | `legacy_0.5.2alpha-archive` | `4263828` | `329e096a` | `tags/0.5.2alpha-archive/masters` | pyramid3d | 2020-02-06 |

---

## 3. Migration Methodology

1. **Subversion Tag Trees**: The actual master asset trees in Subversion resided within the `masters/` directory of each release tag in the Subversion repository.
2. **Plumbing Operations**: Using `git write-tree` via an isolated temporary index file (`tempfile.gettempdir()`), exact Git tree objects were synthesized from the Subversion tag checkouts.
3. **Commit Chaining**: The sequential release branch `0.5.x` was created using `git commit-tree` to preserve parentage while maintaining historical authorship and committer timestamps.
4. **Annotated Legacy Tags**: Tags were created using `git tag -a -f --no-sign` under the `legacy_*` prefix to prevent collision with modern GitHub release tags.

---

## 4. Automation Tool

The migration is automated via [`scripts/migrate_legacy_svn_history.py`](../scripts/migrate_legacy_svn_history.py).

### Usage:
```bash
# Dry run verification
python3 scripts/migrate_legacy_svn_history.py --svn-dir /path/to/svn/vegastrike-code

# Execute migration
python3 scripts/migrate_legacy_svn_history.py --svn-dir /path/to/svn/vegastrike-code --execute
```
