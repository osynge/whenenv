pwd


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

if [ "X${DIR_EXPORT_TGZ}" = "X" ] ; then
echo "DIR_EXPORT_TGZ not defined"
sleep 1
exit 1
fi

if [ "X${DIR_EXPORT_BTGZ}" = "X" ] ; then
echo "DIR_EXPORT_BTGZ not defined"
sleep 1
exit 1
fi

if [ "X${DIR_EXPORT_SRPM}" = "X" ] ; then
echo "DIR_EXPORT_SRPM not defined"
sleep 1
exit 1
fi

if [ "X${DIR_EXPORT_RPM}" = "X" ] ; then
echo "DIR_EXPORT_RPM not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_BIN}" = "X" ] ; then
echo "DIR_RPM_SRPMS not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_SRC}" = "X" ] ; then
echo "DIR_RPM_SRPMS not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_SRPMS}" = "X" ] ; then
echo " not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_RPMS}" = "X" ] ; then
echo " not defined"
sleep 1
exit 1
fi

if [ "X${PLATFORM}" = "X" ] ; then
echo "PLATFORM not defined"
PLATFORM=`arch`
fi


if [ "X${FLAVOR}" = "X" ] ; then
echo "FLAVOR not defined"
FLAVOR=${OPERATING_SYSTEM}
fi

mkdir -p ${DIR_EXPORT_TGZ}
mkdir -p ${DIR_EXPORT_BTGZ}
mkdir -p ${DIR_EXPORT_SRPM}
mkdir -p ${DIR_EXPORT_RPM}

set +e
files_art_src=$(ls ${DIR_ART_SRC}/*.src.tar.gz)
set -e
if [ "X${files_art_src}" != "X" ] ; then
for art_src in $files_art_src
do
  /usr/bin/rsync -v --ignore-existing ${art_src} ${DIR_EXPORT_TGZ}
done
fi
set +e
files_art_bin=$(ls ${DIR_ART_BIN}/*.bin.tar.gz)
set -e
if [ "X${files_art_bin}" != "X" ] ; then
for art_bin in $files_art_bin
do
/usr/bin/rsync -v --ignore-existing ${art_bin} ${DIR_EXPORT_BTGZ}
done
fi

set +e
files_art_srpm=$(ls ${DIR_ART_SRPMS}/*.rpm)
set -e
if [ "X${files_art_srpm}" != "X" ] ; then
for art_bin in $files_art_srpm
do
/usr/bin/rsync -v --ignore-existing ${art_bin} ${DIR_EXPORT_SRPM}
done
fi

set +e
files_art_rpm=$(ls ${DIR_ART_RPMS}/*.rpm)
set -e
if [ "X${files_art_rpm}" != "X" ] ; then
for art_rpm in $files_art_rpm
do
/usr/bin/rsync -v --ignore-existing ${art_rpm} ${DIR_EXPORT_RPM}
done
fi
