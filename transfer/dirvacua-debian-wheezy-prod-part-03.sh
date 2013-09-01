if [ "X" = "X${CHROOT}" ]
then 
    echo "No CHROOT set"
    exit 1
fi
chroot ${CHROOT}
set -x
set -e
export http_proxy=http://squid:3128
apt-get install git \
    python \
    rpm \
    make \
    python-setuptools \
    python-m2crypto  \
    -y
