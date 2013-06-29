function is_int() { return $(test "$@" -eq "$@" > /dev/null 2>&1); } 
function run () {
echo $@
$@
rc=$?
if $(is_int "${rc}");
then
   if [ $[${rc}] != 0 ] ; then
        exit ${rc}
   fi
fi
}


hostname -f


SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.hepix.virtulization.docs/trunk"
#TAG=`svn ls ${SVNLOCATION} | org_desy_grid_virt_sort_release.py | tail -n 1`
rm -rf build
#svn co ${SVNLOCATION}/${TAG} build
pwd

run svn co ${SVNLOCATION} build
#exit 1
cd build
run make html

run make pdf

cd ..
rm -f artifacts.tgz
run tar -zcvf artifacts.tgz build/*.pdf build/Book
frog="foo"
export frog
