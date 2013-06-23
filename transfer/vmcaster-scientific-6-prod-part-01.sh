export CROOT_DIR="/root/sl6"

python /root/chrootbuilder \
--input \
/var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
--dest  /root/sl6 \
--overlay /root/overlay.cpio.bz2 \
--build
