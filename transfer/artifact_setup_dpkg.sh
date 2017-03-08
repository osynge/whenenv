if [ "X${DIR_ART_ROOT}" = "X" ] ; then
DIR_ART_ROOT=`pwd`/artifacts
echo "DIR_ART_ROOT is defaulted as ${DIR_ART_ROOT}"
fi
export DIR_ART_ROOT

if [ "X${DIR_ART_DPKG}" = "X" ] ; then
DIR_ART_DPKG="${DIR_ART_ROOT}/pkg/dpkg"
echo "DIR_ART_DPKG is defaulted as ${DIR_ART_DPKG}"
fi
export DIR_ART_DPKG

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

rm -rf ${DIR_ART_DPKG}
rm -rf ${DIR_ART_BIN}
rm -rf ${DIR_ART_SRC}

mkdir -p ${DIR_ART_DPKG}
mkdir -p ${DIR_ART_BIN}
mkdir -p ${DIR_ART_SRC}
