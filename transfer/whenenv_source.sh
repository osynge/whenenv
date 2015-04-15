#GIT_SRC="git://git.fritz.box/yokel_jenkins.git"
GIT_SRC="https://github.com/osynge/whenenv.git"
GIT_DEST="build"
GIT_TAG_FILTER="whenenv-"
RPM_DEPENDS="bash"
#REPOSITORY_TYPE="private"
REPOSITORY_TYPE="public"
BUILD_TYPE="disttools"
TESTS="nosetests"
export GIT_SRC
export GIT_DEST
export GIT_TAG_FILTER
export RPM_DEPENDS
export REPOSITORY_TYPE
export BUILD_TYPE
export TESTS
