if [ "X${DIR_EXPORT_TGZ}" = "X" ] ; then
echo "DIR_EXPORT_TGZ not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_SRC}" = "X" ] ; then
echo "DIR_ART_SRC not defined"
sleep 1
exit 1
fi

mkdir -p ${DIR_EXPORT_TGZ}

set +e
files_art_src=$(ls ${DIR_ART_SRC}/*.src.tar.gz)
set -e
if [ "X${files_art_src}" != "X" ] ; then
for art_src in $files_art_src
do
  /usr/bin/rsync -v --ignore-existing ${art_src} ${DIR_EXPORT_TGZ}
done
fi
