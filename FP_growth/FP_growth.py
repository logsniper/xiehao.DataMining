class FP_Node:
	def __init__(self,key,parent,nodeList,count=1):
		"""nodeList is the __nodeList in FP_Tree"""
		self.key = key
		self.parent = parent
		self.count = count
		self.children = {}
		if key != None:
			if key in nodeList:
				nodeList[key].append(self)
			else:
				nodeList[key] = [self]

	def addKeyWithCount(self,key,nodeList,count):
		"""nodeList is the __nodeList in FP_Tree"""
		self.count += count
		if key in self.children:
			self.children[key].count += count
		else:
			child = FP_Node(key,self,nodeList,count)
			if child == None:
				print '[Error] : Failed to create child for',key,'with count =',count
				return 1
			self.children[key] = child
		return 0

	def getChild(self,key):
		return self.children[key]

class DataPair:
	def __init__(self,data,count=1):
		"""data may be a list or a tuple"""
		self.data = data
		self.count = count

class FP_Tree:
	def __init__(self):
		self.__head = FP_Node(None,None,0)
		self.__keyTable = {}
		self.__nodeList = {}

	def __comp(self,ka,kb):
		ca = self.__keyTable[ka]
		cb = self.__keyTable[kb]
		if ca == None or cb == None:
			print ka,'or',kb,'doesn\'t exist in keytable'
			return 0
		if ca < cb: return 1
		elif ca > cb : return -1
		else :
			if ka < kb: return -1
			elif ka==kb: return 0
			else : return 1

	def __insert(self,curr_node,array,count):
		""" Insert a record into FP-tree. The record(array) may be a list or tuple."""
		array.sort(self.__comp)
		if len(array) == 0:
			"""Successful insertion and exit the recursion with return 0 """
			return 0
		ret = curr_node.addKeyWithCount(array[0],self.__nodeList,count)
		if ret != 0 :
			print '[Error] : Failed to insert',array,'with count =',count
			return 1
		else :
			next_node = curr_node.getChild(array[0])
			return self.__insert(next_node,array[1:],count)

	def __createCache(self,datalist):
		for datapair in datalist:
			for elem in datapair.data:
				if elem in self.__keyTable:
					self.__keyTable[elem] += 1
				else :
					self.__keyTable[elem] = 1

	def createTree(self,datalist):
		""" datalist must be a list of class DataPair """
		self.__createCache(datalist)
		for datapair in datalist:
			self.__insert(self.__head,datapair.data,datapair.count)

		print self.__keyTable
		print ''
		for node in self.__nodeList.items():
			print node[0],len(node[1])

if __name__=='__main__':
	f = open('test.in.0','r')
	datalist = []
	while True:
		line = f.readline()
		if len(line)==0 : break
		datalist.append(DataPair(line.split(),1))
	tree = FP_Tree()
#	for datapair in datalist:
#		print datapair.data,datapair.count
#	print ''

	tree.createTree(datalist)
