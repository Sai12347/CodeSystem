class RangeModule:
    def __init__(self):
        self.ranges=[]
    def addRange(self,left: int,right: int) -> None:
        out=[];placed=False
        for a,b in self.ranges:
            if b<left:out.append([a,b])
            elif right<a:
                if not placed:out.append([left,right]);placed=True
                out.append([a,b])
            else:left=min(left,a);right=max(right,b)
        if not placed:out.append([left,right])
        self.ranges=out
    def queryRange(self,left: int,right: int) -> bool:
        return any(a<=left and right<=b for a,b in self.ranges)
    def removeRange(self,left: int,right: int) -> None:
        out=[]
        for a,b in self.ranges:
            if b<=left or a>=right:out.append([a,b])
            else:
                if a<left:out.append([a,left])
                if b>right:out.append([right,b])
        self.ranges=out
