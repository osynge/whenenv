pwd
if [ "X${REPOSITORY_TYPE}" = "Xprivate" ] ; then
ROOTDIR="/tmp/private_repo"
fi
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
FLAVOR="debian/7"
mkdir -p ${ROOTDIR}
dir_tgz="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/src/tgz"
dir_btgz="${ROOTDIR}/${FLAVOR}/${RELEASE_TYPE}/${PLATFORM}/tgz"
mkdir -p ${dir_tgz}
mkdir -p ${dir_btgz}
/usr/bin/rsync -v --ignore-existing build/dist/*.src.tar.gz \
    ${dir_tgz}
rm -rf build/dist/*src.tar.gz
/usr/bin/rsync -v --ignore-existing build/dist/*.bin.tar.gz \
    ${dir_btgz}
rm -rf build/dist/*bin.tar.gz

