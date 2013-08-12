pwd
if [ "X${ROOTDIR}" = "X" ] ; then
    echo "ROOTDIR not defined"
    ROOTDIR="/tmp/repo"
    #exit 1
fi
if [ "X${REPOSITORY_TYPE}" = "Xpublic" ] ; then
ROOTDIR="/tmp/public_repo"
fi
if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
ROOTDIR="/tmp/private_repo"
fi

tar -zxvf artifacts.tgz
rm -f artifacts.tgz
RELEASE_TYPE="release"
PLATFORM="x86_64"
FLAVOR="debian"
mkdir -p ${ROOTDIR}
dir_tgz="${ROOTDIR}/${RELEASE_TYPE}/source/${FLAVOR}/7/tgz/"
dir_btgz="${ROOTDIR}/${RELEASE_TYPE}/${PLATFORM}/${FLAVOR}/7/tgz/"
mkdir -p ${dir_tgz}
mkdir -p ${dir_btgz}
/usr/bin/rsync -v --ignore-existing build/dist/*.src.tar.gz \
    ${dir_tgz}
rm -rf build/dist/*src.tar.gz
/usr/bin/rsync -v --ignore-existing build/dist/*.bin.tar.gz \
    ${dir_btgz}
rm -rf build/dist/*bin.tar.gz
