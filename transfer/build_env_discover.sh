PY_OS=`python -c "import platform; import sys; sys.stdout.write(platform.linux_distribution()[0].strip())"`
PY_OS_VER_MAJ=`python -c "import platform; import sys; sys.stdout.write(platform.linux_distribution()[1].split('.')[0])"`

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
export PKG_FORMAT
