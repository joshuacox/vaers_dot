#!/usr/bin/env bash
CWD=$(pwd)
SOURCE=${CWD}/new_data
DEST=${CWD}/data
rm -rfv ${DEST}
mkdir -p ${DEST}
if [[ $# -eq 1 ]]; then
  COUNT=$1
elif [[ $# -eq 0 ]]; then
  COUNT=100
  #set -x
else
  echo "wrong number of args $#"
  exit 1
fi
for i in $(find ${SOURCE} -iname '2019*csv')
do 
  #full_path="/home/user/documents/report.pdf"
  #full_path=$i

  # Extract the directory path
  #path="${full_path%/*}"

  # Extract the full filename (including extension)
  #filename="${full_path##*/}"

  # Extract the filename without the extension
  #filename_no_ext="${filename%.*}"

  # Extract the extension
  #extension="${filename##*.}"

  # echo "Path: $path"
  # echo "Filename: $filename"
  # echo "Filename without extension: $filename_no_ext"
  # echo "Extension: $extension"
  filename="${i##*/}"
  # echo "head -n${COUNT} $i > ${DEST}/$filename"
  head -n${COUNT} $i > ${DEST}/$filename
done
#rm data/AllVAERSDataCSVS.zip
du -sh data
