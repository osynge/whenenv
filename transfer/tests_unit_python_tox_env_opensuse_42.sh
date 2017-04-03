TOXCMD="tox -e py27 -e py34 -e flake8"
TOXDIR_PREFIX=/workspace/tox
TOXDIR="${TOXDIR_PREFIX}/executor_${EXECUTOR_NUMBER}_dir"
export TOXCMD
export TOXDIR
