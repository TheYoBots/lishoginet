#!/bin/sh

echo "- Getting latest Fairy-Stockfish ..."

if [ -d Fairy-Stockfish/src ]; then
    cd Fairy-Stockfish/src
    make clean > /dev/null
    git pull
else
    git clone --depth 1 https://github.com/ianfab/Fairy-Stockfish.git
    cd Fairy-Stockfish/src
fi

echo "- Determining CPU architecture ..."

ARCH="$(uname -m)"
EXE=fairy-stockfish-"$ARCH"
case "$ARCH" in
    aarch64|arm)
        ARCH=armv7
        if [ -f /proc/cpuinfo ]; then
            if grep "^CPU architecture" /proc/cpuinfo | grep -q 8 ; then
                ARCH=armv8
            fi
        fi
        EXE=fairy-stockfish-"$ARCH"
        ;;
    x86_64)
        ARCH=x86-64
        ;;
    i*86)
        # Assuming that everyone trying to run lishoginet has SSE
        ARCH=x86-32
        ;;
    ppc|ppcle)
        ARCH=ppc-32
        ;;
    ppc64|ppc64le)
        ARCH=ppc-64
        ;;
    *)
        # If arch unknown, fall back to general config
        if [ "$(getconf LONG_BIT)" = "64" ]; then
            ARCH=general-64
        else
            ARCH=general-32
        fi
        ;;
esac

if [ "$ARCH" = "x86-64" ]; then
    if [ -f /proc/cpuinfo ]; then
        if grep "^flags" /proc/cpuinfo | grep -q popcnt ; then
            ARCH=x86-64-modern
            EXE=fairy-stockfish-x86_64-modern
        fi

        if grep "^vendor_id" /proc/cpuinfo | grep -q Intel ; then
            if grep "^flags" /proc/cpuinfo | grep bmi2 | grep -q popcnt ; then
                ARCH=x86-64-bmi2
                EXE=fairy-stockfish-x86_64-bmi2
            fi
       fi
    fi
fi

echo "- Building and profiling $EXE ... (patience advised)"
make profile-build ARCH=$ARCH EXE=../../$EXE > /dev/null

cd ../..
echo "- Done!"