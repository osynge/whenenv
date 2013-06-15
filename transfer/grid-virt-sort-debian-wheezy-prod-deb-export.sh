rm -rf build
tar -zxvf artifacts.tgz
rm -f artifacts.tgz
ROOTDIR="/export/yokel.org/"
RELEASE_TYPE="release"
PLATFORM="x86_64"
FLAVOR="debian"
VERSION="7.0"
mkdir -p ${ROOTDIR}
dir_tgz="${ROOTDIR}/${RELEASE_TYPE}/source/${FLAVOR}/${VERSION}/tgz/"
dir_btgz="${ROOTDIR}/${RELEASE_TYPE}/${PLATFORM}/${FLAVOR}/${VERSION}/tgz/"
dir_srpm="${ROOTDIR}/${RELEASE_TYPE}/${PLATFORM}/${FLAVOR}/${VERSION}/srpm/"
dir_rpm="${ROOTDIR}/${RELEASE_TYPE}/${PLATFORM}/${FLAVOR}/${VERSION}/rpm/"
mkdir -p ${dir_tgz}
mkdir -p ${dir_btgz}
#mkdir -p ${dir_srpm}
#mkdir -p ${dir_rpm}
ls build/*
/usr/bin/rsync -v --ignore-existing build/dist/*.src.tar.gz \
    ${dir_tgz}
rm -rf build/dist/*src.tar.gz
/usr/bin/rsync -v --ignore-existing build/dist/*.bin.tar.gz \
    ${dir_btgz}
rm -rf build/dist/*bin.tar.gz

#/usr/bin/rsync -v --ignore-existing build/dist/*.src.rpm \
#    ${dir_srpm}
#rm -rf build/dist/*.src.rpm
#/usr/bin/rsync -v --ignore-existing build/dist/*.rpm \
#    ${dir_rpm}
#rm -rf build/dist/*.rpm
