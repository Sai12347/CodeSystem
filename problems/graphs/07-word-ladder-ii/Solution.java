class Solution {
    public List<List<String>> findLadders(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        List<List<String>> result = new ArrayList<>();
        if (!wordSet.contains(endWord)) {
            return result;
        }

        wordSet.remove(beginWord);
        Map<String, List<String>> parents = new HashMap<>();
        Set<String> layer = new HashSet<>();
        layer.add(beginWord);
        boolean found = false;
        int len = beginWord.length();

        while (!layer.isEmpty() && !found) {
            Set<String> nextLayer = new HashSet<>();
            for (String word : layer) {
                char[] chars = word.toCharArray();
                for (int i = 0; i < len; i++) {
                    char orig = chars[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == orig) continue;
                        chars[i] = c;
                        String next = new String(chars);
                        if (wordSet.contains(next)) {
                            parents.computeIfAbsent(next, k -> new ArrayList<>()).add(word);
                            nextLayer.add(next);
                            if (next.equals(endWord)) {
                                found = true;
                            }
                        }
                    }
                    chars[i] = orig;
                }
            }
            wordSet.removeAll(nextLayer);
            layer = nextLayer;
        }

        if (!found) {
            return result;
        }

        LinkedList<String> path = new LinkedList<>();
        path.add(endWord);
        backtrack(endWord, beginWord, parents, path, result);
        return result;
    }

    private void backtrack(
        String word,
        String beginWord,
        Map<String, List<String>> parents,
        LinkedList<String> path,
        List<List<String>> result
    ) {
        if (word.equals(beginWord)) {
            result.add(new ArrayList<>(path));
            return;
        }
        List<String> prevs = parents.get(word);
        if (prevs == null) return;
        for (String p : prevs) {
            path.addFirst(p);
            backtrack(p, beginWord, parents, path, result);
            path.removeFirst();
        }
    }
}
