#UUID=aa42ca85-179b-4873-b12e-32d549bf02b6
UUID=aa7016b0-6508-41d2-bce0-c1724cb3d3e2
export CROOT_DIR="/root/sl6"
python /root/chrootbuilder \
  --input \
  /var/cache/vmcatcher/endorsed/${UUID} \
  --dest  chroot \
  --overlay /root/overlay.cpio.bz2 \
  --build
