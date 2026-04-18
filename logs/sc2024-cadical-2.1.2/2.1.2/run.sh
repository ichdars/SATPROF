#!/bin/sh
msg () {
  printf "c run.sh: %-20s %s\n" "$1" "$2"
}
index=$1
benchmark="`awk '$1 == "'$index'"{print $2}' benchmarks`"
path="$HOME/data/cnf/sc2024/$benchmark.cnf.xz"
exec 1>"$benchmark".log 2>"$benchmark".err
msg index "$index"
msg benchmark "$benchmark"
msg path "$path"
msg job "$SLURM_ARRAY_JOB_ID"
msg task "$SLURM_ARRAY_TASK_ID"
msg host "`hostname`"
msg cpu "`lscpu|grep 'Model name:'|sed -e 's,^Model name: *,,'`"
msg os "`uname -a`"
unzipped="$TMP/local-unzipped-${SLURM_ARRAY_JOB_ID}-${SLURM_ARRAY_TASK_ID}-${index}-${benchmark}.cnf"
trap "rm -f $unzipped" 2 3 9 15
msg unzipping "`date`"
xz -c -d $path > $unzipped
msg unzipped "`date`"
binary=./binary
runlim \
  --single \
  --real-time-limit=5000 \
  --space-limit=7000 \
  "$binary" \
  "$unzipped" \
  -n --stats
msg finished "`date`"
rm -f "$unzipped"
msg cleaned "`date`"
