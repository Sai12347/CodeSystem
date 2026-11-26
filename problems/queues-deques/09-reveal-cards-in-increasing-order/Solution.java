class Solution {
    public int[] deckRevealedIncreasing(int[] deck) {
        int n = deck.length;
        int[] sorted = deck.clone();
        Arrays.sort(sorted);
        Deque<Integer> q = new ArrayDeque<>(n);
        for (int i = 0; i < n; i++) {
            q.offerLast(i);
        }
        int[] res = new int[n];
        for (int card : sorted) {
            res[q.pollFirst()] = card;
            if (!q.isEmpty()) {
                q.offerLast(q.pollFirst());
            }
        }
        return res;
    }
}
