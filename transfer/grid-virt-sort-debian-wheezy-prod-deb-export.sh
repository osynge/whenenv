set -x
rm -rf build
tar -zxvf artifacts.tgz
rm -f artifacts.tgz
ROOTDIR="/export/yokel.org/"
RELEASE_TYPE="release"
PLATFORM="x86_64"
FLAVOR="debian"
VERSION="7.0"
mkdir -p ${ROOTDIR}
dir_deb="${ROOTDIR}/${RELEASE_TYPE}/source/${FLAVOR}/${VERSION}/packages/"
mkdir -p ${dir_deb}

ls build/*
/usr/bin/rsync -v --ignore-existing build/* \
    ${dir_deb}
