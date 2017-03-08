if [ "X${DIR_EXPORT_SRPM}" = "X" ] ; then
echo "DIR_EXPORT_SRPM not defined"
sleep 1
exit 1
fi


if [ "X${DIR_ART_SRPMS}" = "X" ] ; then
echo "DIR_ART_SRPMS not defined"
sleep 1
exit 1
fi

mkdir -p ${DIR_EXPORT_SRPM}

set +e
files_art_srpm=$(ls ${DIR_ART_SRPMS}/*.rpm)
set -e
if [ "X${files_art_srpm}" != "X" ] ; then
for art_bin in $files_art_srpm
do
/usr/bin/rsync -v --ignore-existing ${art_bin} ${DIR_EXPORT_SRPM}
done
fi
