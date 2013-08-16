rm -f *.orig.tar.gz
rm -f *.changes
rm -f *.build
rm -f *.debian.tar.gz
rm -f *.dsc
rm -f *.deb
rm -f *.upload
rm -rf build
ls
git clone https://github.com/osynge/deb-grid-virt-sort.git build

cd build




#lockfile-create /tmp/foo

#export ARCH=$arch
#export DIST=$distribution
#rm -f *.{deb,dsc,build,changes,gz}

#if git branch -a | grep -q origin/upstream; then
#  git branch upstream origin/upstream
#fi

#if git branch -a | grep -q "origin/$distribution"; then
#  git checkout -b "$distribution" "origin/$distribution"
#else
#  # No matter what branch triggert this build, if we don't have a
#  # special branch for this distribution, build the master branch.
#  git reset --hard origin/master
#fi

version=`awk '{gsub("[()]", ""); print $2; exit}' debian/changelog`

dch -b -v "${version}+${DIST}${BUILD_NUMBER}${ARCH}" "Yokel ${DIST} build #${BUILD_NUMBER}" --distribution $DIST
#dch --distribution ${DIST}

git commit -m"changing dist" debian/changelog
#ctrlpatrh=`find | grep control`
#cat $ctrlpatrh
#TMPDIR=/tmp/jenkins_pbuilder_${BUILD_ID}_${EXECUTOR_NUMBER}/build
#rm -rf $TMPDIR
#mkdir -p $TMPDIR
#cp -r * $TMPDIR/
#cd $TMPDIR/
#sudo env
DIST=${DIST} ARCH=${ARCH} git-buildpackage --git-builder="git-pbuilder"  --git-cleaner="fakeroot debian/rules clean"

#pdebuild --use-pdebuild-internal
dput -u yokel_public_${RELEASE} ../*.changes
#lockfile-remove /tmp/foo
