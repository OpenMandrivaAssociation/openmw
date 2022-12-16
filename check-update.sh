#!/bin/sh
git ls-remote --tags https://github.com/OpenMW/openmw 2>/dev/null |awk '{ print $2; }' |sed -e 's,\^{},,' |grep ^refs/tags/openmw- |cut -d- -f2- |sort -V |tail -n1
