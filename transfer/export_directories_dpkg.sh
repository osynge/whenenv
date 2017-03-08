if [ "X${ROOTDIR}" = "X" ] ; then
    echo "ROOTDIR not defined"
    ROOTDIR="/export/jenkins_matrix_build/repo"
    #exit 1
    if [ "X${REPOSITORY_TYPE}" = "Xpublic" ] ; then
        ROOTDIR="/export/jenkins_matrix_build/public_repo"
    fi
    if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
        ROOTDIR="/export/jenkins_matrix_build/private_repo"
    fi
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

if [ "X${RELEASE_TYPE}" = "X" ] ; then
  if [ "X${BRANCH}" != "X" ] ; then
    echo "release type defaulted from BRANCH"
    RELEASE_TYPE="nightly/${BRANCH}"
  fi
fi

if [ "X${RELEASE_TYPE}" = "X" ] ; then
  echo "release type not defined atempting to default by RELEASE_TYPE"
  if [ "X${RELEASE}" != "X" ] ; then
    if [ "X${RELEASE}" = "Xdevelopment" ] ; then
      RELEASE_TYPE="nightly/master"
    fi

    if [ "X${RELEASE}" = "Xproduction" ] ; then
      RELEASE_TYPE="production"
    fi
  fi
fi

if [ "X${PLATFORM}" = "X" ] ; then
echo "PLATFORM not defined"
PLATFORM=`arch`
fi

if [ "X${FLAVOR}" = "X" ] ; then
echo "FLAVOR not defined"
PY_OS=`python -c "import platform; import sys; sys.stdout.write(platform.linux_distribution()[0].strip())"`
PY_OS_VER_MAJ=`python -c "import platform; import sys; sys.stdout.write(platform.linux_distribution()[1].split('.')[0])"`
if [ "X${PY_OS}" = "Xdebian" ] ; then
FLAVOR="debian/${PY_OS_VER_MAJ}"
fi
if [ "X${PY_OS}" = "XScientific Linux" ] ; then
FLAVOR="scientific/${PY_OS_VER_MAJ}"
fi
if [ "X${PY_OS}" = "XopenSUSE" ] ; then
FLAVOR="openSUSE/${PY_OS_VER_MAJ}"
fi
if [ "X${PY_OS}" = "XFedora" ] ; then
FLAVOR="Fedora/${PY_OS_VER_MAJ}"
fi

fi
if [ "X${FLAVOR}" = "X" ] ; then
echo "No flavour defined"
FLAVOR="${PY_OS}/${PY_OS_VER_MAJ}"
fi

if [ "X${RELEASE_TYPE}" = "X" ] ; then
echo "No RELEASE_TYPE defined"
sleep 1
exit 1
fi


if [ "X${DIR_EXPORT_TGZ}" = "X" ] ; then
DIR_EXPORT_TGZ="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/src/tgz"
fi
if [ "X${DIR_EXPORT_BTGZ}" = "X" ] ; then
DIR_EXPORT_BTGZ="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/tgz"
fi
if [ "X${DIR_EXPORT_DPKG}" = "X" ] ; then
DIR_EXPORT_DPKG="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/dpkg"
fi

export DIR_EXPORT_TGZ
export DIR_EXPORT_BTGZ
export DIR_EXPORT_DPKG

mkdir -p ${DIR_EXPORT_TGZ}
mkdir -p ${DIR_EXPORT_BTGZ}
mkdir -p ${DIR_EXPORT_DPKG}
