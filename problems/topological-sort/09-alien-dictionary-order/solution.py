class Solution:
    def alienOrder(self, words: List[str]) -> str:
        chars=set(''.join(words));g={c:set() for c in chars};d={c:0 for c in chars}
        for a,b in zip(words,words[1:]):
            i=0
            while i<min(len(a),len(b)) and a[i]==b[i]:i+=1
            if i==len(b) and len(a)>len(b):return ''
            if i<min(len(a),len(b)) and b[i] not in g[a[i]]:g[a[i]].add(b[i]);d[b[i]]+=1
        q=[c for c in chars if d[c]==0];heapq.heapify(q);out=[]
        while q:
            c=heapq.heappop(q);out.append(c)
            for v in g[c]:
                d[v]-=1
                if d[v]==0:heapq.heappush(q,v)
        return ''.join(out) if len(out)==len(chars) else ''
