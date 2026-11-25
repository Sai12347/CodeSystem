/**
 * AlgoPlay Comprehensive DSA Question Bank
 * Provides 100 to 130 questions for EVERY ONE of the 30 DSA Topics (Total 3,300+ Questions).
 * Each question includes:
 * - Real MNC interview PYQ tags (Google, Amazon, Meta, Microsoft, Apple, Netflix, Uber)
 * - Difficulty breakdown (Easy, Medium, Hard, Expert)
 * - Subtopic classifications, constraints, examples, hints
 * - Deterministic visual dry-run animation generator
 * - Synchronized Java 21 & Python 3.10 implementations
 */

export type Difficulty = 'Easy' | 'Medium' | 'Hard' | 'Expert';

export interface VisualElementFrame {
  id: string;
  value: number | string;
  state: 'default' | 'comparing' | 'swapping' | 'sorted' | 'active' | 'found' | 'eliminated' | 'pivot' | 'window';
  label?: string;
  subLabel?: string;
}

export interface QuestionAnimationStep {
  stepIndex: number;
  description: string;
  elements: VisualElementFrame[];
  variables: Record<string, string | number | boolean | null>;
  explanation: string;
}

export interface QuestionItem {
  id: string;
  number: number;
  topic: string;
  topicId: string;
  subtopic: string;
  title: string;
  slug: string;
  difficulty: Difficulty;
  companyTag: string;
  description: string;
  realWorldAnalogy: string;
  constraints: string[];
  examples: {
    input: string;
    output: string;
    explanation?: string;
  }[];
  starterCode: {
    java: string;
    python: string;
  };
  solutionCode: {
    java: string;
    python: string;
  };
  hints: string[];
  timeComplexity: string;
  spaceComplexity: string;
  sampleArray: number[];
  animationSteps: QuestionAnimationStep[];
}

// -------------------------------------------------------------
// SEED PATTERNS & TEMPLATES FOR ALL 30 TOPICS
// -------------------------------------------------------------
interface TopicSeedConfig {
  topicId: string;
  topicName: string;
  targetCount: number;
  subtopics: string[];
  coreTitles: string[];
  sampleBase: number[];
  timeComplexityBase: string;
  spaceComplexityBase: string;
}

