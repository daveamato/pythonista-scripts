import os, platform, sys

machine = platform.machine()
print 'Platform system:' + machine

if 'iP' in machine:
  BASE_DIR = os.path.expanduser('~/Documents')
else:
  BASE_DIR = os.getcwd()

GITHUB_MASTER = 'https://raw.githubusercontent.com/khilnani/pythonista/master/'
S3BACKUP_FILE = 's3backup.py'
S3CONF_FILE = 'aws.conf'

try:
  import requests as r
except ImportError:
  print('Please install: pip install requests')
  sys.exit()

def download_file(name):
  print 'Reading %s from %s' % (name, GITHUB_MASTER + name)
  file_content = r.get(GITHUB_MASTER + name).text
  print 'Writing %s' % name
  file_path = os.path.join(BASE_DIR, name)
  f = open(file_path, 'w')
  f.write(file_content)
  f.close()
  print 'Done.'

download_file(S3BACKUP_FILE)
download_file(S3CONF_FILE)
