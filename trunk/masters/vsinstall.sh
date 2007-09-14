#!/bin/sh
ARG=$1
SETUPARG=${ARG:="nosetup"}
CURPWD=$PWD

VERSION=`head -1 $CURPWD/../Version.txt`
mkdir -p $HOME/$VERSION
cd $HOME/$VERSION
mkdir -p $HOME/$VERSION/save
mkdir -p $HOME/$VERSION/serialized_xml
mkdir -p $HOME/$VERSION/serialized_xml/New_Game
cp $CURPWD/../New_Game $HOME/$VERSION/save/
cp $CURPWD/../Llama.begin.csv $HOME/$VERSION/serialized_xml/New_Game/
echo "a"
if test \( $CURPWD/../setup.config -nt $HOME/$VERSION/setup.config \) -o \! \( -e ~/.privgold100/setup.config \) ; then
  cp $CURPWD/../setup.config .
echo "aa"
fi
echo "b"
if test \( $CURPWD/../vegastrike.config -nt $HOME/.openalrc \) -o \! \( -e $HOME/.openalrc \) ; then
  echo "(define devices '(arts esd native))">>$HOME/.openalrc
echo "bb"
fi
echo "c"
if test \( $CURPWD/../vegastrike.config -nt $HOME/$VERSION/vegastrike.config \) -o \! \( -e $HOME/$VERSION/vegastrike.config \) ; then
  cp $CURPWD/../vegastrike.config .
  $CURPWD/setup
echo "cc"
fi
if [ $SETUPARG = "setup" ] || [ $SETUPARG = "--setup" ]; then
   echo "d"
   $CURPWD/setup
else
  cd $CURPWD
  ./vegastrike
fi
