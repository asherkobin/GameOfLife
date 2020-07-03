import subprocess

def get_clipboard_text():
  process = subprocess.run("pbpaste", check=True, stdout=subprocess.PIPE, universal_newlines=True)
  text = process.stdout

  return text