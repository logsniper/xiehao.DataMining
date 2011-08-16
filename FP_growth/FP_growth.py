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

	def comp(self,ka,kb):
		ca = self.__keyTable[ka]
		cb = self.__keyTable[kb]
		if ca == None or cb == None:
			print '[Error] :',ka,'or',kb,'doesn\'t exist in keytable'
			return 0
		if ca < cb: return 1
		elif ca > cb : return -1
		else :
			if ka < kb: return -1
			elif ka==kb: return 0
			else : return 1

	def __insert(self,array,count):
		""" Insert a record into FP-tree. The record(array) may be a list or tuple."""
		idx = 0
		node = self.__head
		n = len(array)
		while idx < n:
			ret = node.addKeyWithCount(array[idx],self.__nodeList,count)
			if ret != 0 :
				print '[Error] : Failed to insert',array,'with count =',count,'and index =',idx
				return 1
			else :
				node = node.getChild(array[idx])
				idx += 1
		return 0

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
			datapair.data.sort(self.comp)
			if 0 != self.__insert(datapair.data,datapair.count):
				print '[Error] : Failed to insert',array,'with count =',count

#		print 'key table :\n',self.__keyTable
#		print 'node list :'
#		for node in self.__nodeList.items():
#			print node[0],len(node[1])

	def singlePath(self):
		node = self.__head
		while True:
			childNumber = len(node.children)
			if childNumber == 0: return True
			elif childNumber > 1: return False
			else: node = node.children.values()[0]

	def getHead(self):
		return self.__head

	def getKeyTable(self):
		return self.__keyTable

	def getNodeList(self):
		return self.__nodeList

class FP_growth:
	def __init__(self,min_sup_count):
		self.min_sup_count = min_sup_count

	def __getSubsets(self,fptree):
		node = fptree.getHead()
		nodelist = []
		while True:
			if len(node.children) == 0: break
			node = node.children.values()[0]
			if node.count < self.min_sup_count: break
			nodelist.append(DataPair(node.key,node.count))
		n = len(nodelist)
		size = 1<<n
		resmp = {}
		for mask in range(1,size): # use bitmap to reach every nodes combination
			count = 0
			array = []
			for i in range(n):
				if (mask & (1<<i)) > 0:
					array.append(nodelist[i].data)
					count = nodelist[i].count
			resmp[tuple(array)] = count
		return resmp

	def mining(self,fptree):
		if fptree.singlePath():
			return self.__getSubsets(fptree)
		keylist = fptree.getKeyTable().keys()
		keylist.sort(fptree.comp)
		keylist.reverse()
		result = {}
#		print 'keylist :',keylist
		for key in keylist:
			datalist = []
			nodelist = fptree.getNodeList()[key]
			for node in nodelist:
				count = node.count
				node = node.parent
				array = []
				while node.parent != None:
					array.append(node.key)
					node = node.parent
				datapair = DataPair(array,count)
				datalist.append(datapair)
			sub_fptree = FP_Tree()
			sub_fptree.createTree(datalist)
			resmp = self.mining(sub_fptree)
			for item in resmp.items():
				if item[1] < self.min_sup_count: continue
				freqSet = []
				freqSet.extend(item[0])
				freqSet.append(key)
				result[tuple(freqSet)] = item[1]
		return result

if __name__=='__main__':
	f = open('test.in.0.0','r')
	datalist = []
	while True:
		line = f.readline()
		if len(line)==0 : break
		datalist.append(DataPair(line.split(),1))
	tree = FP_Tree()
#	for datapair in datalist:
#		print datapair.data,datapair.count
#	print ''
	import profile
#	tree.createTree(datalist)
	profile.run('tree.createTree(datalist)')
	fpgrowth = FP_growth(200)
	profile.run('resmp = fpgrowth.mining(tree)')
	print 'frequent sets :'
	print resmp
	print 'number :',len(resmp)
