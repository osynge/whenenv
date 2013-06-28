hostname -f

SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.hepix.virtulization.docs/trunk"
#TAG=`svn ls ${SVNLOCATION} | org_desy_grid_virt_sort_release.py | tail -n 1`
rm -rf build
#svn co ${SVNLOCATION}/${TAG} build
svn co ${SVNLOCATION} build
cd build
make html
make pdf
cd ..
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/*.pdf build/Book
