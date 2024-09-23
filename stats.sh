#!/bin/bash

count_incidence () {
  echo $( cat data/${1}VAERSDATA.csv \
    |csvcut -c${2} -e'latin-1' \
    |column -t -s',' \
    |grep -v '^""$'\
    |wc -l \
    |awk '{print $1}')
}
calc_perc () {
  echo "scale=2;$1/$2*100" | bc
}
printerrr () {
  printf " %7s - %7s / %7s = %7s%%" $1 $2 $total $(calc_perc $2 $total)
}

for i in {1990..2024}; do
  RPT_DATE=$(count_incidence $i 8)
  VAX_DATE=$(count_incidence $i 19)
  ONSET_DATE=$(count_incidence $i 20)
  total=$( wc -l data/${i}VAERSDATA.csv|awk '{print $1}')
  printf "%7s - " $i
  printerrr 'VAX' $VAX_DATE
  printerrr 'RPT' $RPT_DATE
  printerrr 'ONSET' $ONSET_DATE
  echo ''
done

