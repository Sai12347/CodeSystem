import path from 'node:path';
import { readFileSync } from 'node:fs';
import { describe, it, expect } from 'vitest';
import { LocalJudge, compareOutputs } from '../../judge/localJudge';

const repoRoot = path.resolve(__dirname, '../../..');
const judge = new LocalJudge({ repoRoot });

describe('LocalJudge output comparison', () => {
  it('supports exact, float, sorted, sortedDeep, and anyOf modes', () => {
    expect(compareOutputs([1, 2], [1, 2], 'exact')).toBe(true);
    expect(compareOutputs([1, 2], [2, 1], 'exact')).toBe(false);
    expect(compareOutputs(3.14159, 3.141594, 'float')).toBe(true);
    expect(compareOutputs(3.14, 3.15, 'float')).toBe(false);
    expect(compareOutputs([1, 2, 3], [3, 1, 2], 'sorted')).toBe(true);
    expect(compareOutputs([[1, 2], [3, 4]], [[4, 3], [2, 1]], 'sortedDeep')).toBe(true);
    expect(compareOutputs([[0, 1], [1, 0]], [1, 0], 'anyOf')).toBe(true);
  });
});

describe('LocalJudge execution engine', () => {
  it('reports health with Java, Python, and loaded problem bank', () => {
    const h = judge.health();
    expect(h.status).toBe('UP');
    expect(h.loadedProblems).toBeGreaterThan(200);
    expect(h.javaAvailable).toBe(true);
    expect(h.pythonAvailable).toBe(true);
  });

  it('compiles and accepts reference Java & Python solutions and rejects broken code', async () => {
    const arrays = JSON.parse(
      readFileSync(path.join(repoRoot, 'frontend/src/data/problems/arrays.json'), 'utf8')
    );
    const twoSum = arrays.find((p: any) => p.slug === 'two-sum');
    expect(twoSum).toBeDefined();

    const pyOk = await judge.evaluate(
      { problemId: 'two-sum', language: 'python', code: twoSum.solutionCode.python },
      false
    );
    expect(pyOk.status).toBe('ACCEPTED');
    expect(pyOk.passedCount).toBe(pyOk.totalCount);
    expect(pyOk.hiddenTotal).toBeGreaterThan(0);

    const javaOk = await judge.evaluate(
      { problemId: 'two-sum', language: 'java', code: twoSum.solutionCode.java },
      false
    );
    expect(javaOk.status).toBe('ACCEPTED');
    expect(javaOk.passedCount).toBe(javaOk.totalCount);

    const javaCompileErr = await judge.evaluate(
      {
        problemId: 'two-sum',
        language: 'java',
        code: '  public class Solution {\n    public int[] twoSum(int[] nums, int target) { return nums }\n}',
      },
      true
    );
    expect(javaCompileErr.status).toBe('COMPILATION_ERROR');
    expect(javaCompileErr.compileError).toContain('Solution.java:2:');

    const pySyntaxErr = await judge.evaluate(
      {
        problemId: 'two-sum',
        language: 'python',
        code: 'class Solution:\n    def twoSum(self, nums, target)\n        return []\n',
      },
      true
    );
    expect(pySyntaxErr.status).toBe('COMPILATION_ERROR');
    expect(pySyntaxErr.compileError).toContain('line 2');
  }, 30_000);
});
