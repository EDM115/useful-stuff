#!/bin/bash

echo "--- Launch Discord script by EDM115 ---"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -b|--build) build="$2"; shift ;;
        -bd|--betterdiscord) betterdiscord="$2"; shift ;;
        *) echo "Unknown parameter passed : $1"; exit 1 ;;
    esac
    shift
done

# Validate build parameter
if [[ -z "$build" ]]; then
    echo "Build not provided. Usage : -b/--build [stable|ptb|canary]"
    echo "Exiting..."
    exit 1
fi

# Define variables based on build
case $build in
    "stable") appname="discord" ;;
    "ptb") appname="discord-ptb" ;;
    "canary") appname="discord-canary" ;;
    *) echo "Invalid build. Use 'stable', 'ptb', or 'canary'"; exit 1 ;;
esac

# Launch discord and capture stdout
$appname | while read line
do
    echo "$line"

    # Check for the update-manually message
    if [[ "$line" == *"update-manually"* ]]; then
        # Extract version from the line
        version=$(echo "$line" | grep -oP 'update-manually \K[0-9.]+')

        # Kill discord
        pkill -f $appname

        # Call updater script with the new version and restart discord
        sudo ./upgrade-discord.sh -v $version -b $build -bd $betterdiscord | while read update_line
        do
            if [[ "$update_line" == *"Done !"* ]]; then
                $appname &
                break 2
            fi
        done

        break
    fi

    # Check for the splashScreen.pageReady message (no update)
    if [[ "$line" == *"splashScreen.pageReady"* ]]; then
        sleep 5
        break
    fi
done
