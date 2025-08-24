# Let the client know we're running SC2 in Wine
export SC2PF=WineLinux
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# FIXME Replace with path to the version of Wine used to run SC2
export WINE="/usr/bin/wine"

# FIXME Replace with path to StarCraft II install folder
export SC2PATH="/home/alchav/Games/battlenet/drive_c/Program Files (x86)/StarCraft II/"

# FIXME Set to directory which contains Archipelago AppImage file
#PATH_TO_ARCHIPELAGO=

# Gets the latest version of Archipelago AppImage in PATH_TO_ARCHIPELAGO.
# If PATH_TO_ARCHIPELAGO is not set, this defaults to the directory containing
# this script file.
#ARCHIPELAGO="$(ls ${PATH_TO_ARCHIPELAGO:-$(dirname $0)}/Archipelago_*.AppImage | sort -r | head -1)"
/home/alchav/PycharmProjects/Archipelago/venv310/bin/python3.10 Starcraft2Client.py
# Start the Archipelago client
#$ARCHIPELAGO Starcraft2Client
