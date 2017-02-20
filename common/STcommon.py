try:
	import logging
	import argparse
	import configparser
	from Crypto.PublicKey import RSA
	from os.path import isfile
except ImportError as e:
	print("[-] {}, exiting".format(e))
	exit(1)

class Settings():
	def __init__()
		settings = configparser.ConfigParser()
		settingsFile = ""
		loaded = False

	def __createSettings(self,inFile='STcommon/settings.ini'):
		self.settingsFile = inFile
		with open(self.settingsFile,'w') as outFile:
			self.settings.write(outFile)
		self.loaded = True
		return True

	def loadSettings(self,inFile='STcommon/settings.ini'):
		if not isfile(inFile):
			self.__createSettings(inFile)
		self.settings.read(inFile)
		self.loaded = True
		self.settingsFile = inFile
		return True

	def writeSetting(self,key,value,section='DEFAULT'):
		if not self.loaded:
			return False
		self.settings[section][key] = value
		with open(self.settingsFile,'w') as outFile:
			self.settings.write(outFile)
		return True

	def getSetting(self,key,section='DEFAULT'):
		return self.settings[section].get(key)


def configDebugLog(logFileName):
	log_file = logging.FileHandler(logFileName,mode='w')
	log_file.setLevel(logging.DEBUG)
	log_file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

	# ERROR level or higher should be output to console as well
	log_console = logging.StreamHandler()
	log_console.setLevel(logging.ERROR)
	log_console.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

	logger = logging.getLogger('main_logger')
	logger.addHandler(log_console)
	logger.addHandler(log_file)
	return logger

def keyGen(path):
	key = RSA.generate(2048)
	with open(path +'/python.pem','wb') as privateKey:
		privateKey.write(key.exportKey('PEM'))
	with open(path+ '/python.pub', 'wb') as publicKey:
		publicKey.write(key.publickey().exportKey('PEM'))

def parseArgs():
	'''Parses args using the argparse lib'''
	parser = argparse.ArgumentParser(description='Location logging server')

	parser.add_argument('-a', '--address', metavar='ADDRESS')
	parser.add_argument('-c', '--configure', action='store_true')
	parser.add_argument('-g', '--generate-keys', metavar='PATH', type=str)
	parser.add_argument('-L', '--logfile', metavar='LOG_FILE')
	parser.add_argument('-p', '--port', metavar='PORT')

	return parser.parse_args()

if __name__ == "__main__":
	mysettings = Settings()

	args = parseArgs()

	if args.generate_keys:
		keyGen(args.generate_keys)
	if args.configure:
		if not mysettings.loaded:
			mysettings.loadSettings()
		if args.address:
			mysettings.writeSetting("Address",str(args.address),'DEFAULT')
		if args.port:
			mysettings.writeSetting("Port",str(args.port),'DEFAULT')
		if args.logfile:
			mysettings.writeSetting("LogFile",str(args.logfile),'DEFAULT')
	else
		if args.address or args.port or args.logfile:
			print("ERROR: must include -c or --configure")