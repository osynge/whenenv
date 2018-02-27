if [ "X${DIR_EXPORT_ROOT}" = "X" ] ; then
    echo "DIR_EXPORT_ROOT not defined"
    sleep 10
    exit 1
fi
if [ "X${RELEASE_FLAVOR}" = "X" ] ; then
    echo "RELEASE_FLAVOR not defined"
    sleep 10
    exit 1
fi



tar -zxvf artifacts.tgz
rm -f artifacts.tgz




RELEASE_TYPE="nightly"
#if "X$RELEASE" == "Xdevelopment" then
#    RELEASE_TYPE="nightly"
#fi
if [ "X$RELEASE" = "Xproduction" ] ; then
    RELEASE_TYPE="release"
fi

PLATFORM="x86_64"
mkdir -p ${DIR_EXPORT_ROOT}
dir_tgz="${DIR_EXPORT_ROOT}/${FLAVOR}/${RELEASE_TYPE}/src/tgz"
dir_btgz="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/tgz"
mkdir -p ${dir_tgz}
mkdir -p ${dir_btgz}
/usr/bin/rsync -v --ignore-existing build/dist/*.src.tar.gz \
    ${dir_tgz}
rm -rf build/dist/*src.tar.gz
/usr/bin/rsync -v --ignore-existing build/dist/*.bin.tar.gz \
    ${dir_btgz}
rm -rf build/dist/*bin.tar.gz

