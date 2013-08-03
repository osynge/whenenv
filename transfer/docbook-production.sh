function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}

echo CHROOT=$CHROOT

#SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.hepix.virtulization.docs/trunk"
GIT_SRC="git://github.com/hepix-virtualisation/hepix-virtualisation-book.git"
#TAG=`svn ls ${SVNLOCATION} | org_desy_grid_virt_sort_release.py | tail -n 1`
rm -rf build
#svn co ${SVNLOCATION}/${TAG} build
pwd
#ycheckrc svn co ${SVNLOCATION} build
git clone ${GIT_SRC} build
#exit 1
cd build
ycheckrc make html

ycheckrc make pdf

cd ..
rm -f artifacts.tgz
ycheckrc tar -zcvf artifacts.tgz build/*.pdf build/Book
frog="foo"
export frog
/etc/init.d/dbus stop
