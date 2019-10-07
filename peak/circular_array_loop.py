# leetcode 457

class Solution:
    
    @staticmethod
    def dfs(graph, nums, start_node, visited, path):
        if start_node in path:
            occ = path.index(start_node)
            if len(path) - occ > 1:
                # only possible cycle
                _dir = nums[start_node]
                for i in range(occ, len(path)):
                    if _dir * nums[path[i]] < 0:
                        return False
                return True
            else:
                return False
        if start_node in graph:
            path.append(start_node)
            for adj_node in graph[start_node]:
                if __class__.dfs(graph, nums, adj_node, visited, path):
                    return True
            path.pop()
        visited.add(start_node)
        return False
        
    
    def circularArrayLoop(self, nums) -> bool:
        # translate to a directed graph represented with a hash table
        n_nodes = len(nums)
        dgraph = {}
        for i in range(n_nodes):
            to_idx = (i + nums[i]) % n_nodes
            if i in dgraph:
                dgraph[i].append(to_idx)
            else:
                dgraph[i] = [to_idx]
        # detect cycle with in directed graph with DFS
        visited = set()
        path = []
        while len(visited) < n_nodes:
            to_visit = set(dgraph.keys()) - visited
            if __class__.dfs(dgraph, nums, next(iter(to_visit)), visited, path):
                return True
        return False
    
if __name__ == '__main__':
    print(Solution().circularArrayLoop([2,-1,1,2,2])) # True
    print(Solution().circularArrayLoop([-1,2])) # False
    print(Solution().circularArrayLoop([-2,1,-1,-2,-2])) # False
    print(Solution().circularArrayLoop([2,-1,1,-2,-2])) # False
    print(Solution().circularArrayLoop([3,1,2])) # True
    print(Solution().circularArrayLoop([2,-1,2,-1,3])) # True
    