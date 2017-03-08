if [ "X${DIR_EXPORT_DPKG}" = "X" ] ; then
echo "DIR_EXPORT_DPKG not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_DPKG}" = "X" ] ; then
echo "DIR_ART_DPKG not defined"
sleep 1
exit 1
fi

mkdir -p ${DIR_EXPORT_DPKG}

set +e
files_art_bin=$(ls ${DIR_ART_DPKG}/*.deb)
set -e
if [ "X${files_art_bin}" != "X" ] ; then
for art_bin in $files_art_bin
do
/usr/bin/rsync -v --ignore-existing ${art_bin} ${DIR_EXPORT_DPKG}
done
fi
