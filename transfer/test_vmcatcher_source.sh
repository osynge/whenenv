#SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.hepix.testing.hepixvmitrust/trunk"
GIT_SRC="git://git.fritz.box/imagelist_functional_tests.git"
GIT_DEST="build"
GIT_TAG_FILTER="-"
BUILD_DEPS_RPM="git \
    python \
    rpm-build \
    make \
    org-desy-grid-virt-sort-release \
    openssl-devel \
    python-devel \
    pkgconfig \
    swig \
    gcc \
    pexpect \
    lcg-CA \
    ca_BitFace \
    fetch-crl \
    vmcatcher \
    ntp\
"
REPOSITORY_TYPE="public"
BUILD_TYPE="disttools"
export GIT_SRC
export GIT_DEST
export GIT_TAG_FILTER
export BUILD_DEPS_RPM
export REPOSITORY_TYPE
export BUILD_TYPE
