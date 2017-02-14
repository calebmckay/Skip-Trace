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

	def createSettings(self,inFile='STcommon/settings.ini'):
		self.settingsFile = inFile
		with open(self.settingsFile,'w') as outFile:
			self.settings.write(outFile)
		self.loaded = True
		return True

	def loadSettings(self,inFile='STcommon/settings.ini'):
		self.settings.read(inFile)
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

	parser.add_argument('-c', '--configure', nargs=2, metavar='ADDRESS PORT')
	parser.add_argument('-g', '--generate-keys', metavar='PATH', type=str)

	return parser.parse_args()

if __name__ == "__main__":
	args = parseArgs()

	if args.generate_keys:
		keyGen(args.generate_keys)
	if args.configure:
		Settings.createSettings()
		for section in ["DEFAULT","Server","Client"]:
			Settings.writeSetting("Address",str(args.configure[0]),section)
			Settings.writeSetting("Port",str(args.configure[1]),section)
