pwd
if [ "X${ROOTDIR}" = "X" ] ; then
    echo "ROOTDIR not defined"
    ROOTDIR="/tmp/repo"
    #exit 1
    if [ "X${REPOSITORY_TYPE}" = "Xpublic" ] ; then
        ROOTDIR="/tmp/public_repo"
    fi
    if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
        ROOTDIR="/tmp/private_repo"
    fi
fi
tar -zxvf artifacts.tgz
rm -f artifacts.tgz
RELEASE_TYPE="development"
PLATFORM="x86_64"
FLAVOR="scientific"
mkdir -p ${ROOTDIR}
dir_tgz="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/source/6/tgz"
dir_btgz="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/6/tgz"
dir_srpm="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/source/6/srpm"
dir_rpm="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/6/rpm"
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

/usr/bin/rsync -v --ignore-existing build/dist/*.src.rpm \
    ${dir_srpm}
rm -rf build/dist/*.src.rpm
/usr/bin/rsync -v --ignore-existing build/dist/*.rpm \
    ${dir_rpm}
rm -rf build/dist/*.rpm
