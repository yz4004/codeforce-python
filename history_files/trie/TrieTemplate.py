from collections import defaultdict
"""
    一个可以插入字符串的字典树
    最简单版本 只有key包含子信息 endOfWord 包含是否为词尾，以区分前缀和完整的词
"""
class Node:
    __slots__ = 'children', 'endOfWord'
    def __init__(self):
        self.children = defaultdict(Node)
        self.endOfWord = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        cur = self.root
        for w in word:
            cur = cur.children[w]
        cur.endOfWord = True

    """
        def search(self, word: str) -> bool:
            cur = self.root
            for w in word:
                if w in cur.children:
                    cur = cur.children[w] #错误，没有退出，这等于越过了不存在的字符w 从下一个存在的字符开始
            return cur.endOfWord
    """

    def search(self, word: str) -> bool:
        cur = self.root
        for w in word:
            if w not in cur.children:
                return False
            cur = cur.children[w]
        return cur.endOfWord

    def search_prefix(self, word: str) -> bool:
        cur = self.root
        for w in word:
            if w not in cur.children:
                return False
            cur = cur.children[w]
        return True # 唯一区别，不再检查是否是词尾

def print_trie(node, prefix=""):
    """ Recursively prints the trie. """
    children = list(node.children.keys())
    for i, char in enumerate(children):
        if i == len(children) - 1:
            # Last child
            print(prefix + "+-- " + char)
            new_prefix = prefix + "    "
        else:
            print(prefix + "+-- " + char)
            new_prefix = prefix + "|   "
        print_trie(node.children[char], new_prefix)

if __name__ == '__main__':
    trie = Trie()
    trie.insert("abcd")
    trie.insert("abce")
    trie.insert("aze")

    # abcd, aze 在树中，abc作为前缀在树中，但不是endOfWord，af则不存在这个f
    print(trie.search("abcd"), trie.search("aze"), trie.search("abc"), trie.search("af"))

    # 如果存在这个prefix则返回，即使它不是词
    print(trie.search_prefix("abcd"), trie.search_prefix("aze"), trie.search_prefix("abc"), trie.search_prefix("af"))

    # print(trie.delete(trie.root, "abce", 0))

    print(trie.search("abcd"), trie.search("aze"), trie.search("abc"), trie.search("af"))




    print_trie(trie.root)

