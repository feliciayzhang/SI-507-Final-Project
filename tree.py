class Node:
    def __init__(self,feature,track,left=None,right=None,
                                       parent=None):
        self.feature = feature
        self.track = track
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,feature,track,lc,rc):
        self.feature = feature
        self.track = track
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()
    
        
    def put(self,feature,track):
      if self.root:
        self._put(feature,track, self.root)
      else: 
        self.root = Node(feature,track)
      self.size = self.size + 1
    
    def _put(self,feature,track,currentNode):
      if feature < currentNode.feature:
        if currentNode.hasLeftChild():
          self._put(feature,track,currentNode.leftChild)
        else:
          currentNode.leftChild = Node(feature,track,parent=currentNode)
      else:
        if currentNode.hasRightChild():
            self._put(feature,track,currentNode.rightChild)
        else:
          currentNode.rightChild = Node(feature,track,parent=currentNode)

    def get(self,feature):
      if self.root:
        res = self._get(feature,self.root)
        if res:
          return res.track
        else:
          return None
      else:
        return None
        
    def _get(self,feature,currentNode):
      if not currentNode:
        return None
      elif currentNode.feature == feature:
        return currentNode
      elif feature < currentNode.feature:
        return self._get(feature,currentNode.leftChild)
      else:
        return self._get(feature,currentNode.rightChild)
        
    def __getitem__(self,feature):
        return self.get(feature)  

def inorder(Node):
    if Node:
        inorder(Node.get('left'))
    print(Node['feature'])
    inorder(Node.get('right'))
        
