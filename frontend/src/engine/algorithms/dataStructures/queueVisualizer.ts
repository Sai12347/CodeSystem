import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const queueMetadata: AlgorithmMetadata = {
  id: 'queue',
  title: 'Queue (FIFO Data Structure)',
  category: 'INTERMEDIATE',
  subcategory: 'Data Structures',
  difficulty: 'Easy',
  description:
    'A First-In-First-Out (FIFO) abstract data type with Enqueue, Dequeue, and Peek operations.',
  realWorldExample:
    'A line of people waiting at a movie ticket booth: the first person to arrive is the first person served.',
  timeComplexity: {
    best: 'O(1) (enqueue, dequeue, front)',
    average: 'O(1)',
    worst: 'O(1)',
  },
  spaceComplexity: 'O(n) space for storing n items',
  commonMistakes: [
    'Using an unoptimized array shift() in JavaScript or list.pop(0) in Python which takes O(n) instead of a circular buffer or doubly linked list.',
  ],
  defaultInput: ['ENQUEUE 15', 'ENQUEUE 30', 'ENQUEUE 45', 'DEQUEUE', 'ENQUEUE 60'],
  code: {
    java: `public class Queue {
    private LinkedList<Integer> queue = new LinkedList<>();

    public void enqueue(int val) {
        queue.addLast(val);
    }
    public int dequeue() {
        if (queue.isEmpty()) throw new NoSuchElementException();
        return queue.removeFirst();
    }
    public int front() {
        return queue.getFirst();
    }
}`,
    python: `from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, val):
        self.queue.append(val)

    def dequeue(self):
        if not self.queue:
            raise IndexError("dequeue from empty queue")
        return self.queue.popleft()

    def front(self):
        return self.queue[0]`,
  },
};

export function generateQueueSteps(operations: string[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const currentQueue: number[] = [];

  const getVisualElements = (action: string): VisualElement[] => {
    return currentQueue.map((val, idx) => ({
      id: `queue-item-${idx}-${val}`,
      value: val,
      state: idx === 0 ? 'active' : 'default',
      label: idx === 0 ? 'FRONT' : idx === currentQueue.length - 1 ? 'REAR' : `${idx}`,
      subLabel: idx === 0 ? 'Next out' : '',
    }));
  };

  steps.push({
    stepIndex: steps.length,
    description: 'Initialized empty Queue. size = 0.',
    elements: [],
    variables: { front: null, rear: null, size: 0, lastOp: 'INIT' },
    codeLine: { java: 2, python: 4 },
    explanation: {
      why: 'Empty queue ready.',
      whatNext: 'Execute enqueue and dequeue actions.',
      keyTakeaway: 'FIFO: First items inserted are the first items removed.',
    },
  });

  for (const op of operations) {
    const parts = op.trim().split(' ');
    const command = parts[0].toUpperCase();
    const arg = parts.length > 1 ? parseInt(parts[1], 10) : undefined;

    if (command === 'ENQUEUE' && arg !== undefined) {
      currentQueue.push(arg);
      steps.push({
        stepIndex: steps.length,
        description: `ENQUEUE ${arg}: Added ${arg} at the REAR of the queue.`,
        elements: getVisualElements('ENQUEUE'),
        variables: {
          front: currentQueue[0],
          rear: currentQueue[currentQueue.length - 1],
          size: currentQueue.length,
          enqueued: arg,
          lastOp: 'ENQUEUE',
        },
        changedVariables: ['rear', 'size', 'enqueued'],
        codeLine: { java: 5, python: 8 },
        explanation: {
          why: `Placed ${arg} at the end of the line.`,
          whatNext: 'Ready for next operation.',
          keyTakeaway: 'Enqueue adds to rear in O(1).',
        },
      });
    } else if (command === 'DEQUEUE') {
      if (currentQueue.length > 0) {
        const dequeued = currentQueue.shift()!;
        steps.push({
          stepIndex: steps.length,
          description: `DEQUEUE: Removed element ${dequeued} from FRONT of queue.`,
          elements: getVisualElements('DEQUEUE'),
          variables: {
            front: currentQueue.length > 0 ? currentQueue[0] : null,
            rear: currentQueue.length > 0 ? currentQueue[currentQueue.length - 1] : null,
            size: currentQueue.length,
            dequeued,
            lastOp: 'DEQUEUE',
          },
          changedVariables: ['front', 'size', 'dequeued'],
          codeLine: { java: 9, python: 13 },
          explanation: {
            why: `Oldest remaining item removed from front.`,
            whatNext: 'Next operation.',
            keyTakeaway: 'FIFO discipline maintained.',
          },
        });
      }
    }
  }

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
