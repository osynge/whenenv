set -x
export CROOT_DIR="/root/sl6"
python /root/chrootbuilder \
--input \
/var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
--dest ${CROOT_DIR} \
--overlay  /var/cache/vmcatcher/endorsed/6b9384e5-5923-4d47-aaab-0fde0c52f8b8 \
--build
