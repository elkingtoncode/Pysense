level=$1
shift
tmpfile=$(mktemp)

cleanup() {
    rm -f $tmpfile
}

trap cleanup 0

pylint "$@" | tee $tmpfile

score=$(sed -n 's@.*rated at \([0-9.]*\)/10.*@\1@p' < $tmpfile)

if [ "$(echo "$score >= $level" | bc)" -eq 1 ]; then
    exit 0
else
    exit 1
fi

# check-pylint-score.sh ends here
