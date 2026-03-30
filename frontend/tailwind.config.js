/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        card: 'rgba(255,255,255,0.08)'
      },
      boxShadow: {
        glow: '0 8px 30px rgba(56, 189, 248, 0.15)'
      }
    }
  },
  plugins: []
}
