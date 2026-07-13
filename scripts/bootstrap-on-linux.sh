#!/usr/bin/env bash
#====================================
# @file   : bootstrap-on-linux.sh
# @brief  : bash script to install the dependencies needed to
#           automatically generate the assets for Assets-Production
#           from the Assets-Masters source, on Linux
#====================================
# Copyright (C) 2026 Evert Vorster, Stephen G. Tuggy, Roy Falk,
# Benjamen R. Meyer, SGD1953, and other vsUTCS contributors.
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


set -e

echo "------------------------------------------"
echo "--- bootstrap-on-linux.sh | 2026-07-13 ---"
echo "------------------------------------------"

UPDATE_ALL_SYSTEM_PACKAGES="$1"

if [ -f /etc/os-release ]
then
    OS_RELEASE_LOCATION="/etc/os-release"
elif [ -f /usr/lib/os-release ]
then
    OS_RELEASE_LOCATION="/usr/lib/os-release"
else
    echo "os-release file not found; unable to continue"
    exit 1
fi
LINUX_ID=$(grep ^ID= $OS_RELEASE_LOCATION | sed 's/^ID=//' | tr -d '"\n')
echo "LINUX_ID = ${LINUX_ID}"
LINUX_CODENAME=$(grep ^VERSION_CODENAME= $OS_RELEASE_LOCATION | sed 's/^VERSION_CODENAME=//' | tr -d '"\n')
echo "LINUX_CODENAME = ${LINUX_CODENAME}"
LINUX_VERSION_ID=$(grep ^VERSION_ID= $OS_RELEASE_LOCATION | sed 's/^VERSION_ID=//' | tr -d '"\n')
echo "LINUX_VERSION_ID = ${LINUX_VERSION_ID}"

function bootstrapOnDebian()
{
    apt-get update

    if [ ${UPDATE_ALL_SYSTEM_PACKAGES} -eq 1 ]
    then
        apt-get -qy upgrade
    fi

    case "$LINUX_CODENAME" in
        "trixie")
            apt-get -qy install libnvtt-bin python3-virtualenv
            if [ ${SKIP_MANUAL} -eq 1 ]
            then
                echo "Skipping texlive installation; SKIP_MANUAL is set"
            else
                apt-get -qy install texlive-full
            fi
            ;;
        "bookworm")
            apt-get -qy install libnvtt-bin python3-virtualenv
            if [ ${SKIP_MANUAL} -eq 1 ]
            then
                echo "Skipping texlive installation; SKIP_MANUAL is set"
            else
                apt-get -qy install texlive-full
            fi
            ;;
        "bullseye"|"buster"|"stretch")
            echo "Sorry, Debian ${LINUX_CODENAME} is no longer supported"
            exit 2
            ;;
        *)
            echo "Sorry, this version of Debian is unsupported"
            exit 2
            ;;
    esac
}

function bootstrapOnUbuntu()
{
    apt-get update

    if [ ${UPDATE_ALL_SYSTEM_PACKAGES} -eq 1 ]
    then
        apt-get -qy upgrade
    fi

    case "$LINUX_CODENAME" in
        "resolute"|"questing"|"plucky")
            apt-get -qy install nvidia-texture-tools python3-virtualenv
            if [ ${SKIP_MANUAL} -eq 1 ]
            then
                echo "Skipping texlive installation; SKIP_MANUAL is set"
            else
                apt-get -qy install texlive-full
            fi
            ;;
        "noble")
            apt-get -qy install nvidia-texture-tools python3-virtualenv
            if [ ${SKIP_MANUAL} -eq 1 ]
            then
                echo "Skipping texlive installation; SKIP_MANUAL is set"
            else
                apt-get -qy install texlive-full
            fi
            ;;
        "jammy"|"hirsute"|"impish"|"focal"|"bionic"|"xenial")
            echo "Sorry, Ubuntu ${LINUX_CODENAME} is no longer supported"
            exit 2
            ;;
        *)
            echo "Sorry, this version of Ubuntu is unsupported"
            exit 2
            ;;
    esac
}

case "${LINUX_ID}" in
    "debian")
        bootstrapOnDebian
        ;;
    "ubuntu")
        bootstrapOnUbuntu
        ;;
    *)
        echo "Sorry, Assets-Masters does not currently support this Linux distribution"
        exit 2
        ;;
esac

mkdir -p /usr/local/src/vsUTCS && cd $_

/usr/bin/env python3 -m venv ./.venv
source ./.venv/bin/activate
pip install pillow>=10.4.0

echo "Bootstrapping finished!"
