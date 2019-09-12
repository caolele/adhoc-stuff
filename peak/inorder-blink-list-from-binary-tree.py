# https://www.youtube.com/watch?time_continue=1240&v=FsxTX7-yhOw

from vanilla_binary_tree import Node as BinaryTree


class DoubleLinkedList:
    
    class DllNode:
        data = None
        prev, next = None, None
        
        def __init__(self, _data):
            self.data = _data
    
    head = None # type:DllNode
    ptr = None # type:DllNode
    
    def reset_ptr(self):
        self.ptr = self.head
            
    def create_dll_from_btree(self, btree_root: BinaryTree):
        if btree_root is None:
            return None
        # recursive the left tree
        self.create_dll_from_btree(btree_root.left)
        # process the current node
        p = self.DllNode(btree_root.data)
        if self.ptr is None:
            self.head = p
        else:
            p.prev = self.ptr
            self.ptr.next = p
        self.ptr = p
        # recursive the right tree
        self.create_dll_from_btree(btree_root.right)
        
    def get_forward_pass_nodes(self):
        result = []
        self.reset_ptr()
        while self.ptr is not None:
            result.append(self.ptr.data)
            self.ptr = self.ptr.next
        return result
        
        
if __name__ == "__main__":
    
    # build a test binary tree
    bt_root = BinaryTree(10)
    bt_root.insert(5)
    bt_root.insert(15)
    bt_root.insert(8)
    bt_root.insert(13)
    bt_root.insert(3)
    bt_root.insert(6)
    print(bt_root.in_order())
    
    # build a dll from the binary tree
    my_dll = DoubleLinkedList()
    my_dll.create_dll_from_btree(bt_root)
    print(my_dll.get_forward_pass_nodes())