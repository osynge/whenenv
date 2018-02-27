if [ "X${DIR_EXPORT_ROOT}" = "X" ] ; then
    echo "DIR_EXPORT_ROOT not defined"
    sleep 10
    exit 1
fi


if [ "X${DIR_ART_BIN}" = "X" ] ; then
echo "DIR_EXPORT_RPM_SRPMS not defined"
sleep 10
exit 1
fi


if [ "X${DIR_ART_SRC}" = "X" ] ; then
echo "DIR_EXPORT_RPM_SRPMS not defined"
sleep 10
exit 1
fi

if [ "X${RELEASE_ENV}" = "X" ] ; then
  if [ "X${BRANCH}" != "X" ] ; then
    echo "release type defaulted from BRANCH"
    RELEASE_ENV="nightly/${BRANCH}"
  fi
fi

if [ "X${RELEASE_ENV}" = "X" ] ; then
  echo "release type not defined atempting to default by RELEASE_ENV"
  if [ "X${RELEASE}" != "X" ] ; then
    if [ "X${RELEASE}" = "Xdevelopment" ] ; then
      RELEASE_ENV="nightly/master"
    fi

    if [ "X${RELEASE}" = "Xproduction" ] ; then
      RELEASE_ENV="production"
    fi
  fi
fi

if [ "X${PLATFORM}" = "X" ] ; then
echo "PLATFORM not defined"
PLATFORM=`arch`
fi

if [ "X${RELEASE_FLAVOR}" = "X" ] ; then
echo "RELEASE_FLAVOR not defined"
PY_OS=`python -c "import platform; import sys; sys.stdout.write(platform.linux_distribution()[0].strip())"`
PY_OS_VER_MAJ=`python -c "import platform; import sys; sys.stdout.write(platform.linux_distribution()[1].split('.')[0])"`
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

if [ "X${RELEASE_ENV}" = "X" ] ; then
echo "No RELEASE_ENV defined"
sleep 1
exit 1
fi


if [ "X${DIR_EXPORT_TGZ}" = "X" ] ; then
DIR_EXPORT_TGZ="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_ENV}/src/tgz"
fi
if [ "X${DIR_EXPORT_BTGZ}" = "X" ] ; then
DIR_EXPORT_BTGZ="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_ENV}/${PLATFORM}/tgz"
fi
if [ "X${DIR_EXPORT_SRPM}" = "X" ] ; then
DIR_EXPORT_SRPM="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_ENV}/src/srpm"
fi
if [ "X${DIR_EXPORT_RPM}" = "X" ] ; then
DIR_EXPORT_RPM="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_ENV}/${PLATFORM}/rpm"
fi

export DIR_EXPORT_TGZ
export DIR_EXPORT_BTGZ
export DIR_EXPORT_SRPM
export DIR_EXPORT_RPM

mkdir -p ${DIR_EXPORT_TGZ}
mkdir -p ${DIR_EXPORT_BTGZ}
mkdir -p ${DIR_EXPORT_SRPM}
mkdir -p ${DIR_EXPORT_RPM}
