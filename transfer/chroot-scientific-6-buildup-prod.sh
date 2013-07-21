set -x
CHROOT="/tmp/chroot/executor_${EXECUTOR_NUMBER}"
mkdir -p ${CHROOT}
rm -rf artifacts.tgz
/usr/bin/chrootbuilder \
--input \
/var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
--dest ${CHROOT} \
--overlay  /var/cache/vmcatcher/endorsed/6b9384e5-5923-4d47-aaab-0fde0c52f8b8 \
--build
export CHROOT
