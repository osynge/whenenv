#UUID=aa42ca85-179b-4873-b12e-32d549bf02b6
UUID="aa7016b0-6508-41d2-bce0-c1724cb3d3e2"
UUID_Overlay="333fe448-28c9-44da-a9cb-402818d433bb"
set +e
export CHROOT="/workspace/chroot"
chrootbuilder \
  --input \
  /var/cache/vmcatcher/endorsed/${UUID} \
  --dest  ${CHROOT} \
  --overlay /var/cache/vmcatcher/endorsed/${UUID_Overlay} \
  --build

#UUID=aa42ca85-179b-4873-b12e-32d549bf02b6
UUID=aa7016b0-6508-41d2-bce0-c1724cb3d3e2
UUID_Overlay=333fe448-28c9-44da-a9cb-402818d433bb
python /root/chrootbuilder   --input   /var/cache/vmcatcher/endorsed/${UUID}   --dest  ${CHROOT}   --overlay /var/cache/vmcatcher/endorsed/${UUID_Overlay}   --build
CHROOT="/workspace/document-production/chroot"
export CHROOT=$CHROOT
echo $CHROOT
set -e
chrootbuilder   --input   /var/cache/vmcatcher/endorsed/${UUID}   --dest  ${CHROOT}   --overlay /var/cache/vmcatcher/endorsed/${UUID_Overlay}   --build
