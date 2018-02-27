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
RELEASE_TYPE="development"
PLATFORM="x86_64"
mkdir -p ${DIR_EXPORT_ROOT}
dir_tgz="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_TYPE}/src/tgz"
dir_btgz="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/tgz"
dir_srpm="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_TYPE}/src/srpm"
dir_rpm="${DIR_EXPORT_ROOT}/${RELEASE_FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/rpm"
mkdir -p ${dir_tgz}
mkdir -p ${dir_btgz}
mkdir -p ${dir_srpm}
mkdir -p ${dir_rpm}
/usr/bin/rsync -v --ignore-existing build/dist/*.src.tar.gz \
    ${dir_tgz}
rm -rf build/dist/*src.tar.gz
/usr/bin/rsync -v --ignore-existing build/dist/*.bin.tar.gz \
    ${dir_btgz}
rm -rf build/dist/*bin.tar.gz
set +e
files_srpm=$(ls build/dist/*.src.rpm)
set -e
if [ $files_srpm ] ; then
  /usr/bin/rsync -v --ignore-existing build/dist/*.src.rpm \
    ${dir_srpm}
  rm -rf build/dist/*.src.rpm
fi

set +e
files_rpm=$(ls build/dist/*.rpm ${DIR_ART_RPMS}/*.rpm)
set -e
if [ "X${files_rpm}" != "X" ] ; then
for art_bin in $files_rpm
do
/usr/bin/rsync -v --ignore-existing ${art_bin} ${dir_rpm}
  rm -f ${art_bin}
done
fi
