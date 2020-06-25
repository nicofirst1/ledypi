

function upload_all() {
  echo "Loading website"
  ampy rmdir website
  ampy put website

  echo "Loading config"
  ampy rm config
  ampy put config

  for entry in *.py
    do
      echo "Loading $entry..."
      ampy rm $entry
      ampy put $entry
    done

  echo "Esp32 content:"
  ampy ls

}

function upload() {
  echo "Uploading $1"
  ampy rm $1
  ampy put $1

}
