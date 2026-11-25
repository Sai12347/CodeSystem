import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const bubbleSortMetadata: AlgorithmMetadata = {
  id: 'bubble-sort',
  title: 'Bubble Sort',
  category: 'BEGINNER',
  subcategory: 'Sorting Algorithms',
  difficulty: 'Easy',
  description:
    'Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order until no swaps are needed.',
  realWorldExample:
    'Air bubbles rising to the water surface: the largest elements gradually "bubble up" to the end of the array on every full pass.',
  timeComplexity: {
    best: 'O(n) (when optimized with a swapped flag and input is already sorted)',
    average: 'O(n²)',
    worst: 'O(n²) (reverse sorted array)',
  },
  spaceComplexity: 'O(1) auxiliary space (in-place)',
  commonMistakes: [
    'Not adjusting the inner loop bound (j < n - i - 1), doing redundant comparisons on already sorted items.',
    'Forgetting the swapped flag optimization to exit early when array becomes sorted.',
    'Off-by-one errors comparing arr[j] with arr[j+1] causing IndexOutOfBounds.',
  ],
  defaultInput: [34, 12, 45, 9, 23, 18],
  code: {
    java: `public void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        boolean swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}`,
    python: `def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break`,
  },
};

export function generateBubbleSortSteps(initialArr: number[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const arr = [...initialArr];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const getVisualElements = (
    currentJ: number | null = null,
    swapping: boolean = false,
    sortedStartIndex: number = n
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      let subLabel = '';

      if (idx >= sortedStartIndex) {
        state = 'sorted';
        subLabel = 'sorted';
      } else if (currentJ !== null && (idx === currentJ || idx === currentJ + 1)) {
        state = swapping ? 'swapping' : 'comparing';
        subLabel = idx === currentJ ? 'j' : 'j+1';
      }

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel,
        heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
      };
    });
  };

  steps.push({
    stepIndex: steps.length,
    description: `Start Bubble Sort on array of ${n} elements.`,
    elements: getVisualElements(),
    variables: { i: null, j: null, swapped: false, swapCount: 0 },
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'Initialize array and prepare for passes.',
      whatNext: 'Begin outer loop pass i = 0.',
      keyTakeaway: 'Each pass guarantees placing the next largest element in its final sorted position at the end.',
    },
  });

  let totalSwaps = 0;

  for (let i = 0; i < n - 1; i++) {
    let swapped = false;

    steps.push({
      stepIndex: steps.length,
      description: `Starting Pass i = ${i}. Inner loop will check pairs from j = 0 to ${n - i - 2}.`,
      elements: getVisualElements(null, false, n - i),
      variables: { i, j: null, swapped: false, swapCount: totalSwaps },
      changedVariables: ['i'],
      codeLine: { java: 3, python: 3 },
      explanation: {
        why: `Outer loop iteration ${i}.`,
        whatNext: 'Compare adjacent elements.',
        keyTakeaway: `Last ${i} elements are already in their final sorted positions.`,
      },
    });

    for (let j = 0; j < n - i - 1; j++) {
      const willSwap = arr[j] > arr[j + 1];

      // Predict challenge on first comparison of pass 0
      const prediction: AlgorithmStep['prediction'] | undefined =
        i === 0 && j === 0
          ? {
              question: `arr[j]=${arr[j]} and arr[j+1]=${arr[j + 1]}. Will they swap?`,
              options: [
                willSwap ? 'Yes, because arr[j] > arr[j+1]' : 'No, they are in correct order',
                willSwap ? 'No, no swap needed' : 'Yes, swap them anyway',
              ],
              correctOptionIndex: 0,
              explanation: willSwap
                ? `${arr[j]} > ${arr[j + 1]}, so a swap is required to move larger value right.`
                : `${arr[j]} <= ${arr[j + 1]}, so they are already in relative ascending order.`,
              hint: 'In ascending sort, we swap if the left element is larger than the right element.',
            }
          : undefined;

      // Comparing step
      steps.push({
        stepIndex: steps.length,
        description: `Compare arr[${j}] (${arr[j]}) with arr[${j + 1}] (${arr[j + 1]}).`,
        elements: getVisualElements(j, false, n - i),
        variables: {
          i,
          j,
          'arr[j]': arr[j],
          'arr[j+1]': arr[j + 1],
          swapped,
          swapCount: totalSwaps,
        },
        changedVariables: ['j', 'arr[j]', 'arr[j+1]'],
        codeLine: { java: 6, python: 6 },
        prediction,
        explanation: {
          why: `Compare adjacent elements at index ${j} and ${j + 1}.`,
          whatNext: willSwap
            ? `arr[${j}] > arr[${j + 1}] (${arr[j]} > ${arr[j + 1]}): Perform swap!`
            : `arr[${j}] <= arr[${j + 1}] (${arr[j]} <= ${arr[j + 1]}): Already ordered, do not swap.`,
          keyTakeaway: 'Bubble sort only compares immediate neighbors.',
        },
      });

      if (willSwap) {
        // Swap
        const temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
        swapped = true;
        totalSwaps++;

        steps.push({
          stepIndex: steps.length,
          description: `SWAP! Exchanged ${arr[j]} and ${arr[j + 1]}.`,
          elements: getVisualElements(j, true, n - i),
          variables: {
            i,
            j,
            'arr[j]': arr[j],
            'arr[j+1]': arr[j + 1],
            swapped: true,
            swapCount: totalSwaps,
          },
          changedVariables: ['arr[j]', 'arr[j+1]', 'swapped', 'swapCount'],
          codeLine: { java: 7, python: 7 },
          explanation: {
            why: `Swapped to maintain ascending order.`,
            whatNext: `Increment j to inspect next pair.`,
            keyTakeaway: `Total swaps so far: ${totalSwaps}.`,
          },
        });
      }
    }

    // End of pass: arr[n - i - 1] is placed in sorted position
    steps.push({
      stepIndex: steps.length,
      description: `Pass i = ${i} complete. Element ${arr[n - i - 1]} at index ${n - i - 1} is now in final sorted position.`,
      elements: getVisualElements(null, false, n - i - 1),
      variables: { i, j: null, swapped, swapCount: totalSwaps },
      codeLine: { java: 12, python: 10 },
      explanation: {
        why: `Largest remaining element has bubbled up to index ${n - i - 1}.`,
        whatNext: swapped ? 'Proceed to next pass.' : 'No swaps occurred! Array is already fully sorted.',
        keyTakeaway: swapped
          ? `Continuing optimization.`
          : 'Early exit condition triggered: saved remaining iterations!',
      },
    });

    if (!swapped) {
      break;
    }
  }

  // Final sorted state
  steps.push({
    stepIndex: steps.length,
    description: `Bubble Sort finished! Entire array is sorted with ${totalSwaps} total swaps.`,
    elements: getVisualElements(null, false, 0),
    variables: { i: null, j: null, swapped: false, swapCount: totalSwaps },
    codeLine: { java: 14, python: 11 },
    explanation: {
      why: 'All elements verified in non-decreasing order.',
      whatNext: 'Sorting completed.',
      keyTakeaway: 'Stable sorting algorithm: does not alter relative order of identical elements.',
    },
  });

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
