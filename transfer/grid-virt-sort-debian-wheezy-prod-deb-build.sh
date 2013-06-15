set -x	

chroot chroot
id
hostname -fS
dirStart=`pwd`
rm -f artifacts.tgz *.dsc *.deb 
GITLOCATION="git://github.com/osynge/deb-grid-virt-sort.git"
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
tar -zcvf artifacts.tgz build/*.deb *.dsc

