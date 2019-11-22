import os


def getSequenceFiles(_path):
	'''
	Given a file path, find all sibling files for the sequence.
	:param _path: Path to a file. Ex= X:/Files/render/RND_beauty.0001.exr
	:type _path: string
	:return: List of files (full paths) with the same name pattern in the given directory
	:rtype: list
	'''
	patternBool, namePattern, fileExt, parentFolder, hashStr = get_pattern(_path)

	if patternBool:
		print "Name pattern for given sequence is: {}{}.{}".format(namePattern, hashStr, fileExt)
		# Build list of files with the same name structure in the directory
		filesAndDirs = os.listdir(parentFolder)
		fileList = []
		for each in filesAndDirs:
			if os.path.isfile(os.path.join(parentFolder, each)):
				thisFileExt = _getFileExtension(each)
				if each[:len(namePattern)] == namePattern and thisFileExt == fileExt:
					fileList.append(os.path.join(parentFolder, each))
		fileList= sorted(fileList)

		if is_sequence(fileList, namePattern):
			return fileList

	return [_path]


def get_pattern(_path):
	'''
	Tests if given file path has siblings.
	:param _path: Path to a file. Ex= X:/Files/render/RND_beauty.0001.exr
	:type _path: string
	:return: sequenceBool: True if siblings found. False if file is unique in that directory.
	:rtype: bool
	:return: namePattern: Base file name used for sibling files.
	:rtype: string
	:return: fileExt: File extension for sibling files.
	:rtype: string
	:return: parentFolder: Parent folder that contains all given sibling files.
	:rtype: string
	:return: hasStr: Number of digits, represented as '#' characters found in the name pattern for sibling files.
	:rtype: string
	'''
	pathParts = os.path.split(os.path.realpath(os.path.normcase(_path)))
	parentFolder = pathParts[0]
	fileWithExt = pathParts[1]
	# Split extension
	fileName, fileExt = fileWithExt.rsplit(".", 1)
	# Get number of digits
	digitsNumber = 0
	for each in fileName[::-1]:
		if each.isdigit() or each == '#':
			digitsNumber += 1
		else:
			break
	namePattern = fileName[:-digitsNumber]
	hashStr = "#" * digitsNumber
	# Find other files with the same name structure in the directory
	filesAndDirs = os.listdir(parentFolder)
	patternBool = False
	for each in filesAndDirs:
		eachPath = os.path.join(parentFolder, each)
		if os.path.isfile(eachPath):
			thisFileExt = _getFileExtension(each)
			if os.path.realpath(os.path.normcase(_path)) == os.path.realpath(os.path.normcase(eachPath)):
				continue
			elif each[:len(namePattern)] == namePattern and thisFileExt == fileExt:
				patternBool = True
				break
	return patternBool, namePattern, fileExt, parentFolder, hashStr


def is_sequence(_files, namePattern):
	firstFile = _files[0]
	lastFile = _files[-1]
	splitFirstFile = os.path.split(firstFile)[1]
	firstFileName = splitFirstFile.rsplit(".", 1)[0]
	firstFileNumber = int(firstFileName[len(namePattern):])

	splitLastFile = os.path.split(lastFile)[1]
	lastFileName = splitLastFile.rsplit(".", 1)[0]
	lastFileNumber = int(lastFileName[len(namePattern):])

	difference = lastFileNumber - firstFileNumber + 1

	if len(_files) != difference:
		return False

	return True


def _enumerate_sequence(_files, firstFileNumber, lastFileNumber):
	fileNumber = firstFileNumber
	fileIndex = 0
	while fileNumber < lastFileNumber:
		yield (_files[fileIndex], fileNumber)
		fileIndex += 1


def _getFileExtension(filename):
    ''' Returns extension of this file with no '.' '''
    thisFileExt = os.path.splitext(filename)[1]
    if len(thisFileExt) > 0:
        thisFileExt = thisFileExt.split('.')[1]
    else:
        thisFileExt = None
    return thisFileExt
