if [ "X${DIR_ART_RPMS}" = "X" ] ; then
echo "DIR_ART_RPMS not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_SRPMS}" = "X" ] ; then
echo "DIR_ART_SRPMS not defined"
sleep 1
exit 1
fi

if [ "X${BUILD_SRC}" = "X" ] ; then
echo "DIR_ART_SRPMS not defined"
sleep 1
exit 1
fi

ORIGINALDIR=`pwd`
cd $BUILD_SRC
make rpm

set +e
files_art_src=$(ls RPMS/x86_64/*)
set -e
if [ "X${files_art_src}" != "X" ] ; then
for art_src in $files_art_src
do
  /usr/bin/rsync -v --ignore-existing ${art_src} ${DIR_ART_RPMS}
done
fi

set +e
files_art_src=$(ls ${DIR_ART_SRC}/*.src.tar.gz)
set -e
if [ "X${files_art_src}" != "X" ] ; then
for art_src in $files_art_src
do
  /usr/bin/rsync -v --ignore-existing ${art_src} ${DIR_ART_SRPMS}
done
fi
