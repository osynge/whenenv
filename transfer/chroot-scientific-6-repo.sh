rm -rf sl6.cpio.bz2
wget --quiet ${HUDSON_URL}/job/GenChroot.SL-6X/lastSuccessfulBuild/artifact/sl6.cpio.bz2
su exporter -c"vmcaster \
   --database sqlite:////var/lib/vmcaster/local.db \
   --upload-image sl6.cpio.bz2 \
   --select-image aa42ca85-179b-4873-b12e-32d549bf02b6 \
   --verbose    --verbose"
rm -rf sl6.cpio.bz2
