if [ "X${DIR_EXPORT_BTGZ}" = "X" ] ; then
echo "DIR_EXPORT_BTGZ not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_BIN}" = "X" ] ; then
echo "DIR_ART_BIN not defined"
sleep 1
exit 1
fi

mkdir -p ${DIR_EXPORT_BTGZ}

set +e
files_art_bin=$(ls ${DIR_ART_BIN}/*.bin.tar.gz)
set -e
if [ "X${files_art_bin}" != "X" ] ; then
for art_bin in $files_art_bin
do
/usr/bin/rsync -v --ignore-existing ${art_bin} ${DIR_EXPORT_BTGZ}
done
fi
