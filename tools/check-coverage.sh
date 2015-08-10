level=$1
shift
dir=$2
shift

cd "$dir"
python setup.py testr --coverage --testr-args="$*"

cover=$(fgrep "'pc_cov'" cover/index.html | sed 's/.*>\([0-9]*\)%..*/\1/')

echo "Coverage: ${cover}%"

if [ "$cover" -lt "$level" ]; then
    echo "Expecting ${level}%. Aborting."
    exit 1
fi

# check-coverage.sh ends here
