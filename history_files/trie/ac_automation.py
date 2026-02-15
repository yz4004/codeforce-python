"""
AC自动机 【trie上


"""
from collections import defaultdict, deque
from typing import List


class Node:
    __slots__ = 'children', 'fail', 'exist'
    def __init__(self):
        self.children = defaultdict(Node)
        self.exist = [] # 记录长度  替代了 self.endOfWord
        self.fail = None

class AC:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        cur = self.root
        for w in word:
            cur = cur.children[w]
        cur.exist.append(len(word)) # 用长度替代了endOfWord 改成word编号也行 保留更多信息

    def build(self, words : List[str]):
        # 1. 普通构建字典树
        for word in words:
            self.insert(word)

        # 2. bfs的构建fail指针
        q = deque([]) # 先将root孩子入队，并将fail指针指向root
        children = self.root.children
        for w in children.keys():
            q.append(children[w])
            children[w].fail = self.root

        while q:
            cur = q.popleft()
            for w in cur.children: #当前cur的 孩子 w/children[w] 构建他的fail指针
                # 2.1 普通bfs入队逻辑
                child = cur.children[w]
                q.append(child)

                # 2.2 循环构建fail指针
                fafail = cur.fail
                while fafail and w not in fafail.children:
                    fafail = fafail.fail
                if fafail:
                    child.fail = fafail.children[w]
                else:
                    child.fail = self.root
                # 2.3 更新当前child的结尾单词，如果children的fail指针
                if child.fail and child.fail.exist: #虽然这个判断在python里多余
                    child.exist.extend(child.fail.exist)
        """
        说明 
        1. 只有root fail指针为空，其余都是非空，所以截断条件 x.fail is None
        2. 相比普通bfs唯一多出的是构建fail指针部分
        3. fafail回溯条件，父节点的fail指针没有w 即 那条不会是最大匹配前后缀时，查看次大 直到fail为空为根节点
        4. 最后 如果child更新后fail指针里蕴含了exist非空单词，说明有单词结尾，也在child里更新
        5. 一段前缀的结尾 对应的trie上节点 是该前缀最后一个字符w通过 children[w] 访问到的树节点，里面储存是是否有单词的信息 exist
            所以fail指针指向的是 已经匹配的前后缀的 后一个树节点
        
        fail指针的定义 x.fail = y 【根节点到y这条分支/前缀】 是 【根节点到x这条分支的最大匹配后缀】
        """



    def query(self, text): # 多模式匹配，找到text中所有匹配字典树的单词
        res = []
        cur = self.root # trie 上节点指针
        for i, c in enumerate(text): #对text[,i] 查找其所有的匹配单词
            # 失配回溯fail指针
            while c not in cur.children and not cur.fail:
                cur = cur.fail
            if c in cur.children:
                cur = cur.children[c]
            else: # 就是root节点
                continue

            if cur.exist: # 以text[，i] 匹配到的当前字典树node 上的单词串非空
                for l in cur.exist: # exist包含长度
                    res.append(text[i-l+1:i+1])
        return res
    """ 主要思想
    i - text上指针; cur - 树节点指针
    两者从开始时同时移动，如果树指针有对应子节点 (text[i]/c) 则这是匹配的单词前缀，同步前进
    如果失配，则利用树节点指针的fail指针会退 （text[i] 不发生回退）
    
    fail指针定义 x.fail = y
    树节点x对应的前缀 的 【最长后缀】 是 树节点y对应的前缀
    - 字典树就是普通建立的字典树，所以每个节点往上到根节点，就是某个单词的前缀
    - 匹配发生失配时，字典树上指针和文本指针 （cur/i) 必须发生回退，我们规定树回退,文本不动
      树节点此时对应的前缀 和 文本截止到i 已经发生了一部分前缀匹配，【如果是kmp则预处理这个前缀的最长匹配前后缀】
      希望尽可能短的回退，即希望找trie上尽可能长的前缀 （最长的前缀即为当前的失配前缀，回退到次大前缀）
      所以对当前失配分支，我想问，有没有另一个分支 去匹配这个失配分支的后缀，
      
    """




###################
# fail指针跳转优化
# 1. 跳转到fail指针的支路后，那条支路钱途未卜，可能若干匹配后失败，需要再次跳转fail - 直去表





