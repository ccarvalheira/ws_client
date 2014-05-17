#! /bin/bash

. ../env/bin/activate
python researcher.py &
echo $! > ./researcher1.pid
python researcher.py &
echo $! > ./researcher2.pid
python provider.py &
echo $! > ./provider1.pid
python tripler.py &
echo $! > ./tripler1.pid
