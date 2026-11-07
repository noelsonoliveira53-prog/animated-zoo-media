import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  build: {
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      // Phaser (~1.2 MB) only changes when we bump it, so ship it as its own chunk:
      // players keep it cached across game updates and only re-download the game code.
      output: { manualChunks: { phaser: ['phaser'] } },
    },
  },
  test: {
    include: ['tests/**/*.test.ts'],
  },
} as any);
