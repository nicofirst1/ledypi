path2repo="$(dirname $(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd))"

echo "Path to ledypi is : $path2repo"

pythonpath="$path2repo/src:$path2repo/audio-reactive-led-strip/src:$path2repo/ledyweb"
export PYTHONPATH="$pythonpath"