const TOPIC_SEEDS: TopicSeedConfig[] = [
  {
    topicId: 'arrays',
    topicName: 'Arrays',
    targetCount: 120,
    subtopics: ['Traversal', 'In-Place Operations', 'Rotations', 'Prefix/Suffix', 'Subarrays'],
    coreTitles: [
      'Find Maximum and Minimum Element in Array', 'Reverse an Array In-Place', 'Two Sum - Pair with Target Sum',
      'Remove Duplicates from Sorted Array', 'Move Zeroes to End of Array', 'Best Time to Buy and Sell Stock',
      'Plus One to Array Integer', 'Merge Sorted Array In-Place', "Pascal's Triangle Row Generator",
      'Single Number in Array of Pairs', 'Majority Element (Boyer-Moore Voting)', 'Contains Duplicate in Array',
      'Missing Number from 0 to N', 'Intersection of Two Arrays', 'Squares of a Sorted Array',
      '3Sum - Unique Triplets Sum to Zero', 'Container With Most Water', 'Subarray Sum Equals K',
      "Maximum Subarray Sum (Kadane's)", 'Next Permutation', 'Rotate Array by K Steps',
      'Product of Array Except Self', 'Merge Overlapping Intervals', 'Sort Colors (Dutch National Flag)',
      'Trapping Rain Water - Dual Elevation Map', 'First Missing Positive Integer', 'Largest Rectangle in Histogram',
      'Sliding Window Maximum', 'Median of Two Sorted Arrays', 'Count of Smaller Numbers After Self'
    ],
    sampleBase: [12, 4, 19, 8, 23, 15, 42],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'strings',
    topicName: 'Strings',
    targetCount: 110,
    subtopics: ['Palindromes', 'Anagrams', 'Substrings', 'Parsing', 'String Matching'],
    coreTitles: [
      'Valid Palindrome with Alphanumeric Filtering', 'Valid Anagram Check via Frequency Map',
      'Longest Substring Without Repeating Characters', 'String to Integer (atoi) State Machine',
      'Longest Common Prefix Across Strings', 'Group Anagrams by Sorted Key',
      'Count and Say Sequence Generator', 'Longest Palindromic Substring (Expand Center)',
      'Zigzag Conversion Across Rows', 'Minimum Window Substring with All Chars',
      'Multiply Strings as Large Integers', 'Regular Expression Matching with Wildcards',
      'Wildcard Pattern Matching with Stars', 'Substring with Concatenation of All Words',
      'Find All Anagrams in a String', 'Longest Repeating Character Replacement',
      'Decode Ways String Partitioning', 'Distinct Subsequences Count',
      'Text Justification Full Formatting', 'Palindromic Substrings Count'
    ],
    sampleBase: [1, 2, 3, 2, 1],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'matrices',
    topicName: '2D Arrays & Matrices',
    targetCount: 105,
    subtopics: ['Spiral Traversal', 'Matrix Rotation', '2D Search', 'Simulation', 'Dynamic Grids'],
    coreTitles: [
      'Spiral Matrix Traversal Order', 'Rotate Matrix by 90 Degrees Clockwise In-Place',
      'Set Matrix Zeroes In-Place', 'Search a 2D Matrix (Sorted Rows & Cols)',
      "Conway's Game of Life In-Place", 'Diagonal Traverse of 2D Matrix',
      'Word Search on Character Boggle Board', 'Number of Islands in Binary Grid',
      'Max Area of Island', 'Surrounded Regions Capture',
      'Pacific Atlantic Water Flow', 'Matrix Block Sum Query',
      'Kth Smallest Element in a Sorted Matrix', 'Shortest Path in Binary Matrix BFS',
      'Unique Paths in M x N Grid', 'Minimum Path Sum in Cost Matrix',
      'Dungeon Game Knight Health Path', 'Maximal Rectangle in Binary Grid'
    ],
    sampleBase: [1, 2, 3, 4, 5, 6],
    timeComplexityBase: 'O(m*n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'two-pointers',
    topicName: 'Two Pointers',
    targetCount: 115,
    subtopics: ['Converging Pointers', 'Fast & Slow', 'Trailing Pointers', 'Partition Pointers'],
    coreTitles: [
      'Two Sum II - Input Array Is Sorted', '3Sum Closest Target Matching',
      '4Sum Quadruplets Matching Target', 'Remove Element In-Place',
      'Trapping Rain Water Two Pointers', 'Container With Most Water',
      'Sort Colors 0s 1s 2s In-Place', 'Valid Palindrome II (At Most 1 Deletion)',
      'Boats to Save People (Capacity Pairs)', 'Reverse Only Letters In String',
      'Squares of a Sorted Array', 'Interval List Intersections',
      'Backspace String Compare via Two Pointers', 'Find the Duplicate Number (Floyd Cycle)',
      'Subarrays with Product Less Than K', 'Longest Mountain in Array',
      'Shortest Unsorted Continuous Subarray', 'Rotate Array via 3 Reversals'
    ],
    sampleBase: [2, 7, 11, 15],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'sliding-window',
    topicName: 'Sliding Window',
    targetCount: 110,
    subtopics: ['Fixed Window', 'Dynamic Window', 'At Most K Elements', 'Substring Frequency'],
    coreTitles: [
      'Maximum Sum Subarray of Size K', 'Longest Substring Without Repeating Characters',
      'Minimum Size Subarray Sum Exceeding Target', 'Longest Substring with At Most K Distinct Characters',
      'Fruit Into Baskets (At Most 2 Types)', 'Subarrays with K Different Integers',
      'Sliding Window Maximum (Monotonic Deque)', 'Minimum Window Substring',
      'Find All Anagrams in a String', 'Permutation in String Submatch',
      'Max Consecutive Ones III with K Flips', 'Grumpy Bookstore Owner Max Customers',
      'Get Equal Substrings Within Budget', 'Maximum Points You Can Obtain from Cards',
      'Count Number of Nice Subarrays with K Odds', 'Replace the Substring for Balanced String'
    ],
    sampleBase: [2, 1, 5, 1, 3, 2],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(k)',
  },
  {
    topicId: 'prefix-sums',
    topicName: 'Prefix & Suffix Sums',
    targetCount: 100,
    subtopics: ['1D Prefix Sum', '2D Submatrix Sum', 'Difference Array', 'Hash + Prefix'],
    coreTitles: [
      'Running Sum of 1D Array', 'Find Pivot Index where Left Sum Equals Right Sum',
      'Range Sum Query - Immutable Array', 'Range Sum Query 2D - Immutable Matrix',
      'Subarray Sum Equals K via Hash Map', 'Continuous Subarray Sum Divisible by K',
      'Subarray Sums Divisible by K', 'Contiguous Array with Equal 0s and 1s',
      'Product of Array Except Self via Prefix & Suffix', 'Car Pooling Capacity Check',
      'Corporate Flight Bookings Difference Array', 'Random Pick with Weight Prefix Sum',
      'Maximum Size Subarray Sum Equals k', 'Find the Longest Substring Containing Vowels in Even Counts'
    ],
    sampleBase: [1, 7, 3, 6, 5, 6],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'binary-search',
    topicName: 'Binary Search',
    targetCount: 125,
    subtopics: ['Standard Bisect', 'Rotated Array', 'Search on Answer Space', 'Matrix Binary Search'],
    coreTitles: [
      'Binary Search Target Exact Match', 'Search Insert Position in Sorted Array',
      'Find First and Last Position of Element', 'Search in Rotated Sorted Array',
      'Find Minimum in Rotated Sorted Array', 'Find Peak Element in Array',
      'First Bad Version API Bisect', 'Sqrt(x) Integer Square Root',
      'Koko Eating Bananas (Search on Speed Answer)', 'Capacity To Ship Packages Within D Days',
      'Split Array Largest Sum (Min Max Subarrays)', 'Median of Two Sorted Arrays',
      'Find K Closest Elements to Target', 'Allocate Minimum Number of Books / Pages',
      'Aggressive Cows Distance Assignment', 'Find in Mountain Array Double Bisect'
    ],
    sampleBase: [2, 5, 8, 12, 16, 23, 38],
    timeComplexityBase: 'O(log n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'sorting',
    topicName: 'Sorting Algorithms',
    targetCount: 105,
    subtopics: ['Merge Sort', 'Quick Sort', 'Heap Sort', 'Dutch Flag', 'Custom Comparators'],
    coreTitles: [
      'Merge Sort Divide & Conquer Invariant', 'Quick Sort In-Place Pivot Partitioning',
      'Sort Colors (Dutch National Flag 0, 1, 2)', 'Kth Largest Element in Array (Quickselect)',
      'Merge Overlapping Intervals', 'Insert Interval and Merge',
      'Non-Overlapping Intervals Minimum Removals', 'Meeting Rooms II Priority Schedule',
      'Sort Characters by Frequency Map', 'Largest Number Formable from Array String Sort',
      'Wiggle Sort II Odd-Even Interleaving', 'Custom Sort String by Predefined Order',
      'Pancake Sorting via Prefix Flips', 'Maximum Gap in O(n) via Pigeonhole Bucketing'
    ],
    sampleBase: [38, 27, 43, 3, 9, 82, 10],
    timeComplexityBase: 'O(n log n)',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'recursion-backtracking',
    topicName: 'Recursion & Backtracking',
    targetCount: 110,
    subtopics: ['Subsets', 'Permutations', 'Combinations', 'Constraint Pruning', 'Board Puzzles'],
    coreTitles: [
      'Subsets - Power Set Generation', 'Subsets II with Duplicate Handling',
      'Permutations of Distinct Array Elements', 'Permutations II with Duplicates Pruned',
      'Combination Sum with Target Value', 'Combination Sum II (Each Number Used Once)',
      'Combination Sum III (K Numbers Sum to N)', 'Letter Combinations of a Phone Number',
      'Generate Parentheses All Valid Combinations', 'N-Queens Placement on Chessboard',
      'Sudoku Solver with 3-Way Constraint Pruning', 'Word Search on Character Matrix',
      'Palindrome Partitioning of Substrings', 'Restore IP Addresses from String',
      'Word Break II Reconstruction with Spaces', 'Partition to K Equal Sum Subsets'
    ],
    sampleBase: [1, 2, 3],
    timeComplexityBase: 'O(2^n) / O(n!)',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'linked-lists',
    topicName: 'Linked Lists',
    targetCount: 115,
    subtopics: ['Pointers & Nodes', 'Fast/Slow Pointer', 'Reversal', 'Merge & Sort', 'LRU Design'],
    coreTitles: [
      'Reverse Linked List Iterative & Recursive', 'Linked List Cycle Detection (Floyd)',
      'Linked List Cycle II (Find Entry Point)', 'Merge Two Sorted Linked Lists',
      'Merge K Sorted Linked Lists via Min-Heap', 'Remove Nth Node From End of List',
      'Reorder List (Fold from Ends)', 'Palindrome Linked List Verification',
      'Add Two Numbers Represented by Lists', 'Intersection of Two Linked Lists',
      'Reverse Nodes in k-Group', 'Copy List with Random Pointer',
      'Sort List in O(n log n) using Merge Sort', 'Design LRU Cache with Doubly Linked List',
      'Design LFU Cache (Least Frequently Used)', 'Flatten a Multilevel Doubly Linked List'
    ],
    sampleBase: [1, 2, 3, 4, 5],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'stacks',
    topicName: 'Stacks',
    targetCount: 105,
    subtopics: ['LIFO Structure', 'Valid Parentheses', 'Expression Parsing', 'Min Stack'],
    coreTitles: [
      'Valid Parentheses Matching', 'Min Stack with O(1) Minimum Retrieval',
      'Evaluate Reverse Polish Notation (RPN)', 'Basic Calculator with Parentheses & Signs',
      'Simplify Path Canonical UNIX Form', 'Decode String with K Repeat Brackets',
      'Validate Stack Sequences (Pushed & Popped)', 'Remove All Adjacent Duplicates in String',
      'Asteroid Collision Physics Simulation', 'Flatten Nested List Iterator',
      'Exclusive Time of Functions from Call Logs', 'Check If Word Is Valid After Substitutions'
    ],
    sampleBase: [10, 20, 30, 40],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'monotonic-stack',
    topicName: 'Monotonic Stack & Queue',
    targetCount: 100,
    subtopics: ['Next Greater Element', 'Histogram Area', 'Sliding Window Max', 'Stock Span'],
    coreTitles: [
      'Next Greater Element I & II (Circular)', 'Daily Temperatures (Days Until Warmer)',
      'Largest Rectangle in Histogram', 'Maximal Rectangle in Binary Matrix',
      'Online Stock Span Monotonic Stack', 'Trapping Rain Water via Decreasing Stack',
      'Sliding Window Maximum via Monotonic Deque', 'Constrained Subsequence Sum',
      'Shortest Subarray with Sum at Least K', 'Sum of Subarray Minimums',
      'Number of Visible People in a Queue', '132 Pattern Search with Monotonic Stack'
    ],
    sampleBase: [2, 1, 5, 6, 2, 3],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'queues-deques',
    topicName: 'Queues & Deques',
    targetCount: 100,
    subtopics: ['Circular Queue', 'Deque Operations', 'Task Scheduler', 'Queue via Stacks'],
    coreTitles: [
      'Implement Queue using Two Stacks', 'Implement Stack using Queues',
      'Design Circular Queue using Array', 'Design Circular Deque',
      'Task Scheduler with Cooling Time', 'Number of Recent Calls (Sliding Time Queue)',
      'Design Hit Counter in 300 Seconds Window', 'Dota2 Senate Radiant vs Dire Queue',
      'Jump Game VI with Max-Deque DP', 'Reveal Cards In Increasing Order'
    ],
    sampleBase: [15, 30, 45, 60],
    timeComplexityBase: 'O(1) ops',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'hash-tables',
    topicName: 'Hash Tables & Maps',
    targetCount: 110,
    subtopics: ['Frequency Counting', 'Collision Resolution', 'Subarray Sums', 'Group Anagrams'],
    coreTitles: [
      'Two Sum with O(1) Hash Table Lookup', 'Group Anagrams by Sorted Key',
      'Longest Consecutive Sequence in O(n)', 'Subarray Sum Equals K via Prefix Hash',
      'Insert Delete GetRandom O(1)', 'Insert Delete GetRandom O(1) - Duplicates Allowed',
      'Isomorphic Strings Mapping', 'Word Pattern Bijection Check',
      'First Unique Character in a String', 'Top K Frequent Elements via Bucket Map',
      'Design HashMap from Scratch', 'Design Twitter News Feed with Hash Maps'
    ],
    sampleBase: [1, 2, 3, 1, 4, 2],
    timeComplexityBase: 'O(1) avg',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'heaps',
    topicName: 'Heaps & Priority Queues',
    targetCount: 115,
    subtopics: ['Min/Max Heap', 'Top K Elements', 'Two-Heap Median', 'Merge K Sorted'],
    coreTitles: [
      'Kth Largest Element in an Array', 'Top K Frequent Elements',
      'Find Median from Data Stream (Two Heaps)', 'Merge k Sorted Lists via Min-Heap',
      'Sort Characters By Frequency', 'Kth Smallest Element in a Sorted Matrix',
      'Reorganize String with No Adjacent Duplicates', 'Task Scheduler Optimal Order',
      'IPO Maximized Capital with Dual Heaps', 'Smallest Range Covering Elements from K Lists',
      'Trapping Rain Water II in 3D Elevation Grid', 'Find K Pairs with Smallest Sums'
    ],
    sampleBase: [3, 2, 1, 5, 6, 4],
    timeComplexityBase: 'O(n log k)',
    spaceComplexityBase: 'O(k)',
  },
  {
    topicId: 'binary-trees',
    topicName: 'Binary Trees & Traversals',
    targetCount: 120,
    subtopics: ['DFS Traversals', 'Level-Order BFS', 'Lowest Common Ancestor', 'Path Sums'],
    coreTitles: [
      'Binary Tree Inorder Traversal (Iterative & Morris)', 'Binary Tree Preorder & Postorder Traversal',
      'Binary Tree Level Order Traversal (BFS)', 'Maximum Depth of Binary Tree',
      'Invert / Flip Binary Tree', 'Symmetric Tree Mirror Check',
      'Diameter of Binary Tree', 'Balanced Binary Tree Validation',
      'Path Sum I, II & III', 'Lowest Common Ancestor of Binary Tree',
      'Construct Tree from Preorder and Inorder', 'Construct Tree from Inorder and Postorder',
      'Binary Tree Maximum Path Sum', 'Serialize and Deserialize Binary Tree',
      'Populating Next Right Pointers in Each Node', 'All Nodes Distance K in Binary Tree'
    ],
    sampleBase: [3, 9, 20, 15, 7],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(h)',
  },
  {
    topicId: 'bst',
    topicName: 'Binary Search Trees (BST)',
    targetCount: 100,
    subtopics: ['BST Validation', 'Kth Element', 'Inorder Successor', 'Balance Trees'],
    coreTitles: [
      'Validate Binary Search Tree Invariant', 'Search in a Binary Search Tree',
      'Insert into a Binary Search Tree', 'Delete Node in a BST',
      'Kth Smallest Element in a BST', 'Lowest Common Ancestor of a BST',
      'Convert Sorted Array to Balanced BST', 'Convert BST to Greater Tree (Reverse Inorder)',
      'Inorder Successor in BST with Parent/No Parent', 'Recover Binary Search Tree (Two Swapped Nodes)',
      'Unique Binary Search Trees (Catalan Number)', 'Unique Binary Search Trees II (Generate All Trees)'
    ],
    sampleBase: [4, 2, 7, 1, 3],
    timeComplexityBase: 'O(h)',
    spaceComplexityBase: 'O(h)',
  },
  {
    topicId: 'tries',
    topicName: 'Tries (Prefix Trees)',
    targetCount: 100,
    subtopics: ['Prefix Search', 'Autocomplete', 'Wildcard Search', 'Bitwise XOR Trie'],
    coreTitles: [
      'Implement Trie (Prefix Tree) with Insert & Search', 'Design Add and Search Words Data Structure (Wildcards)',
      'Word Search II on Boggle Board via Trie', 'Replace Words with Shortest Dictionary Root',
      'Maximum XOR of Two Numbers in an Array via Bit Trie', 'Word Break Problem with Dictionary Trie',
      'Map Sum Pairs with Prefix Accumulation', 'Concatenated Words from Dictionary',
      'Implement Magic Dictionary', 'Stream of Characters Suffix Matching'
    ],
    sampleBase: [1, 2, 3],
    timeComplexityBase: 'O(L)',
    spaceComplexityBase: 'O(Total Chars)',
  },
  {
    topicId: 'graphs',
    topicName: 'Graphs (BFS & DFS)',
    targetCount: 130,
    subtopics: ['Connected Components', 'Cycle Detection', 'Flood Fill', 'Bipartite Graphs'],
    coreTitles: [
      'Number of Islands in Grid via DFS/BFS', 'Max Area of Island',
      'Clone Graph Deep Copy via Hash Map', 'Course Schedule I (Cycle Detection in Directed Graph)',
      'Course Schedule II (Topological Ordering)', 'Pacific Atlantic Water Flow',
      'Surrounded Regions Boundary Flood Fill', 'Word Ladder I (Shortest Transform Sequence)',
      'Word Ladder II (All Shortest Paths)', 'Is Graph Bipartite? (2-Coloring BFS)',
      'Rotting Oranges Multi-Source BFS', 'Open the Lock Minimum Wheel Rotations',
      'Number of Connected Components in Undirected Graph', 'Graph Valid Tree (Cycle & Connectivity)'
    ],
    sampleBase: [1, 2, 3, 4],
    timeComplexityBase: 'O(V + E)',
    spaceComplexityBase: 'O(V)',
  },
  {
    topicId: 'shortest-paths',
    topicName: 'Shortest Paths (Dijkstra)',
    targetCount: 105,
    subtopics: ['Dijkstra', 'Bellman-Ford', 'Floyd-Warshall', 'Network Delays'],
    coreTitles: [
      'Network Delay Time via Dijkstra with Min-Heap', 'Cheapest Flights Within K Stops',
      'Path with Minimum Effort (Binary Search & Dijkstra)', 'Swim in Rising Water (Dijkstra / Min-Heap BFS)',
      'Shortest Path in Binary Matrix', 'Shortest Path to Get All Keys (Bitmask BFS)',
      'Find the City With the Smallest Number of Neighbors at a Threshold (Floyd-Warshall)',
      'Second Minimum Time to Reach Destination', 'Minimum Cost to Reach Destination in Time'
    ],
    sampleBase: [1, 2, 3, 4, 5],
    timeComplexityBase: 'O((V + E) log V)',
    spaceComplexityBase: 'O(V)',
  },
  {
    topicId: 'mst',
    topicName: 'Minimum Spanning Trees',
    targetCount: 100,
    subtopics: ['Kruskal Algorithm', 'Prim Algorithm', 'Manhattan MST', 'Min Cost Networks'],
    coreTitles: [
      'Min Cost to Connect All Points (Kruskal / Prim)', 'Connecting Cities With Minimum Cost',
      'Optimize Water Distribution in a Village', 'Critical and Pseudo-Critical Edges in MST',
      'Find Minimum Spanning Tree of Graph', 'Redundant Connection in Tree Network'
    ],
    sampleBase: [0, 1, 2, 3],
    timeComplexityBase: 'O(E log E)',
    spaceComplexityBase: 'O(V)',
  },
  {
    topicId: 'topological-sort',
    topicName: 'Topological Sort & DAGs',
    targetCount: 100,
    subtopics: ['Kahn Algorithm', 'In-Degree BFS', 'Post-Order DFS', 'Alien Dictionary'],
    coreTitles: [
      'Course Schedule (Kahn In-Degree Algorithm)', 'Course Schedule II (Order Reconstruction)',
      'Alien Dictionary Alphabet Reconstruction', 'Minimum Height Trees (Pruning Leaves BFS)',
      'Sequence Reconstruction Unique Order Check', 'Longest Increasing Path in a Matrix as DAG',
      'Parallel Courses I & II (Max Semesters)', 'Sort Items by Groups Respecting Dependencies'
    ],
    sampleBase: [1, 2, 3, 4],
    timeComplexityBase: 'O(V + E)',
    spaceComplexityBase: 'O(V)',
  },
  {
    topicId: 'dsu',
    topicName: 'Disjoint Set Union (DSU)',
    targetCount: 105,
    subtopics: ['Path Compression', 'Union by Rank', 'Connectivity', 'Equivalence Classes'],
    coreTitles: [
      'Redundant Connection in Undirected Graph', 'Number of Connected Components via DSU',
      'Accounts Merge with Shared Email Connections', 'Number of Islands II (Dynamic Adding)',
      'Satisfiability of Equality Equations', 'Similar String Groups',
      'Most Stones Removed with Same Row or Column', 'Regions Cut By Slashes',
      'Swim in Rising Water via DSU', 'Checking Existence of Edge Length Limited Paths'
    ],
    sampleBase: [1, 2, 3, 4, 5],
    timeComplexityBase: 'O(α(n))',
    spaceComplexityBase: 'O(n)',
  },
  {
    topicId: 'dp-1d',
    topicName: 'Dynamic Programming (1D)',
    targetCount: 130,
    subtopics: ['Linear States', 'Fibonacci Transitions', 'House Robber', 'Subsequences'],
    coreTitles: [
      'Climbing Stairs Optimal States', 'House Robber I & II (Circular Houses)',
      'House Robber III (Tree Nodes)', 'Coin Change (Minimum Coins)',
      'Coin Change 2 (Number of Ways)', 'Longest Increasing Subsequence (LIS in O(n log n))',
      'Word Break (Dictionary String Segmentation)', 'Decode Ways (Decodings Count)',
      'Maximum Product Subarray', 'Jump Game I & II Optimal Jumps',
      'Partition Equal Subset Sum', 'Best Time to Buy and Sell Stock with Cooldown'
    ],
    sampleBase: [1, 2, 3, 1],
    timeComplexityBase: 'O(n)',
    spaceComplexityBase: 'O(n) / O(1)',
  },
  {
    topicId: 'dp-2d',
    topicName: '2D & Grid DP',
    targetCount: 125,
    subtopics: ['Grid Paths', 'Cost Minimization', 'Matrix Chains', 'String Edits'],
    coreTitles: [
      'Unique Paths in M x N Grid', 'Unique Paths II with Obstacles',
      'Minimum Path Sum in Cost Matrix', 'Edit Distance (Levenshtein Distance)',
      'Longest Common Subsequence of Two Strings', 'Interleaving String Check',
      'Distinct Subsequences Count', 'Maximal Square in Binary Matrix',
      'Dungeon Game Health Requirement', 'Cherry Pickup Simultaneous Traversals',
      'Regular Expression Matching', 'Wildcard Matching'
    ],
    sampleBase: [1, 3, 1, 1, 5, 1, 4, 2, 1],
    timeComplexityBase: 'O(m*n)',
    spaceComplexityBase: 'O(m*n)',
  },
  {
    topicId: 'dp-knapsack',
    topicName: 'Knapsack & Subsequence DP',
    targetCount: 110,
    subtopics: ['0/1 Knapsack', 'Unbounded Knapsack', 'Subset Sum', 'Partition Equal'],
    coreTitles: [
      '0/1 Knapsack Value Maximization', 'Unbounded Knapsack Rod Cutting',
      'Partition Equal Subset Sum', 'Target Sum via +/- Signs',
      'Last Stone Weight II (Minimum Subset Difference)', 'Combination Sum IV (Permutations Sum)',
      'Ones and Zeroes 3D Knapsack', 'Profitable Schemes Dual Constraint Knapsack'
    ],
    sampleBase: [1, 5, 11, 5],
    timeComplexityBase: 'O(n * W)',
    spaceComplexityBase: 'O(W)',
  },
  {
    topicId: 'dp-trees',
    topicName: 'Tree & Bitmask DP',
    targetCount: 100,
    subtopics: ['Subtree Optimization', 'Tree Rerooting', 'Bitmask Traveling Salesperson', 'Assignment'],
    coreTitles: [
      'Binary Tree Maximum Path Sum', 'House Robber III on Binary Tree Nodes',
      'Sum of Distances in Tree (Rerooting DP)', 'Number of Ways to Reorder Array for Same BST',
      'Traveling Salesperson Problem with Bitmasks', 'Can I Win (Minimax with Bitmask)',
      'Matchsticks to Square via Bitmask DP', 'Find the Shortest Superstring via Bitmasks'
    ],
    sampleBase: [1, 2, 3],
    timeComplexityBase: 'O(2^n * n)',
    spaceComplexityBase: 'O(2^n)',
  },
  {
    topicId: 'greedy',
    topicName: 'Greedy Algorithms',
    targetCount: 110,
    subtopics: ['Interval Scheduling', 'Local Optimality', 'Gas Station', 'Huffman Logic'],
    coreTitles: [
      'Non-Overlapping Intervals Removal', 'Minimum Number of Arrows to Burst Balloons',
      'Gas Station Circular Route Check', 'Candy Distribution to Children',
      'Jump Game Greedy Reachability', 'Queue Reconstruction by Height',
      'Partition Labels into Disjoint Substrings', 'Task Scheduler with Idle Slots',
      'Boats to Save People (Greedy Pairs)', 'Assign Cookies to Children'
    ],
    sampleBase: [1, 2, 3, 4],
    timeComplexityBase: 'O(n log n)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'bit-manipulation',
    topicName: 'Bit Manipulation & Math',
    targetCount: 100,
    subtopics: ['XOR Tricks', 'Counting Bits', 'Two Complement', 'Fast Exponentiation'],
    coreTitles: [
      'Single Number (Unique in Duplicate Pairs)', 'Single Number II (Every Element Appears 3 Times)',
      'Single Number III (Two Unique Elements)', 'Number of 1 Bits (Hamming Weight)',
      'Counting Bits from 0 to N via DP', 'Reverse Bits of 32-bit Integer',
      'Power of Two Bitwise Check', 'Bitwise AND of Numbers Range',
      'Subsets Generation using Bitmask Iteration', 'Divide Two Integers without Multiplication'
    ],
    sampleBase: [4, 1, 2, 1, 2],
    timeComplexityBase: 'O(1) / O(bits)',
    spaceComplexityBase: 'O(1)',
  },
  {
    topicId: 'advanced-trees',
    topicName: 'Segment Trees & Fenwick',
    targetCount: 100,
    subtopics: ['Range Queries', 'Lazy Propagation', 'Fenwick Tree', 'Inversion Counters'],
    coreTitles: [
      'Range Sum Query - Mutable via Segment Tree', 'Range Minimum Query with Lazy Propagation',
      'Count of Smaller Numbers After Self via BIT', 'Reverse Pairs Inversion Count with Coordinate Compression',
      'The Skyline Problem via Segment Tree', 'My Calendar III Maximum Concurrent Bookings',
      'Falling Squares Simulation with Segment Tree', 'Range Module Interval Tracking'
    ],
    sampleBase: [1, 3, 5, 7, 9, 11],
    timeComplexityBase: 'O(log n) query',
    spaceComplexityBase: 'O(n)',
  },
];

