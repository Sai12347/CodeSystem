import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const quickSortMetadata: AlgorithmMetadata = {
  id: 'quick-sort',
  title: 'Quick Sort',
  category: 'BEGINNER',
  subcategory: 'Sorting Algorithms',
  difficulty: 'Medium',
  description:
    'An efficient in-place divide-and-conquer sorting algorithm. It selects a "pivot" element, partitions the other elements into two sub-arrays according to whether they are less than or greater than the pivot, and then recursively sorts the sub-arrays.',
  realWorldExample:
    'Organizing books on a shelf by choosing an arbitrary middle book: place books thinner than it to its left, thicker books to its right, and repeat.',
  timeComplexity: {
    best: 'O(n log n)',
    average: 'O(n log n)',
    worst: 'O(n²) (when pivot is repeatedly the smallest or largest element)',
  },
  spaceComplexity: 'O(log n) auxiliary stack space',
  commonMistakes: [
    'Always picking arr[0] as pivot on already-sorted arrays, causing O(n²) worst-case performance.',
    'Infinite recursion due to incorrect partition index bounds.',
  ],
  defaultInput: [10, 80, 30, 90, 40, 50, 70],
  code: {
    java: `public void quickSort(int[] arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr, i, j);
        }
    }
    swap(arr, i + 1, high);
    return i + 1;
}`,
    python: `def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1`,
  },
};

export function generateQuickSortSteps(initialArr: number[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const arr = [...initialArr];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const getVisualElements = (
    pivotIdx: number | null,
    iIdx: number | null,
    jIdx: number | null,
    swapping: boolean = false
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      const labels: string[] = [];

      if (idx === pivotIdx) {
        state = 'pivot';
        labels.push('pivot');
      } else if (swapping && (idx === iIdx || idx === jIdx)) {
        state = 'swapping';
      } else if (idx === jIdx) {
        state = 'comparing';
        labels.push('j');
      }

      if (idx === iIdx) {
        labels.push('i');
      }

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel: labels.join(', '),
        heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
      };
    });
  };

  steps.push({
    stepIndex: steps.length,
    description: `Start Quick Sort on ${n} elements.`,
    elements: getVisualElements(null, null, null),
    variables: { low: 0, high: n - 1, pivot: null },
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'Quick Sort partitions elements around a pivot.',
      whatNext: 'Begin partitioning range [0 ... n-1].',
      keyTakeaway: 'In-place sorting with O(log n) stack memory.',
    },
  });

  function partition(low: number, high: number): number {
    const pivot = arr[high];
    let i = low - 1;

    steps.push({
      stepIndex: steps.length,
      description: `Partition range [${low} ... ${high}]. Selected pivot = arr[${high}] (${pivot}).`,
      elements: getVisualElements(high, i, null),
      variables: { low, high, pivot, i },
      changedVariables: ['pivot', 'i'],
      codeLine: { java: 9, python: 8 },
      explanation: {
        why: `Pivot is chosen as last element ${pivot}.`,
        whatNext: 'Scan j from low to high-1 to find elements smaller than pivot.',
        keyTakeaway: 'Elements <= pivot will end up on the left; elements > pivot on the right.',
      },
    });

    for (let j = low; j < high; j++) {
      const isSmaller = arr[j] < pivot;

      steps.push({
        stepIndex: steps.length,
        description: `Inspect arr[${j}] (${arr[j]}): is ${arr[j]} < pivot (${pivot})?`,
        elements: getVisualElements(high, i, j),
        variables: { low, high, pivot, i, j, 'arr[j]': arr[j] },
        codeLine: { java: 12, python: 11 },
        explanation: {
          why: `Comparing candidate element ${arr[j]} with pivot ${pivot}.`,
          whatNext: isSmaller ? 'Increment i and swap arr[i] with arr[j].' : 'Continue scanning j.',
          keyTakeaway: 'i keeps boundary of elements smaller than pivot.',
        },
      });

      if (isSmaller) {
        i++;
        const temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;

        steps.push({
          stepIndex: steps.length,
          description: `arr[${j}] < pivot. Swapped arr[${i}] and arr[${j}].`,
          elements: getVisualElements(high, i, j, true),
          variables: { low, high, pivot, i, j },
          changedVariables: ['i'],
          codeLine: { java: 14, python: 13 },
          explanation: {
            why: `Small element moved to left partition at index ${i}.`,
            whatNext: 'Advance j.',
            keyTakeaway: 'Smaller elements congregate at indices 0..i.',
          },
        });
      }
    }

    // Place pivot at i + 1
    const temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    const pi = i + 1;

    steps.push({
      stepIndex: steps.length,
      description: `Place pivot ${pivot} into its final sorted position at index ${pi}.`,
      elements: getVisualElements(pi, null, null),
      variables: { low, high, pivot, pi },
      changedVariables: ['pi'],
      codeLine: { java: 17, python: 14 },
      explanation: {
        why: `All items before ${pi} are < ${pivot}; all items after are >= ${pivot}.`,
        whatNext: `Pivot ${pivot} is now fixed. Recursively sort left and right partitions.`,
        keyTakeaway: 'Index pi is in its absolute final sorted position.',
      },
    });

    return pi;
  }

  function sort(low: number, high: number) {
    if (low < high) {
      const pi = partition(low, high);
      sort(low, pi - 1);
      sort(pi + 1, high);
    }
  }

  sort(0, n - 1);

  steps.push({
    stepIndex: steps.length,
    description: `Quick Sort completed! Array is fully sorted.`,
    elements: arr.map((val, idx) => ({
      id: `elem-${idx}-${val}`,
      value: val,
      state: 'sorted',
      label: `${idx}`,
      subLabel: 'sorted',
      heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
    })),
    variables: { low: 0, high: n - 1, complete: true },
    codeLine: { java: 5, python: 5 },
    explanation: {
      why: 'All partitions solved.',
      whatNext: 'Sorting complete.',
      keyTakeaway: 'Average time complexity is O(n log n) with excellent cache locality.',
    },
  });

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
