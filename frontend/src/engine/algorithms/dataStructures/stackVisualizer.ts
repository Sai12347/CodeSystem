import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const stackMetadata: AlgorithmMetadata = {
  id: 'stack',
  title: 'Stack (LIFO Data Structure)',
  category: 'INTERMEDIATE',
  subcategory: 'Data Structures',
  difficulty: 'Easy',
  description:
    'A Last-In-First-Out (LIFO) abstract data type with operations Push, Pop, and Peek.',
  realWorldExample:
    'A stack of cafeteria trays or your browser’s Back button history: the last page visited is the first page returned to.',
  timeComplexity: {
    best: 'O(1) (push, pop, peek)',
    average: 'O(1)',
    worst: 'O(1)',
  },
  spaceComplexity: 'O(n) space for storing n items',
  commonMistakes: [
    'Popping or peeking from an empty stack (StackUnderflowException).',
    'Mixing up LIFO with FIFO (queue).',
  ],
  defaultInput: ['PUSH 10', 'PUSH 25', 'PUSH 40', 'PEEK', 'POP', 'PUSH 50'],
  code: {
    java: `public class ArrayStack {
    private int[] stack = new int[100];
    private int top = -1;

    public void push(int val) {
        stack[++top] = val;
    }
    public int pop() {
        if (top == -1) throw new EmptyStackException();
        return stack[top--];
    }
    public int peek() {
        return stack[top];
    }
}`,
    python: `class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, val):
        self.stack.append(val)
        
    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()
        
    def peek(self):
        return self.stack[-1]`,
  },
};

export function generateStackSteps(operations: string[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const currentStack: number[] = [];

  const getVisualElements = (action: string, targetVal?: number): VisualElement[] => {
    return currentStack.map((val, idx) => ({
      id: `stack-item-${idx}-${val}`,
      value: val,
      state: idx === currentStack.length - 1 ? 'active' : 'default',
      label: `top: ${idx}`,
      subLabel: idx === currentStack.length - 1 ? 'TOP' : '',
    }));
  };

  steps.push({
    stepIndex: steps.length,
    description: 'Initialized empty Stack. top = -1.',
    elements: [],
    variables: { top: -1, size: 0, lastOp: 'INIT' },
    codeLine: { java: 3, python: 3 },
    explanation: {
      why: 'Empty stack initialized.',
      whatNext: 'Execute sequence of push/pop operations.',
      keyTakeaway: 'Top pointer tracks the index of the most recently inserted item.',
    },
  });

  for (const op of operations) {
    const parts = op.trim().split(' ');
    const command = parts[0].toUpperCase();
    const arg = parts.length > 1 ? parseInt(parts[1], 10) : undefined;

    if (command === 'PUSH' && arg !== undefined) {
      currentStack.push(arg);
      steps.push({
        stepIndex: steps.length,
        description: `PUSH ${arg}: Placed ${arg} at top of stack (index ${currentStack.length - 1}).`,
        elements: getVisualElements('PUSH', arg),
        variables: { top: currentStack.length - 1, size: currentStack.length, pushed: arg, lastOp: 'PUSH' },
        changedVariables: ['top', 'size', 'pushed'],
        codeLine: { java: 6, python: 6 },
        explanation: {
          why: `Incremented top pointer and stored value ${arg}.`,
          whatNext: 'Ready for next operation.',
          keyTakeaway: 'Push operates in guaranteed O(1) constant time.',
        },
      });
    } else if (command === 'POP') {
      if (currentStack.length > 0) {
        const popped = currentStack.pop()!;
        steps.push({
          stepIndex: steps.length,
          description: `POP: Removed and returned top element ${popped}.`,
          elements: getVisualElements('POP', popped),
          variables: { top: currentStack.length - 1, size: currentStack.length, popped, lastOp: 'POP' },
          changedVariables: ['top', 'size', 'popped'],
          codeLine: { java: 10, python: 11 },
          explanation: {
            why: `Top element ${popped} removed, top pointer decremented to ${currentStack.length - 1}.`,
            whatNext: 'Next operation.',
            keyTakeaway: 'LIFO: Most recently pushed element is the first popped.',
          },
        });
      }
    } else if (command === 'PEEK') {
      const topVal = currentStack[currentStack.length - 1];
      steps.push({
        stepIndex: steps.length,
        description: `PEEK: Inspected top element without removing it. Value is ${topVal}.`,
        elements: getVisualElements('PEEK', topVal),
        variables: { top: currentStack.length - 1, size: currentStack.length, peeked: topVal, lastOp: 'PEEK' },
        changedVariables: ['peeked'],
        codeLine: { java: 13, python: 14 },
        explanation: {
          why: 'Examine current top of stack without modifying state.',
          whatNext: 'Next operation.',
          keyTakeaway: 'Peek is non-destructive O(1).',
        },
      });
    }
  }

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
