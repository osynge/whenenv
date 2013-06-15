set -x	

chroot chroot
id
hostname -f
rm -f artifacts.tgz
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
