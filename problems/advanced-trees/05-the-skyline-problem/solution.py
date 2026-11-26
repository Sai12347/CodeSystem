class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events=[]
        for left,right,height in buildings:
            events.append((left,-height));events.append((right,height))
        events.sort();active=Counter({0:1});heap=[0];out=[];i=0;prev=0
        while i<len(events):
            x=events[i][0]
            while i<len(events) and events[i][0]==x:
                h=events[i][1]
                if h<0:active[-h]+=1;heapq.heappush(heap,h)
                else:active[h]-=1
                i+=1
            while active[-heap[0]]==0:heapq.heappop(heap)
            cur=-heap[0]
            if cur!=prev:out.append([x,cur]);prev=cur
        return out
