import os, shutil, platform, sys, logging, urllib2, zipfile

############################################

INSTALL_DIR = os.getcwd()

GITHUB_MASTER = 'https://raw.githubusercontent.com/khilnani/pythonista-scripts/master/'
GITHUB_ARCHIVE = 'https://github.com/khilnani/pythonista-scripts/archive/master.zip'

ARCHIVE_DIR_PARTIAL = 'pythonista-scripts-master/'
ARCHIVE_DIR = os.path.join(INSTALL_DIR, ARCHIVE_DIR_PARTIAL)
ARCHIVE_NAME = 'pythonista-scripts.zip'
ARCHIVE_PATH = os.path.join(INSTALL_DIR, ARCHIVE_NAME)

TOOLS_DIR = 'tools/'
S3BACKUP = 's3backup.py'
S3CONF_SAMPLE = 'sample.aws.conf'
S3CONF = 'aws.conf'

############################################

machine = platform.machine()
print 'Platform system:' + machine

print('Installing to: %s' % INSTALL_DIR)

if 'iP' in machine:
	BASE_DIR = os.path.expanduser('~/Documents')
else:
	BASE_DIR = os.getcwd()

############################################

try:
	import console
except ImportError:
	class console (object):
		@staticmethod
		def hud_alert(message, icon=None, duration=None):
			print message

		@staticmethod
		def input_alert(title, message=None, input=None, ok_button_title=None, hide_cancel_button=False):
			message = '' if message == None else message
			ret = input
			try:
				ret = raw_input(title + '' + message + ' :')
			except Exception as e:
				print e
			return ret

############################################

def setup_logging(log_level='INFO'):
	log_format = "%(message)s"
	logging.addLevelName(15, 'FINE')
	logging.basicConfig(format=log_format, level=log_level)

def move_files(from_dir, to_dir):
	logging.info('Moving files from %s to %s' % (from_dir, to_dir))
	for dirpath, dirnames, filenames in os.walk(from_dir):
		dir_partial = dirpath.split(ARCHIVE_DIR)[1]
		dest_dir = os.path.join(to_dir, dir_partial)
		if not os.path.exists(dest_dir):
			os.makedirs(dest_dir)
		for f in filenames:
			from_file = os.path.join(dirpath, f)
			to_file = os.path.join(dest_dir, f)
			if os.path.exists(to_file):
				logging.info('   OVERWRITE from %s to %s' % (from_file, to_file))
			else:
				logging.info('   From %s to %s' % (from_file, to_file))
			try:
				shutil.copyfile(from_file, to_file)
			except IOError as ioe:
				logging.error(ioe)
			except shutil.Error as e:
				logging.warn(e)
			except Exception as e:
				logging.error(e)
	logging.info('Done.')

def download_file(src, dest):
	logging.info('Downloading %s' % (src))
	file_content = urllib2.urlopen(src).read()
	logging.info('Writing %s' % dest)
	f = open(dest, 'w')
	f.write(file_content)
	f.close()
	logging.info('Done.')

def list_zip(zip_file):
	logging.info('Lising zip %s' % (zip_file))
	zip_ref = zipfile.ZipFile(zip_file, 'r')
	for name in zip_ref.namelist():
		print name
	zip_ref.close()
	logging.info('Done.')

def unzip_file(zip_file, extract_to):
	logging.info('Unzipping %s to %s' % (zip_file, extract_to))
	zip_ref = zipfile.ZipFile(zip_file, 'r')
	zip_ref.extractall(extract_to)
	zip_ref.close()
	logging.info('Done.')

def get_selection():
	sel = None
	if len(sys.argv) > 1:
		sel =sys.argv[1]
	else:
		sel = console.input_alert('''
Select an option:
1. S3 backup/restore script
2. List all files
3. Download all files
''', "", "")
	return sel

############################################

def download_s3backup():
	download_file(GITHUB_MASTER+TOOLS_DIR+S3BACKUP, os.path.join(INSTALL_DIR, S3BACKUP))
	download_file(GITHUB_MASTER+TOOLS_DIR+S3CONF_SAMPLE, os.path.join(INSTALL_DIR, S3CONF))
	print 'Please edit %s and then run: %s' % (S3CONF, S3BACKUP)

def download_archive():
	download_file(GITHUB_ARCHIVE, ARCHIVE_PATH)
	unzip_file(ARCHIVE_PATH, INSTALL_DIR)
	move_files(ARCHIVE_DIR, INSTALL_DIR)
	shutil.rmtree(ARCHIVE_DIR)
	os.remove(ARCHIVE_PATH)

def review_archive():
	download_file(GITHUB_ARCHIVE, ARCHIVE_PATH)
	list_zip(download_loc)
	os.remove(ARCHIVE_PATH)

############################################

def main():
	setup_logging()
	sel = get_selection()

	# tools/s3backup
	if sel == '1':
		download_s3backup()
	elif sel == '2':
		review_archive()
	elif sel == '3':
		download_archive()

############################################

if __name__ == '__main__':
	main()