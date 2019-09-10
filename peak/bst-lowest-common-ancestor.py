class Node:
    def __init__(self, info): 
        self.info = info  
        self.left = None  
        self.right = None 
        self.level = None 

    def __str__(self):
        return str(self.info) 

class BinarySearchTree:
    def __init__(self): 
        self.root = None

    def create(self, val):  
        if self.root == None:
            self.root = Node(val)
        else:
            current = self.root
         
            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break

# Enter your code here. Read input from STDIN. Print output to STDOUT
'''
class Node:
      def __init__(self,info): 
          self.info = info  
          self.left = None  
          self.right = None 
           

       // this is a node of the tree , which contains info as data, left , right
'''

def get_path(root, v):
    # list to keep track of search path
    result = [root]

    # search v
    current = root
    while current.info != v:
        if v < current.info:
            current = current.left
        elif v > current.info:
            current = current.right
        result.append(current)
    
    return result

def lca_v1(root, v1, v2):
    # search v1 and v2
    trace_v1 = get_path(root, v1)
    trace_v2 = get_path(root, v2)

    # location deviation point
    result = root
    for i in range(1, min(len(trace_v1), len(trace_v2)) - 1):
        if trace_v1[i].info != trace_v2[i].info:
            break
        else:
            result = trace_v1[i]
    return result


def lca(root, v1, v2):
    
    while True:
            
        if root.info>v1 and root.info>v2:
            root=root.left
        
        elif root.info<v1 and root.info<v2:
            root=root.right
        
        else:
            return root
  

tree = BinarySearchTree()
t = int(input())

arr = list(map(int, input().split()))

for i in range(t):
    tree.create(arr[i])

v = list(map(int, input().split()))

ans = lca(tree.root, v[0], v[1])
print (ans.info)
