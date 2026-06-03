import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import {resolve} from "path"


export default defineConfig({
    resolve: {
        alias: {
            "@": resolve(__dirname, "src"),
        },
        tsconfigPaths: true,
    },
    plugins: [react()],
    test: {
        globals: true,
        environment: 'jsdom',
        include: ['tests/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
        coverage: {
            provider: 'v8',
            reporter: ['text', 'json', 'html'],
        },
    

    }
})

