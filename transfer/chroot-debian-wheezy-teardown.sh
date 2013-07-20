function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}

ycheckrc python /root/chrootbuilder \
  --dest  ${CHROOT}  \
  --clean