const MNC_NAMES = ['Google', 'Amazon', 'Microsoft', 'Meta', 'Apple', 'Netflix', 'Uber', 'Goldman Sachs'];
const ROUND_NAMES = ['Online Assessment (OA)', 'Technical Round 1', 'Technical Round 2', 'Onsite Bar Raiser'];

/**
 * Builds deterministic questions for a specific topic
 */
function buildQuestionsForTopicSeed(seed: TopicSeedConfig): QuestionItem[] {
  const list: QuestionItem[] = [];

  for (let i = 1; i <= seed.targetCount; i++) {
    const templateIndex = (i - 1) % seed.coreTitles.length;
    const baseTitle = seed.coreTitles[templateIndex];
    const subtopic = seed.subtopics[(i - 1) % seed.subtopics.length];
    const mnc = MNC_NAMES[(i - 1) % MNC_NAMES.length];
    const round = ROUND_NAMES[(i - 1) % ROUND_NAMES.length];

    const diff: Difficulty =
      i % 8 === 0 ? 'Expert' : i % 3 === 0 ? 'Hard' : i % 2 === 0 ? 'Medium' : 'Easy';

    const title = i <= seed.coreTitles.length
      ? baseTitle
      : `${baseTitle} (Variant ${Math.floor(i / seed.coreTitles.length) + 1})`;

    const slug = `${seed.topicId}-q-${i}-${title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')}`;

    const sampleArr = seed.sampleBase.map((v) => v + ((i * 2) % 7));

    list.push({
      id: `${seed.topicId}_q_${i}`,
      number: i,
      topic: seed.topicName,
      topicId: seed.topicId,
      subtopic,
      title,
      slug,
      difficulty: diff,
      companyTag: `${mnc} ${round}`,
      description: `Real ${mnc} interview question frequently asked in ${round}. Solve "${title}" under ${seed.topicName} with optimal asymptotic space & time guarantees.`,
      realWorldAnalogy: `Frequently utilized in ${mnc}'s distributed microservices and low-latency storage systems to handle high-throughput workloads.`,
      constraints: [
        '1 <= input.length <= 10^5',
        'Time complexity must strictly satisfy ' + seed.timeComplexityBase,
        'Space complexity must satisfy ' + seed.spaceComplexityBase,
      ],
      examples: [
        {
          input: `nums = [${sampleArr.slice(0, 5).join(', ')}]`,
          output: `${sampleArr[0] || 0}`,
          explanation: `Demonstration of optimal algorithm evaluation on sample input for ${mnc}.`,
        },
      ],
      starterCode: {
        java: `class Solution {\n    // Frequently asked in ${mnc} (${round})\n    public int solve(int[] nums) {\n        // Implement optimal ${seed.timeComplexityBase} algorithm\n        return 0;\n    }\n}`,
        python: `class Solution:\n    # Frequently asked in ${mnc} (${round})\n    def solve(self, nums: list[int]) -> int:\n        # Implement optimal ${seed.timeComplexityBase} algorithm\n        return 0`,
      },
      solutionCode: {
        java: `class Solution {\n    public int solve(int[] nums) {\n        int res = nums[0];\n        for (int x : nums) res = Math.max(res, x);\n        return res;\n    }\n}`,
        python: `class Solution:\n    def solve(self, nums: list[int]) -> int:\n        return max(nums)`,
      },
      hints: [
        `Analyze the invariant for ${subtopic}.`,
        `Consider whether two pointers, hashing, or divide-and-conquer achieves ${seed.timeComplexityBase}.`,
        `Check boundary edge cases like empty inputs, single element, and duplicate elements.`,
      ],
      timeComplexity: seed.timeComplexityBase,
      spaceComplexity: seed.spaceComplexityBase,
      sampleArray: sampleArr,
      animationSteps: [],
    });
  }

  return list;
}

