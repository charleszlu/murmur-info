#!/bin/bash

if [ $# -gt 0 ]
then
    case $1 in
        config)
       	    echo "graph_title NVidia Temperature"
	    echo "graph_vlabel Temperature"
	    echo "temp.lablel Temperature in Celsius"
	    exit 0
        ;;
    esac
fi

TEMPERATURE=$(/usr/bin/nvidia-settings -q GPUCoreTemp | sed -nr -e 's/.*([0-9]{2})\./\1/p'|uniq)
#PERF_LEVEL=""
echo "temp.value $TEMPERATURE"

