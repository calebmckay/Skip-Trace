try:
	import logging
	import argparse
	import configparser
	from Crypto.PublicKey import RSA
except ImportError as e:
	print("[-] {}, exiting".format(e))
	exit(1)

class Settings():
	settings = configparser.ConfigParser()
	settingsFile = ""
	loaded = False

	def loadSettings(self,settingsFile='STcommon/settings.ini'):
		self.settings.read(settingsFile)
		if len(self.settings.sections()) == 0:
			return False
		else
			self.loaded = True
			self.settingsFile = settingsFile
			return True

	def writeSetting(self,key,value,section='DEFAULT'):
		if !self.loaded:
			return False
		self.settings[section][key] = value
		with open(self.settingsFile,'w') as settingsFile:
			self.settings.write(settingsFile)
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

	parser.add_argument('-g', '--generate-keys', metavar='PATH', type=str)

	return parser.parse_args()

if __name__ == "__main__":
	args = parseArgs()

	if args.generate_keys:
		keyGen(args.generate_keys)