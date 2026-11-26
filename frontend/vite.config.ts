import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { localJudgePlugin } from './judge/localJudge';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export default defineConfig({
  // The local judge compiles/runs Java & Python submissions directly in the dev server
  // (set ALGOPLAY_JUDGE=backend to use the Spring Boot judge on :8080 instead).
  plugins: [react(), localJudgePlugin({ repoRoot })],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
});
