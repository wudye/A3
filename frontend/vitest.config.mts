import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
 
export default defineConfig({
    resolve: {
        alias: {
            '@': '/src',
        },
        tsconfigPaths: true,
    },
    plugins: [react()],
    test: {
        include: ['tests/unit/**/*.test.ts', 'tests/integration/*.test.ts'],
        environment: 'jsdom',
    },
})