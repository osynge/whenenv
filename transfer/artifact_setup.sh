if [ "X${DIR_ART_ROOT}" = "X" ] ; then
DIR_ART_ROOT=`pwd`/artifacts
echo "DIR_ART_ROOT is defaulted as ${DIR_ART_ROOT}"
fi
export DIR_ART_ROOT

if [ "X${DIR_ART_SRPMS}" = "X" ] ; then
DIR_ART_SRPMS="${DIR_ART_ROOT}/pkg/srpm"
echo "DIR_ART_SRPMS is defaulted as ${DIR_ART_SRPMS}"
fi
export DIR_ART_SRPMS

if [ "X${DIR_ART_RPMS}" = "X" ] ; then
DIR_ART_RPMS="${DIR_ART_ROOT}/pkg/rpm"
echo "DIR_ART_RPMS is defaulted as ${DIR_ART_RPMS}"
fi
export DIR_ART_RPMS

if [ "X${DIR_ART_BIN}" = "X" ] ; then
DIR_ART_BIN="${DIR_ART_ROOT}/bin"
echo "DIR_ART_BIN is defaulted as ${DIR_ART_BIN}"
fi
export DIR_ART_BIN

if [ "X${DIR_ART_SRC}" = "X" ] ; then
echo "DIR_RPM_RPMS not defined"
DIR_ART_SRC="${DIR_ART_ROOT}/src"
echo "DIR_ART_SRC is defaulted as ${DIR_ART_SRC}"
fi
export DIR_ART_SRC

rm -rf ${DIR_ART_SRPMS}
rm -rf ${DIR_ART_RPMS}
rm -rf ${DIR_ART_BIN}
rm -rf ${DIR_ART_SRC}

mkdir -p ${DIR_ART_SRPMS}
mkdir -p ${DIR_ART_RPMS}
mkdir -p ${DIR_ART_BIN}
mkdir -p ${DIR_ART_SRC}
