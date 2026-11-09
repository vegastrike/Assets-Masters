# Vega Strike Assets-Masters Legacy History Migration

This document details the mapping, reconstruction, and verification of legacy release branches and tags for the **Assets-Masters** repository (*Vega Strike: Upon the Coldest Sea* master asset and texture repository).

---

## 1. Background & Architecture

The `Assets-Masters` repository was created in Subversion on September 14, 2007 (r11333, commit [`73e2ef1`](https://github.com/vegastrike/Assets-Masters/commit/73e2ef1a59b290f074faaeeeab2ed99b18a3bf85)) under `trunk/masters` to manage high-resolution texture masters, source 3D models, audio masters, and media design files separate from packaged game data.

Because this repository was established in late 2007 during the 0.5.x development era, it did not exist as a separate repository or directory for earlier project releases (versions 0.1.x through 0.4.x). Subversion tags corresponding to project releases in the 0.5.x era preserved master assets under `tags/<release>/masters`.

This migration reconstructs the sequential `0.5.x` maintenance release branch and standardizes all legacy master release tags under the `legacy_<tag_name>` naming scheme.

---

## 2. Early Project History (0.1.x – 0.4.x) & Assets-Production Linkage

Prior to September 2007, Vega Strike game assets were maintained within a single unified tree in the monolithic Subversion/CVS repository:
* **0.1.x – 0.3.x era (2001–2003):** Assets resided in `trunk/data`.
* **0.4.x era (2003–2007):** Assets resided in `trunk/data4.x`.

During these earlier eras, master assets and production game data were not split into separate repositories. All assets (including source textures and models) were tracked directly within the primary data tree.

### Full History in `Assets-Production`:
Users, packagers, and historians seeking the complete continuous history and historical release lines for **0.1.x through 0.4.x** should refer to the **Assets-Production** repository:
* **Repository URL:** [https://github.com/vegastrike/Assets-Production](https://github.com/vegastrike/Assets-Production)
* **Reconstructed Release Branches:**
  * [`0.1.x`](https://github.com/vegastrike/Assets-Production/tree/0.1.x) (Milestones from Oct 2001 to Jan 2002)
  * [`0.2.x`](https://github.com/vegastrike/Assets-Production/tree/0.2.x) (Releases 0.2.0 through 0.2.9.4)
  * [`0.3.x`](https://github.com/vegastrike/Assets-Production/tree/0.3.x) (Releases 0.3.0 through 0.3.9)
  * [`0.4.x`](https://github.com/vegastrike/Assets-Production/tree/0.4.x) (Releases 0.4.0 through 0.4.3)
  * [`0.5.x`](https://github.com/vegastrike/Assets-Production/tree/0.5.x) (Releases 0.5.0 through 0.5.2alpha-archive)
* **Legacy Release Tags:** 25 historical tags under the `legacy_*` prefix (e.g. `legacy_betareleasecandidate102901`, `legacy_vegastrike_0.1.0` ... `legacy_vegastrike_0_4_3`).
* **Documentation:** [Assets-Production Legacy History Migration Guide](https://github.com/vegastrike/Assets-Production/blob/documentation_legacy-svn-history/documentation/legacy-history-migration.md)

---

## 3. Release Line & Tag Mapping Table (0.5.x)

In `Assets-Masters`, historical releases begin with the 0.5.x series, chained sequentially along the `0.5.x` maintenance release branch:

| Series | Tag Name | Base Anchor Commit | Tree SHA | SVN Tag Path | Original Author | Historical Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0.5.x** | `legacy_0.5.0` | `2fe5066` | `a80b058b` | `tags/0.5.0/masters` | ace123 | 2008-05-08 |
| | `legacy_vegastrike_0_5_1_beta1` | `3521c07` | `cbe9117d` | `tags/vegastrike_0_5_1_beta1/masters` | klaussfreire | 2011-03-09 |
| | `legacy_vegastrike_0_5_1_beta2` | `0597fdf` | `e12de745` | `tags/vegastrike_0_5_1_beta2/masters` | klaussfreire | 2012-01-30 |
| | `legacy_vegastrike_0_5_1_r1` | `bc0b3ff` | `d87c47c9` | `tags/vegastrike_0_5_1_r1/masters` | klaussfreire | 2012-04-01 |
| | `legacy_0.5.2alpha-archive` | `4263828` | `329e096a` | `tags/0.5.2alpha-archive/masters` | pyramid3d | 2020-02-06 |

---

## 4. Migration Methodology

1. **Subversion Tag Trees**: The actual master asset trees in Subversion resided within the `masters/` directory of each release tag in the Subversion repository.
2. **Plumbing Operations**: Using `git write-tree` via an isolated temporary index file (`tempfile.gettempdir()`), exact Git tree objects were synthesized from the Subversion tag checkouts.
3. **Commit Chaining**: The sequential release branch `0.5.x` was created using `git commit-tree` to preserve parentage while maintaining historical authorship and committer timestamps.
4. **Annotated Legacy Tags**: Tags were created using `git tag -a -f --no-sign` under the `legacy_*` prefix to prevent collision with modern GitHub release tags.

---

## 5. Automation Tool

The migration is automated via [`scripts/migrate_legacy_svn_history.py`](../scripts/migrate_legacy_svn_history.py).

### Usage:
```bash
# Dry run verification
python3 scripts/migrate_legacy_svn_history.py --svn-dir /path/to/svn/vegastrike-code

# Execute migration
python3 scripts/migrate_legacy_svn_history.py --svn-dir /path/to/svn/vegastrike-code --execute
```
