
class Node:
    data = None
    left, right = None, None
    
    def __init__(self, _data):
        self.data = _data
        
    def insert(self, value):
        if value <= self.data:
            if self.left is None:
                self.left = Node(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = Node(value)
            else:
                self.right.insert(value)
    
    def has(self, value):
        if self.data == value:
            return True
        elif value < self.data:
            if self.left is None:
                return False
            else:
                return self.left.has(value)
        else:
            if self.right is None:
                return False
            else:
                return self.right.has(value)
            
    # Important: https://foofish.net/python-function-args.html
    def in_order(self, _cache=None):
        if _cache is None:
            _cache = []
        if self.left is not None:
            self.left.in_order(_cache)
        _cache.append(self.data)
        if self.right is not None:
            self.right.in_order(_cache)
        return _cache
    
    
if __name__ == '__main__':
    
    bt_root = Node(10)
    bt_root.insert(5)
    bt_root.insert(15)
    bt_root.insert(8)
    
    print(bt_root.has(15))
    print(bt_root.has(16))
    
    print(bt_root.in_order())
    
    bt_root.insert(13)
    bt_root.insert(3)
    bt_root.insert(6)
    
    print(bt_root.in_order())