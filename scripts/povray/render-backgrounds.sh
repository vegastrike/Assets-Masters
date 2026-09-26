#!/usr/bin/env bash
#====================================
# @file   : scripts/povray/render-backgrounds.sh
# @brief  : Render the Vega Strike space backgrounds from their POV-Ray
#           sources and assemble the engine cubemaps.
#====================================
# Copyright (C) 2026 Evert Vorster, Stephen G. Tuggy, Roy Falk,
# Benjamen R. Meyer, and other vsUTCS contributors.
#
# This file is part of Vega Strike: Upon the Coldest Sea ("vsUTCS").
#
# vsUTCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# vsUTCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vsUTCS.  If not, see <https://www.gnu.org/licenses/>.
#
#-----------------------------------------------------------------------------
# Each background ships as textures/backgrounds/sources/<name>_source.zip.
# The Space3D script renders six frames with its skybox camera; this script
# maps those frames onto the six DDS faces (with the rotations Vega Strike
# needs), compresses each face to DXT1 with a full mip chain, and assembles
# <name>_light.cube.
#
# The frame -> face mapping and the up/down rotations were verified against
# the shipped starfield_light.cube (byte-size identical, per-face RMSE ~0.02).
#
#   DDS face   POV frame   rotation
#   +X         4           0
#   -X         2           0
#   +Y         5           90
#   -Y         6           180
#   +Z         3           0
#   -Z         1           0
#
# Usage:
#   scripts/povray/render-backgrounds.sh                 # all sourced backgrounds
#   scripts/povray/render-backgrounds.sh red_galaxy1
#   RES=4096 scripts/povray/render-backgrounds.sh starfield
#
# Output: build/backgrounds/<name>_light.cube (build/ is gitignored).
#
# Sources a zip does not carry are filled in:
#   * rand.inc / consts.inc come from a stock POV-Ray installation
#     (POV_STOCK_INC, auto-detected);
#   * a zip missing starfield.inc / spiral_galaxy.inc borrows them from a
#     sibling source (DONOR);
#   * a source still written against the pre-0.17 Space3D API is patched from
#     fixups/<name>/ (see fixups/red_galaxy1/).
#-----------------------------------------------------------------------------
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"

SOURCES="${SOURCES:-$ROOT/textures/backgrounds/sources}"
FIXUPS="${FIXUPS:-$HERE/fixups}"
WORK="${WORK:-$ROOT/build/povray}"
OUT="${OUT:-$ROOT/build/backgrounds}"

RES="${RES:-1024}"
# Sibling that supplies starfield.inc / spiral_galaxy.inc when a zip omits them.
DONOR="${DONOR:-starfield5}"
# Optional directory of extras a zip does not carry (e.g. milkyway's hipp8.tiff).
POV_EXTRA="${POV_EXTRA:-}"

FACE_NAME=(posx negx posy negy posz negz)
FACE_FRAME=(4 2 5 6 3 1)
FACE_ROT=(0 0 90 180 0 0)

ALL=(starfield starfield2 starfield3 starfield4 starfield5 milkyway plasma_galaxy red_galaxy1)

die() { echo "error: $*" >&2; exit 1; }

command -v povray >/dev/null 2>&1 || die "povray not found"
command -v magick >/dev/null 2>&1 || die "ImageMagick (magick) not found"
command -v python3 >/dev/null 2>&1 || die "python3 not found"

if [ -z "${POV_STOCK_INC:-}" ]; then
    for inc_dir in /usr/share/povray-3.7/include /usr/share/povray-3.6/include \
                   /usr/share/povray/include /usr/local/share/povray-3.7/include; do
        if [ -f "$inc_dir/rand.inc" ]; then
            POV_STOCK_INC="$inc_dir"
            break
        fi
    done
fi
[ -n "${POV_STOCK_INC:-}" ] || die "POV-Ray stock includes not found; set POV_STOCK_INC to the directory holding rand.inc"

render_one() {
    local name="$1"
    local zip="$SOURCES/${name}_source.zip"
    local dir="$WORK/$name"

    [ -f "$zip" ] || { echo "error: no source zip for '$name': $zip" >&2; return 1; }

    rm -rf "$dir"
    mkdir -p "$dir/gallery" # some inis write their frames under gallery/
    unzip -q -o "$zip" -d "$dir"

    # A source written against an older Space3D API is patched over the zip's copy.
    if [ -d "$FIXUPS/$name" ]; then
        cp -f "$FIXUPS/$name"/* "$dir"/
        echo "$name: applied fixup from fixups/$name" >&2
    fi

    # Fill in include files a zip forgot, from a sibling source.
    local inc
    for inc in starfield.inc spiral_galaxy.inc; do
        if [ ! -f "$dir/$inc" ]; then
            unzip -p "$SOURCES/${DONOR}_source.zip" "$inc" > "$dir/$inc" 2>/dev/null \
                || { echo "error: $name: missing $inc and donor '$DONOR' has none" >&2; return 1; }
            echo "$name: borrowed $inc from $DONOR" >&2
        fi
    done

    # Assets a zip omitted but that are not redistributable (e.g. milkyway's
    # hipp8.tiff); the caller points POV_EXTRA at a directory holding them.
    if [ -n "$POV_EXTRA" ] && [ -d "$POV_EXTRA" ]; then
        cp -n "$POV_EXTRA"/* "$dir"/ 2>/dev/null || true
    fi

    # +SF1 +EF6 force frames 1..6 even where an ini starts at frame 2.
    echo "rendering $name @ ${RES}x${RES} ..."
    if ! ( cd "$dir" && povray starfield_example.ini +Istarfield_example.pov \
            +W"$RES" +H"$RES" +SF1 +EF6 +FN +L"$POV_STOCK_INC" +L"$dir" ) \
            > "$dir/povray.log" 2>&1; then
        tail -n 20 "$dir/povray.log" >&2
        echo "error: $name: povray failed (see $dir/povray.log)" >&2
        return 1
    fi

    build_cube "$name" "$dir"
}

build_cube() {
    local name="$1" dir="$2"
    mkdir -p "$OUT" "$WORK/$name/faces"

    local faces=() i frame png face
    for i in 0 1 2 3 4 5; do
        frame=$(printf '%03d' "${FACE_FRAME[$i]}")
        png=$(find "$dir" -name "*_${frame}.png" | head -1)
        if [ -z "$png" ]; then
            echo "error: $name: no rendered frame $frame under $dir" >&2
            return 1
        fi

        face="$WORK/$name/faces/${FACE_NAME[$i]}.dds"
        magick "$png" -rotate "${FACE_ROT[$i]}" -resize "${RES}x${RES}" \
            -define dds:compression=dxt1 "$face" || return 1
        faces+=("$face")
    done

    python3 "$HERE/dds_cubemap.py" "$OUT/${name}_light.cube" "${faces[@]}" || return 1
    echo "built $OUT/${name}_light.cube ($(du -h "$OUT/${name}_light.cube" | cut -f1))"
}

names=("$@")
[ ${#names[@]} -gt 0 ] || names=("${ALL[@]}")
for n in "${names[@]}"; do
    render_one "$n" || echo "FAILED: $n (continuing)" >&2
done
