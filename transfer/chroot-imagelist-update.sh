su exporter -c 'vmcaster \
   --database sqlite:////var/lib/vmcaster/local.db \
   --select-imagelist ab1754cd-7d59-4851-c333-c96cb6545aaa \
   --upload-imagelist \
   --verbose \
   --verbose && exit'
exit 0

