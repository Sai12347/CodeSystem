class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        rank={c:i for i,c in enumerate(order)}
        for a,b in zip(words,words[1:]):
            i=0
            while i<min(len(a),len(b)) and a[i]==b[i]:i+=1
            if i==len(b) and len(a)>len(b):return False
            if i<min(len(a),len(b)) and rank[a[i]]>rank[b[i]]:return False
        return True
