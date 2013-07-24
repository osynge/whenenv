pwd
if [ "X${ROOTDIR}" = "X" ] ; then
    echo "ROOTDIR not defined"
    ROOTDIR="/tmp/repo"
    #exit 1
fi
tar -zxvf artifacts.tgz
rm -f artifacts.tgz
#ROOTDIR="/export/yokel.org/"
mkdir -p ${ROOTDIR}
dir_tgz="${ROOTDIR}release/source/scientific/6x/tgz"
dir_srpm="${ROOTDIR}/release/x86_64/scientific/6x/srpm"
dir_rpm="${ROOTDIR}/release/x86_64/scientific/6x/rpm"
mkdir -p ${dir_tgz}
mkdir -p ${dir_srpm}
mkdir -p ${dir_rpm}
/usr/bin/rsync -v --ignore-existing build/dist/*.tar.gz \
    ${dir_tgz}
rm -rf build/dist/*.tar.gz
/usr/bin/rsync -v --ignore-existing build/dist/*.src.rpm \
    ${dir_srpm}
rm -rf build/dist/*.src.rpm
/usr/bin/rsync -v --ignore-existing build/dist/*.rpm \
    ${dir_rpm}
rm -rf build/dist/*.rpm
