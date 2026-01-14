// [Task]: T026 | [Spec]: specs/002-phase-02-web-app/spec.md
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // Enable dark mode with class strategy (for User Story 7)
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6', // blue-500
          dark: '#2563eb', // blue-600
          light: '#60a5fa', // blue-400
        },
        secondary: {
          DEFAULT: '#6b7280', // gray-500
          dark: '#4b5563', // gray-600
          light: '#9ca3af', // gray-400
        },
        danger: {
          DEFAULT: '#ef4444', // red-500
          dark: '#dc2626', // red-600
          light: '#f87171', // red-400
        },
      },
      screens: {
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
        '2xl': '1536px',
      },
    },
  },
  plugins: [],
}

export default config
