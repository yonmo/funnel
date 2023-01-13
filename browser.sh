#!/bin/bash

if [ "$EUID" = 0 ]; then

    # Necessary Setup

    sudo apt install mercurial
    hg clone https://hg.mozilla.org/mozilla-central/
    cd mozilla-central
    ./mach bootstrap

    # Modify The Critical Exclamation Point Before Running The Following

    # ./mach build
    # ./mach geckodriver

else
    echo "Please run this script as a privileged user..."
    exit 1
fi
