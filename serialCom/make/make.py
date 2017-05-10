#coding=utf-8
'''
Created on 2015-10-28
'''
import xml.dom.minidom as minidom
import sys, os, codecs
import re

# if sys.getdefaultencoding() != 'gbk':
#     reload(sys)
#     sys.setdefaultencoding('gbk')

def genNsi():
	xVersion = packageXmlOps()
	svnVersion = getSubversion()
	pos = xVersion.index('(')
	#1.2.9472.301
	dVersion = xVersion[0:pos]
	pos = xVersion.rindex('.')

	pVersion = xVersion[0:pos]

	#301(恒远)
	pModel = xVersion[pos+1:]

	pos = pVersion.rindex('.')
	pBase = pVersion[pos+1:]

	pos = pModel.index('(')
	#(恒远)
	pUser = pModel[pos:]

	make_dir = "!define MAKE_DIR '..\\..\\base_%s'\n" % (pBase)

	if ('2' != pVersion[2]):
		product_name = "!define PRODUCT_NAME 'Punggol'\n"
	else:
		product_name = "!define PRODUCT_NAME 'Pungo'\n"

	develop_version = "!define DEVELOP_VERSION '%s'\n" % (dVersion)
	support_version = "!define SUPPORT_VERSION '%s'\n" % (svnVersion)
	user_id = "!define USER_ID '%s'\n" % (pUser)
	readme = "!define README '..\\Readme%s.txt'\n" % (pModel)

	if ('release' == sys.argv[1]):
		return ([make_dir, product_name, develop_version, support_version, user_id, readme], xVersion, dVersion + '.' + svnVersion + pUser)
	else:
		test = "!define _TEST\n"
		return ([make_dir, product_name, develop_version, support_version, user_id, readme, test], xVersion, dVersion + '.' + svnVersion + pUser)

def packageXmlOps():
	dom = minidom.parse("package.xml")
	root = dom.documentElement
	version = root.getElementsByTagName('Version')
	xVersion = version[0].firstChild.data
	binary = root.getElementsByTagName('Binary')
	bf = open("binary.nsi", "w")
	for element in binary:
		if -1 != element.firstChild.data.find('Pungo.exe') or -1 != element.firstChild.data.find('Punggol.exe') or -1 != element.firstChild.data.find('ecat.exe'):
			bf.write("File '${MAKE_DIR}\GFD-%s'\n" % element.firstChild.data[element.firstChild.data.rindex('\\')+1:])
		else:
			bf.write("File '${MAKE_DIR}\%s'\n" % element.firstChild.data[element.firstChild.data.rindex('\\')+1:])
		
	bf.close()
	return xVersion

def isXmlTest():
	dom = minidom.parse("sys/000(公共)/测试版.xml")
	root = dom.documentElement
	product = root.getElementsByTagName('TestVersion')
	testVersion = product[0].firstChild.data
	return int(testVersion)

def getSubversion():
	output = os.popen("svn info .")
	# Revision可能在第5行也可能在第6行，与subversion版本有关
	for i in range(0, 5):
		output.readline()
	svnVersion = output.readline()
	if -1 == svnVersion.find('Revision:'):
		svnVersion = output.readline().strip().strip('\n')
	else:
		svnVersion = svnVersion.strip().strip('\n')
	svnVersion = svnVersion[svnVersion.index(':')+2:]
	return svnVersion

def writeNsi(sequence):
	mf = open("make.nsi", "w")
	mf.writelines(sequence)
	package = "!include '%s\\nPackage.nsi'" % (cur_file_dir())
	mf.write(package)
	mf.close

def runNsi():
	os.system('GFD-makensis.exe make.nsi')

def modifyXml(oldStr, newStr, code):
	#替换package.xml中version
	replaceFile('package.xml', oldStr, newStr)
	#替换测试版.xml
	if(1 == code):
		replaceFile("sys/000(公共)/测试版.xml", "<TestVersion>0</TestVersion>", "<TestVersion>1</TestVersion>")
	elif(0 == code):
		replaceFile("sys/000(公共)/测试版.xml", "<TestVersion>1</TestVersion>", "<TestVersion>0</TestVersion>")

def replaceFile(fileName, oldStr, newStr):
	f1 = codecs.open(fileName, 'r', 'utf-8')
	data1 = f1.read()
	f1.close()

	f2 = codecs.open(fileName, 'w', 'utf-8')
	data2 = data1.replace(oldStr, newStr)
	f2.write(data2)
	f2.close()

def revertFile(oldStr, newStr, code):
	if(1 == code):
		modifyXml(oldStr, newStr, 0)
	elif(0 == code):
		modifyXml(oldStr, newStr, 1)
	else:
		modifyXml(oldStr, newStr, code)
	os.remove('make.nsi')
	os.remove('binary.nsi')

def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

if __name__ == '__main__':
	(nsi, oldStr, newStr) = genNsi()
	xmlTest = isXmlTest()

	revertCode = -1
	if xmlTest == 1 and 'release' == sys.argv[1]:
		revertCode = 0
	elif 0 == xmlTest and 'release' != sys.argv[1]:
		revertCode = 1
	modifyXml(oldStr, newStr, revertCode)
	writeNsi(nsi)

	runNsi()
	revertFile(newStr, oldStr, revertCode)
    
