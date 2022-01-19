# Flipflop demo

https://docs.google.com/document/d/1EKELzHmQ0uu2yd_Y5IZuVqJGCVpMIpfF3u9pVEk68pQ/edit#

Support files for a video by https://ZeroToASICcourse.com

## Build GDS

After install of openlane/pdk etc, copy this directory to $OPENLANE_ROOT/designs. Then:

    cd $OPENLANE_ROOT
    make mount
    ./flow.tcl -design flipflop_demo

## Run the spice simulation

This will simulate moving a data pulse through the setup and hold times of a d type flop.

    make sim

## Use the GUI

    ./gui.py
    
You will need to install the [requirements](requirements.txt)
