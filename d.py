import heapq
def solution(scoville,k):
    heapq.heapify(scoville)
    count = 0
    while scoville[0] < k:
        x = heapq.heappop(scoville)
        if len(scoville) == 0:
            return -1
        y = heapq.heappop(scoville)
        heapq.heappush(scoville,x+y* 2)
    return count