class Apriori:
  def __init__(self,filename,min_sup_rate):
    self.filename = filename
    self.dataList=[]
    self.freqDataList=[]
    self.min_sup_rate = min_sup_rate
    self.support = {}
    self.initDataList()

  def initDataList(self):
    """initialize the original data from file"""
    file = open(self.filename,'r')
    countElem={}
    self.datamaps = [] # A class attribute, actually it's a set.
    while True:
      line = file.readline()
      if len(line) == 0: break
      arr = line.split()
      arr.sort() # every record(words) must be ordered
      self.dataList.append(tuple(arr))
      mp = {} # Actually this is a set which will be inserted into datamaps
      for k in arr:
        e = (k,)
        if e in countElem: countElem[e] += 1
        else : countElem[e] = 1
        mp[k] = 1
      self.datamaps.append(mp)
    file.close()
    self.min_sup = len(self.datamaps) * self.min_sup_rate
    print "Minimal support count is", self.min_sup
    for e in countElem:
      if countElem[e] >= self.min_sup:
        self.support[e] = countElem[e]
        self.freqDataList.append(e)
    print 'size of data :',len(self.datamaps)

  def candidatesFilter(self,srcList,dstList):
    """ Select the candidates who are really frequent.
        This function is the bottleneck of the algorithm. """
    actualCount = {}
    print "Number of loops in candidatesFilter :",len(self.datamaps)*len(srcList)
    for mp in self.datamaps: # For every data in database
      for cand in srcList: # For every candidates
        flag = True
        for e in cand:
          if not (e in mp):
            flag = False 
            break
        if flag :
          tcand = tuple(cand)
          if tcand in actualCount: actualCount[tcand] += 1
          else : actualCount[tcand] = 1
    for e in actualCount:
      if actualCount[e] >= self.min_sup:
        dstList.append(e)
        self.support[e] = actualCount[e]

  def findLargerFreqSet(self):
    """ Find a more frequent set, and the old less frequent one will be replaced."""
    candidates = []
    freqBuffer = [] # the larger freqDataSet buffer
    pbuf = self.freqDataList
    print len(pbuf[0]),'frequent set, size of prev freq-set :',len(pbuf)

    dataset = {}
    for e in pbuf : dataset[tuple(e)] = 1;
    def hasInfrequentSubset(data):
      """ if one of data's subset is infrequent, then data must be infrequent"""
      ld = len(data)
      for i in range(0,ld-1):
        tmp = []
        tmp.extend(data[:i])
        tmp.extend(data[i+1:])
        if not tuple(tmp) in dataset :
          return True
      return False

    """ Get the candidates."""
    N = len(pbuf)
    size = len(pbuf[0])
    pbuf.sort()
    for i in range(N):
      for j in range(i+1,N):
        if pbuf[i][:size-1] == pbuf[j][:size-1]:
          tmp = []
          tmp.extend(pbuf[i])
          tmp.append(pbuf[j][-1])
          if not hasInfrequentSubset(tmp) : candidates.append(tmp)
        else : break
    print 'size of candidates :',len(candidates)

    self.candidatesFilter(candidates,freqBuffer)

    if len(freqBuffer) == 0 : return False
    else : 
      self.freqDataList = freqBuffer
      return True

  def excute(self):
    if len(self.freqDataList) == 0 :
      print 'Too big parameter min_sup :',self.min_sup
      return False
    while True :
      if not self.findLargerFreqSet():
        return True

if __name__ == '__main__':
  import profile
  test = Apriori('test.in.0',0.33)
  profile.run('test.excute()')
  for k in test.freqDataList:
    print k
