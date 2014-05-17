#! /bin/bash

kill -9 $(cat ./researcher1.pid)
rm researcher1.pid
kill -9 $(cat ./researcher2.pid)
rm researcher2.pid
kill -9 $(cat ./provider1.pid)
rm provider1.pid
kill -9 $(cat ./tripler1.pid)
rm tripler1.pid
