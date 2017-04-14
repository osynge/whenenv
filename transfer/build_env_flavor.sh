if [ "X${PY_OS}" = "X" ] ; then
    sleep 4
    echo PY_OS is undefiend
    exit 1
fi
if [ "X${PY_OS_VER_MAJ}" = "X" ] ; then
    sleep 4
    echo PY_OS_VER_MAJ is undefiend
    exit 1
fi

if [ "X${RELEASE_FLAVOR}" = "X" ] ; then
    if [ "X${PY_OS}" = "Xdebian" ] ; then
        RELEASE_FLAVOR="debian/${PY_OS_VER_MAJ}"
    fi
    if [ "X${PY_OS}" = "XScientific Linux" ] ; then
        RELEASE_FLAVOR="scientific/${PY_OS_VER_MAJ}"
    fi
    if [ "X${PY_OS}" = "XopenSUSE" ] ; then
        RELEASE_FLAVOR="openSUSE/${PY_OS_VER_MAJ}"
    fi
    if [ "X${PY_OS}" = "XFedora" ] ; then
        RELEASE_FLAVOR="Fedora/${PY_OS_VER_MAJ}"
    fi
fi
if [ "X${RELEASE_FLAVOR}" = "X" ] ; then
    echo "No flavour defined"
    RELEASE_FLAVOR="${PY_OS}/${PY_OS_VER_MAJ}"
fi

export RELEASE_FLAVOR
