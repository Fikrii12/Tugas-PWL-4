import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['react-spring'],
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:6543', 
        changeOrigin: true,
      },
    },
  },
});