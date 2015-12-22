#!/bin/bash
#This script generates an auto-extractible which contains ristretto freeze code
#It is generated with makeself command

version='15.02'
tool_name=ristretto

CUST=$1
gui_folder='./build/RISTRETTO_GUI'
ARCH=$( getconf LONG_BIT)

mkdir -p ./release/$CUST

python createRistrettoExe.py $gui_folder ForLinux || exit 1
python createArchive.py $CUST $gui_folder ForLinux || exit 1
python createExeLinux.py build || exit 1

makeself $gui_folder ./release/$CUST/$tool_name\_lx$ARCH.run "Ristretto $version" ./ristretto/ristretto_core || exit 1

rm -rf build/

cd ./release/$CUST/
mkdir -p $tool_name$version/DEBIAN
mkdir -p $tool_name$version/usr/local/bin
cp -a $tool_name\_lx$ARCH.run $tool_name$version/usr/local/bin/ristretto_lx

echo "\
Package: Ristretto
Version: $version
Section: base
Priority: optional
Architecture: amd64
Maintainer: Hugo Dupras <hdupras@nvidia.com>
Description: Ristretto" > $tool_name$version/DEBIAN/control

dpkg-deb --build $tool_name$version $tool_name$version\_lx$ARCH.deb

rm -rf $tool_name$version $tool_name\_lx$ARCH.run

rm -rf $gui_folder

