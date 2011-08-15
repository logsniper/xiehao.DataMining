
import math

class Point:
	MAX_DIST = 1<<60

	def __init__(self,v):
		self.point = v

	def dist(self,other):
		pa = self.point
		pb = other.point
		if(len(pa) != len(pb)):
			return Point.MAX_DIST*max(len(pa),len(pb))
		res = 0
		for i in range(0,len(pa)):
			res += (pa[i]-pb[i])*(pa[i]-pb[i])
		return math.sqrt(res);

	def __add__(self,other):
		pa = self.point
		pb = other.point
		res = []
		for i in range(min(len(pa),len(pb))):
			res.append(pa[i]+pb[i])
		for i in range(min(len(pa),len(pb)), max(len(pa),len(pb))):
			res.append(Point.MAX_DIST)
		return Point(tuple(res))

	def __div__(self,num):
		p = [1.0*n/num for n in self.point]
		return Point(tuple(p))

if __name__ == '__main__':
	a = Point((1,2,))
	b = Point(tuple((3,4)))
	print a.point,b.point
	print (a+b).point
	print a.dist(b)
	print (a/2).point


