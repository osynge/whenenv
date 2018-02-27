#!/bin/bash


py_os_var()
{
PY_ACTION="$1" python - <<END
import platform
import re
import sys
import os
action = os.environ['PY_ACTION']
py_os = platform.linux_distribution()[0].strip()
py_os_ver_maj = 0
py_os_ver_min = 0
version_raw_split = re.split('[.\/]', platform.linux_distribution()[1])
if len(version_raw_split) >= 2:
    py_os_ver_maj =  version_raw_split[0].strip()
    py_os_ver_min =  version_raw_split[1].strip()
if action == "py_os":
    sys.stdout.write(py_os)
if action == "py_os_ver_maj":
    sys.stdout.write(py_os_ver_maj)
if action == "py_os_ver_min":
    sys.stdout.write(py_os_ver_min)
END
}


PY_OS=`py_os_var py_os`
PY_OS_VER_MAJ=`py_os_var py_os_ver_maj`
PY_OS_VER_MIN=`py_os_var py_os_ver_min`

if [ "X${PY_OS}" = "Xdebian" ] ; then
PKG_FORMAT="dpkg"
fi
if [ "X${PY_OS}" = "XScientific Linux" ] ; then
PKG_FORMAT="rpm"
fi
if [ "X${PY_OS}" = "XopenSUSE" ] ; then
PKG_FORMAT="rpm"
fi
if [ "X${PY_OS}" = "XFedora" ] ; then
PKG_FORMAT="rpm"
fi

if [ "X${PKG_FORMAT}" = "X" ] ; then
PKG_FORMAT="None"
fi
#echo PY_OS=$PY_OS
#echo PY_OS_VER_MAJ=$PY_OS_VER_MAJ
#echo PY_OS=$PY_OS_VER_MIN
#echo PY_OS=$PKG_FORMAT
export PY_OS
export PY_OS_VER_MAJ
export PY_OS_VER_MIN
export PKG_FORMAT

