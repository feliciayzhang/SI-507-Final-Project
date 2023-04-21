class Node:
    def __init__(self,feature_name, feature_value, album_name, track,left=None,right=None,
                                       parent=None):
        self.feature_name = feature_name
        self.feature_value = feature_value
        self.album_name = album_name
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

    def replaceNodeData(self,feature_name, feature_value,album_name, track,lc,rc):
        self.feature_name = feature_name
        self.feature_value = feature_value
        self.album_name = album_name
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
    
        
    def put(self,feature_name, feature_value, album_name, track):
      if self.root:
        self._put(feature_name, feature_value, album_name, track, self.root)
      else: 
        self.root = Node(feature_name, feature_value, album_name, track)
      self.size = self.size + 1
    
    def _put(self,feature_name, feature_value, album_name, track,currentNode):
      if feature_value < currentNode.feature_value:
        if currentNode.hasLeftChild():
          self._put(feature_name, feature_value, album_name, track,currentNode.leftChild)
        else:
          currentNode.leftChild = Node(feature_name, feature_value, album_name, track,parent=currentNode)
      else:
        if currentNode.hasRightChild():
            self._put(feature_name, feature_value, album_name,track,currentNode.rightChild)
        else:
          currentNode.rightChild = Node(feature_name, feature_value,album_name,track,parent=currentNode)

    def get(self,feature_value):
      if self.root:
        res = self._get(feature_value,self.root)
        if res:
          return res.track
        else:
          return None
      else:
        return None
        
    def _get(self,feature_value,currentNode):
      if not currentNode:
        return None
      elif currentNode.feature_value == feature_value:
        return currentNode
      elif feature_value < currentNode.feature_value:
        return self._get(feature_value,currentNode.leftChild)
      else:
        return self._get(feature_value,currentNode.rightChild)
        
    def __getitem__(self,feature_value):
        return self.get(feature_value)  


        
