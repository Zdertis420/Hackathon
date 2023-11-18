#!/bin/sh

LD_LIBRARY_PATH=`pwd`/build/app build/app/hack "$@"
