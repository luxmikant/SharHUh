/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'nexus': {
          'dark': '#0a0a0f',
          'darker': '#05050a',
          'primary': '#00ffff',
          'secondary': '#ff00ff',
          'success': '#00ff00',
          'warning': '#ffaa00',
          'danger': '#ff0000',
          'lcars-orange': '#ff9900',
          'lcars-purple': '#9999ff',
          'lcars-blue': '#99ccff',
        }
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
        'lcars': ['Antonio', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-fast': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px currentColor, 0 0 10px currentColor' },
          '100%': { boxShadow: '0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor' }
        }
      }
    },
  },
  plugins: [],
}
