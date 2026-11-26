class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> wordSet = new HashSet<>(wordList);
        if (!wordSet.contains(endWord)) {
            return 0;
        }
        wordSet.remove(beginWord);
        wordSet.remove(endWord);

        Set<String> front = new HashSet<>();
        Set<String> back = new HashSet<>();
        front.add(beginWord);
        back.add(endWord);

        int length = 1;
        int wordLen = beginWord.length();

        while (!front.isEmpty() && !back.isEmpty()) {
            if (front.size() > back.size()) {
                Set<String> tmp = front;
                front = back;
                back = tmp;
            }
            Set<String> nextFront = new HashSet<>();
            for (String word : front) {
                char[] arr = word.toCharArray();
                for (int i = 0; i < wordLen; i++) {
                    char orig = arr[i];
                    for (char ch = 'a'; ch <= 'z'; ch++) {
                        if (ch == orig) {
                            continue;
                        }
                        arr[i] = ch;
                        String cand = new String(arr);
                        if (back.contains(cand)) {
                            return length + 1;
                        }
                        if (wordSet.remove(cand)) {
                            nextFront.add(cand);
                        }
                    }
                    arr[i] = orig;
                }
            }
            front = nextFront;
            length++;
        }

        return 0;
    }
}
