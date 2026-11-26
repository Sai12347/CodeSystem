class Solution {
    private static class Visit {
        int time;
        String site;

        Visit(int time, String site) {
            this.time = time;
            this.site = site;
        }
    }

    private static int comparePatterns(List<String> a, List<String> b) {
        for (int i = 0; i < 3; i++) {
            int cmp = a.get(i).compareTo(b.get(i));
            if (cmp != 0) {
                return cmp;
            }
        }
        return 0;
    }

    public List<String> mostVisitedPattern(String[] username, int[] timestamp, String[] website) {
        Map<String, List<Visit>> byUser = new HashMap<>();
        for (int i = 0; i < username.length; i++) {
            byUser.computeIfAbsent(username[i], k -> new ArrayList<>())
                  .add(new Visit(timestamp[i], website[i]));
        }

        Map<List<String>, Integer> scores = new HashMap<>();
        for (List<Visit> visits : byUser.values()) {
            visits.sort(Comparator.comparingInt(v -> v.time));
            int m = visits.size();
            Set<List<String>> seen = new HashSet<>();
            for (int i = 0; i < m; i++) {
                for (int j = i + 1; j < m; j++) {
                    for (int k = j + 1; k < m; k++) {
                        seen.add(List.of(visits.get(i).site, visits.get(j).site, visits.get(k).site));
                    }
                }
            }
            for (List<String> pat : seen) {
                scores.put(pat, scores.getOrDefault(pat, 0) + 1);
            }
        }

        List<String> best = null;
        int bestScore = -1;
        for (Map.Entry<List<String>, Integer> e : scores.entrySet()) {
            List<String> pat = e.getKey();
            int score = e.getValue();
            if (score > bestScore || (score == bestScore && comparePatterns(pat, best) < 0)) {
                bestScore = score;
                best = pat;
            }
        }
        return new ArrayList<>(best);
    }
}
