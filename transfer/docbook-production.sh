function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}

SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.hepix.virtulization.docs/trunk"
#TAG=`svn ls ${SVNLOCATION} | org_desy_grid_virt_sort_release.py | tail -n 1`
rm -rf build
#svn co ${SVNLOCATION}/${TAG} build
pwd

ycheckrc svn co ${SVNLOCATION} build
#exit 1
cd build
ycheckrc make html

ycheckrc make pdf

cd ..
rm -f artifacts.tgz
ycheckrc tar -zcvf artifacts.tgz build/*.pdf build/Book
frog="foo"
export frog
