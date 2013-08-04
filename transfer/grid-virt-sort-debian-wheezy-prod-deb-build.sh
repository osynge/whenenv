set -x	
hostname -f
dirStart=`pwd`
rm -f artifacts.tgz *.dsc *.deb 
GITLOCATION="https://github.com/osynge/deb-grid-virt-sort.git"
rm -rf build
cmd="git clone ${GITLOCATION} build/gitclone"
echo $cmd
$cmd
cd build/gitclone
git checkout upstream
git pull
git checkout pristine-tar
git pull
git checkout master
git pull
echo `git-buildpackage`
cd ${dirStart}
rm -f artifacts.tgz
rm -fr   build/gitclone/ build/*.build
tar -zcvf artifacts.tgz build/*

