from point import Point

class KmeansAlgo:

	def __init__(self,K,plist):
		self.k = K
		self.plist = plist
		self.kinds = []
		if len(self.plist) < K:
			print 'plist member too few!'
			return
		for i in range(0,K):
			self.kinds.append([self.plist[i],])
		for i in range(K,len(plist)):
			self.kinds[0].append(self.plist[i])

	def adjust(self):
		readjust = 0
		midpoints = []
		for sublist in self.kinds:
			m = Point((0,0,))
			for x in sublist:
				m = m+x
			m = m/len(sublist)
			midpoints.append(m)
		for ilist in range(self.k):
			sublist = self.kinds[ilist]
			for x in sublist:
				minimal = midpoints[ilist].dist(x)
				idx = ilist
				for imid in range(self.k):
					tmpdist = x.dist(midpoints[imid])
					if tmpdist < minimal:
						minimal = tmpdist
						idx = imid
				if idx != ilist:
					sublist.remove(x)
					self.kinds[idx].append(x)
					readjust += 1
		return readjust

	def repeat(self):
		times = 0
		while True:
			readjust = self.adjust()
			if not readjust:
				break
			times += 1
			print times,readjust


if __name__ == '__main__':
	file = open('points.in','r')
	plist = []
	while True:
		s = file.readline()
		if len(s)==0:
			break
		points = s.split()
		plist.append(Point(tuple([int(i) for i in points])))
	km = KmeansAlgo(4,plist)
	km.repeat()
	for i in range(len(km.kinds)):
		print 'kind ',i
		for p in km.kinds[i]:
			print p.point
