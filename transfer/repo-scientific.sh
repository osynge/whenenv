ROOTDIR="/export/yokel.org/"
mkdir -p ${ROOTDIR}
dir_srpm="${ROOTDIR}/release/x86_64/scientific/6x/srpm"
dir_rpm="${ROOTDIR}/release/x86_64/scientific/6x/rpm"
mkdir -p ${dir_srpm}
mkdir -p ${dir_rpm}
createrepo ${dir_srpm}
createrepo ${dir_rpm}
dir_srpm="${ROOTDIR}/development/x86_64/scientific/6x/srpm/head"
dir_rpm="${ROOTDIR}/development/x86_64/scientific/6x/rpm/head"
mkdir -p ${dir_srpm}
mkdir -p ${dir_rpm}
dirvacua --verbose ${dir_srpm}
dirvacua --verbose ${dir_rpm}
createrepo ${dir_srpm}
createrepo ${dir_rpm}

dirvacua  --verbose /export/yokel.org//development/x86_64/scientific/6x/tgz/head/
dirvacua  --verbose /export/yokel.org/development/source/scientific/6x/tgz/head/
dir_srpm="${ROOTDIR}/prod/srpm/scientific/6/"
dir_rpm="${ROOTDIR}/prod/rpm/scientific/6/"
mkdir -p ${dir_srpm}
mkdir -p ${dir_rpm}
createrepo ${dir_srpm}
createrepo ${dir_rpm}
dir_srpm="${ROOTDIR}/unstable/srpm/scientific/6/"
dir_rpm="${ROOTDIR}/unstable/rpm/scientific/6/"
mkdir -p ${dir_srpm}
mkdir -p ${dir_rpm}
createrepo ${dir_srpm}
createrepo ${dir_rpm}
