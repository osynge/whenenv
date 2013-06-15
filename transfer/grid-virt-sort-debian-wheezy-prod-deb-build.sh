set -x	

chroot chroot
id
hostname -fS
rm -f artifacts.tgz *.dsc *.deb 
GITLOCATION="git://github.com/osynge/deb-grid-virt-sort.git"
rm -rf build
cmd="git clone ${GITLOCATION} build"
echo $cmd
$cmd
cd build
git checkout upstream
git pull
git checkout pristine-tar
git pull
git checkout master
git pull
echo `git-buildpackage`
rm -f artifacts.tgz
tar -zcvf artifacts.tgz *.deb *.dsc

