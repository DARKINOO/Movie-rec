import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  content: ["./src/**/*.{js,jsx,ts,tsx}",],
  darkMode: 'class', // Use class-based dark mode
  theme: {
    extend: {
      colors: {
        red: {
          50: '#FFF5F5',
          100: '#FFEAEA',
          200: '#FFCCCC',
          300: '#FFADAD',
          400: '#FF7A7A',
          500: '#FF3B3B',
          600: '#FF2063',
          700: '#E50914',
          800: '#B80C10',
          900: '#960A0D',
        },
        indigo: {
          50: '#F6F5FF',
          100: '#EDEBFE',
          200: '#DCD7FE',
          300: '#CABFFD',
          400: '#AC9EFC',
          500: '#9B90F8',
          600: '#7B6EF6',
          700: '#5E4BD1',
          800: '#4E3FAB',
          900: '#362C78',
        },
        gray: {
          50: '#F5F7FA',
          100: '#E4E7EB',
          200: '#CBD2D9',
          300: '#9AA5B1',
          400: '#7B8794',
          500: '#616E7C',
          600: '#52606D',
          700: '#3E4C59',
          800: '#1A2037',
          900: '#121829',
        }
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
      boxShadow: {
        card: '0 8px 16px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [react(),
    tailwindcss(),
  ],
})