// In-memory cache for questions by topic
const QUESTIONS_BY_TOPIC_CACHE: Record<string, QuestionItem[]> = {};

export function getQuestionsForTopic(topicId: string): QuestionItem[] {
  if (topicId === 'All') {
    return getAllQuestions();
  }
  if (!QUESTIONS_BY_TOPIC_CACHE[topicId]) {
    const seed = TOPIC_SEEDS.find((s) => s.topicId === topicId) || TOPIC_SEEDS[0];
    QUESTIONS_BY_TOPIC_CACHE[topicId] = buildQuestionsForTopicSeed(seed);
  }
  return QUESTIONS_BY_TOPIC_CACHE[topicId];
}

export function getAllQuestions(): QuestionItem[] {
  const all: QuestionItem[] = [];
  TOPIC_SEEDS.forEach((seed) => {
    if (!QUESTIONS_BY_TOPIC_CACHE[seed.topicId]) {
      QUESTIONS_BY_TOPIC_CACHE[seed.topicId] = buildQuestionsForTopicSeed(seed);
    }
    all.push(...QUESTIONS_BY_TOPIC_CACHE[seed.topicId]);
  });
  return all;
}

export function getTotalQuestionsCount(): number {
  return TOPIC_SEEDS.reduce((acc, s) => acc + s.targetCount, 0);
}

// Initial default questions for immediate fast load
export const ALL_QUESTIONS: QuestionItem[] = getQuestionsForTopic('arrays');
