set -x
export CROOT_DIR="/root/sl6"
python /root/chrootbuilder \
--input \
/var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
--dest ${CROOT_DIR} \
--overlay  /var/cache/vmcatcher/endorsed/bba0d5e8-3c70-49e0-8479-a42278aea120 \
--build