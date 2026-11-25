import { describe, it, expect } from 'vitest';
import { AlgorithmEngine } from '../engine/core/AlgorithmEngine';
import { generateBinarySearchSteps } from '../engine/algorithms/searching/binarySearch';
import { generateBubbleSortSteps } from '../engine/algorithms/sorting/bubbleSort';
import { generateMergeSortSteps } from '../engine/algorithms/sorting/mergeSort';

describe('Algorithm Engine - Deterministic Step Execution', () => {
  it('Binary Search should find target in sorted array deterministically', () => {
    const arr = [2, 5, 8, 12, 16, 23, 38];
    const target = 16;
    const steps = generateBinarySearchSteps(arr, target);

    expect(steps.length).toBeGreaterThan(0);
    const lastStep = steps[steps.length - 1];
    expect(lastStep.variables.result).toBe(4);
    expect(lastStep.description).toContain('MATCH FOUND');
  });

  it('Binary Search should conclude target not found when absent', () => {
    const arr = [2, 5, 8, 12, 16, 23, 38];
    const target = 99;
    const steps = generateBinarySearchSteps(arr, target);

    const lastStep = steps[steps.length - 1];
    expect(lastStep.variables.result).toBe(-1);
    expect(lastStep.description).toContain('Target 99 not in array');
  });

  it('Bubble Sort should sort unsorted array and end in sorted state', () => {
    const input = [34, 12, 45, 9, 23, 18];
    const steps = generateBubbleSortSteps(input);

    expect(steps.length).toBeGreaterThan(0);
    const lastStep = steps[steps.length - 1];
    const finalValues = lastStep.elements.map((e) => e.value);
    expect(finalValues).toEqual([9, 12, 18, 23, 34, 45]);
  });

  it('Merge Sort should correctly sort array through divide and conquer', () => {
    const input = [38, 27, 43, 3, 9, 82, 10];
    const steps = generateMergeSortSteps(input);

    const lastStep = steps[steps.length - 1];
    const finalValues = lastStep.elements.map((e) => e.value);
    expect(finalValues).toEqual([3, 9, 10, 27, 38, 43, 82]);
  });

  it('AlgorithmEngine class should navigate steps, jump, and reset correctly', () => {
    const engine = new AlgorithmEngine('binary-search', {
      array: [10, 20, 30, 40, 50],
      target: 30,
    });

    expect(engine.getCurrentIndex()).toBe(0);
    const step1 = engine.nextStep();
    expect(step1).not.toBeNull();
    expect(engine.getCurrentIndex()).toBe(1);

    const prevStep = engine.previousStep();
    expect(prevStep).not.toBeNull();
    expect(engine.getCurrentIndex()).toBe(0);

    const total = engine.getTotalSteps();
    engine.jumpToStep(total - 1);
    expect(engine.getCurrentIndex()).toBe(total - 1);

    engine.reset();
    expect(engine.getCurrentIndex()).toBe(0);
  });
});
