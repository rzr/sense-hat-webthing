#!/bin/sh -e
#                                                              -*- Mode: Sh -*-
# SPDX-License-Indentifier: MPL-2.0

id=$(/usr/bin/lsb_release -i -s || echo "unknown")

case "$id" in
    "Debian" | "Raspbian" | "Ubuntu")
        sudo=$(which sudo || echo"")
        $sudo sync
        $sudo apt-get update -y ||:
        $sudo apt-get install -y python3-sense-hat
        $sudo sync
        ;;
    *)
        echo "warning: Not supported: $id trying pip"
        sudo pip3 install -r requirements.txt
        ;;
esac
