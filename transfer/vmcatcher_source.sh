GIT_SRC="git://github.com/hepix-virtualisation/vmcatcher.git"
GIT_DEST="build"
GIT_TAG_FILTER="vmcatcher-"
RPM_DEPENDS="smimeX509validation hepixvmitrust python-sqlalchemy fetch-crl"
REPOSITORY_TYPE="public"
BUILD_TYPE="disttools"
export GIT_SRC
export GIT_DEST
export GIT_TAG_FILTER
export RPM_DEPENDS
export REPOSITORY_TYPE
export BUILD_TYPE
