if [ "X${RELEASE_ENV}" = "X" ] ; then
  echo "Atempting to default by RELEASE_ENV"
  if [ "X${RELEASE}" != "X" ] ; then
    RELEASE_ENV="nightly/master"
    if [ "X${RELEASE}" = "Xproduction" ] ; then
      RELEASE_ENV="production"
    fi
  else
    RELEASE_ENV="nightly/master"
  fi
  if [ "X${BRANCH}" != "X" ] ; then
    echo "release type defaulted from BRANCH"
    RELEASE_ENV="nightly/${BRANCH}"
  fi
fi
export RELEASE_ENV
