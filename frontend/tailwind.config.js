/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        apple: {
          bg: '#f5f5f7',
          darkBg: '#000000',
          card: '#ffffff',
          darkCard: '#161618',
          border: 'rgba(0,0,0,0.08)',
          darkBorder: 'rgba(255,255,255,0.12)',
          accent: '#0071e3',
          accentHover: '#0077ed',
          success: '#34c759',
          warning: '#ff9f0a',
          danger: '#ff3b30',
          purple: '#af52de',
          teal: '#30b0c7'
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Text"', '"SF Pro Display"', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['"SF Mono"', 'Menlo', 'Monaco', 'Consolas', 'monospace']
      },
      boxShadow: {
        'apple-sm': '0 2px 8px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06)',
        'apple-md': '0 4px 16px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04)',
        'apple-lg': '0 12px 32px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06)',
        'apple-glass': '0 8px 32px 0 rgba(0, 0, 0, 0.08)'
      },
      backdropBlur: {
        'apple': '20px'
      }
    },
  },
  plugins: [],
}
