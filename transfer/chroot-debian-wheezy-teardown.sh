function ycheckrc () {
echo $@
$@
rc=$?
if [ $[${rc}] != 0 ] ; then
    exit ${rc}
fi
}

ycheckrc mv chroot/build/artifacts.tgz .

python /root/chrootbuilder \
  --dest  chroot \
  --clean
