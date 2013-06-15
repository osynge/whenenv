chroot chroot
id
hostname -f
rm -f artifacts.tgz
GITLOCATION="git@github.com:osynge/deb-grid-virt-sort.git"
rm -rf build
git clone ${GITLOCATION} build
cd build
git checkout upstream
git pull
git checkout pristine-tar
git pull
git checkout master
git pull
git-buildpackage
