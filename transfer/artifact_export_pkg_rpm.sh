if [ "X${DIR_EXPORT_RPM}" = "X" ] ; then
echo "DIR_EXPORT_RPM not defined"
sleep 1
exit 1
fi


if [ "X${DIR_ART_RPMS}" = "X" ] ; then
echo " not defined"
sleep 1
exit 1
fi

mkdir -p ${DIR_EXPORT_RPM}

set +e
files_art_rpm=$(ls ${DIR_ART_RPMS}/*.rpm)
set -e
if [ "X${files_art_rpm}" != "X" ] ; then
for art_rpm in $files_art_rpm
do
/usr/bin/rsync -v --ignore-existing ${art_rpm} ${DIR_EXPORT_RPM}
done
fi
