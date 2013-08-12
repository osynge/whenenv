#SVN_SRC="https://svnsrv.desy.de/public/grid-virt/org.desy.grid-virt.sort.release/"
#SVN_DEST="build"
RPM_DEPENDS="python"
#export SVN_SRC
#export SVN_DEST
#export SVN_TAG_FILTER


GIT_SRC="git://github.com/osynge/grid_version_sort.git"
GIT_DEST="build"
GIT_TAG_FILTER="grid_virt_sort-"
REPOSITORY_TYPE="public"
BUILD_TYPE="disttools"
export GIT_SRC
export GIT_DEST
export GIT_TAG_FILTER
export RPM_DEPENDS
export REPOSITORY_TYPE
export BUILD_TYPE
