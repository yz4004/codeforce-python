from collections import defaultdict
"""
    一个可以插入字符串的字典树，統計節點的詞數（以該節點為前綴的詞數），支持刪除操作
    如果要删除 在父节点那里删除/查询儿子节点的，cur.children[c].nums -= 1
"""
class Node:
    __slots__ = 'children', 'prefix', 'endOfWord', 'cnt'
    def __init__(self):
        self.prefix = "" #当前前缀 最后一个字母为他的parent通向他的path
        self.children = defaultdict(Node)
        self.endOfWord = False
        self.cnt = 0 #一个前缀被多少個詞使用，方便删除, 子樹的葉節點個數

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        cur = self.root
        cur.cnt += 1
        for w in word:
            prefix = cur.prefix
            cur = cur.children[w]
            cur.prefix = prefix + w #上一個cur的prefix拼接當前字符
            cur.cnt += 1 #cnt不能從上面累計，因為有其他詞以他為前綴
        cur.endOfWord = True
        return cur #最後cur一定是None 這麼寫標記函數結尾，可讀性

    def search(self, word: str) -> bool:
        """原始搜索"""
        cur = self.root
        for w in word:
            if w not in cur.children:
                return False
            cur = cur.children[w]
        return cur.endOfWord

    def search1(self, word: str) -> bool:
        """
        考慮count的搜索
        """
        cur = self.root
        for w in word:
            if w not in cur.children or cur.children[w].cnt == 0:  # 下一個為空節點
                return False
            cur = cur.children[w]
        return cur.endOfWord

    def delete(self, word: str) -> None:
        """刪除一個詞，最後返回None"""
        cur = trie.root
        for w in word:
            cur = cur.children[w]
            cur.cnt -= 1
        return cur

def print_trie(node, prefix="", is_last=True):
    """ Recursively prints the trie. """
    if node and node.cnt > 0:
        line = "   " if is_last else "|  "
        if node.prefix != '':  # Skip printing for root node
            print(prefix + "+-- " + node.prefix + " " + str(node.cnt))
        new_prefix = prefix + line
        last_key = list(node.children.keys())[-1] if node.children else None
        for key in node.children:
            print_trie(node.children[key], new_prefix, key == last_key)

if __name__ == '__main__':

    #測試
    """
               +-- a 3
                  +-- ab 2
                  |  +-- abc 2
                  |     +-- abcd 1
                  |     +-- abce 1
                  +-- az 1
                     +-- aze 1
    刪除 abce
                     
               +-- a 2
                  +-- ab 1
                  |  +-- abc 1
                  |     +-- abcd 1
                  +-- az 1
                     +-- aze 1
    """

    trie = Trie()

    # 先插入三個，打印
    trie.insert("abcd")
    trie.insert("abce")
    trie.insert("aze")

    print(trie.search("abcd"), trie.search("aze"), trie.search("abc"), trie.search("af"))
    print(trie.search1("abcd"), trie.search1("aze"), trie.search1("abc"), trie.search1("af"))
    print_trie(trie.root)

    #刪除abce
    trie.delete("abce")
    # 不考慮判斷空節點cnt
    print(trie.search("abce"), trie.search("abcd"))
    # 考慮判斷空節點，abce 為 false abcd true
    print(trie.search1("abce"), trie.search1("abcd"))

    print_trie(trie.root)
