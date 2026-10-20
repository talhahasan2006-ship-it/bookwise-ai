/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B1020',
        secondary: '#11182B',
        card: '#171F35',
        'card-hover': '#1E294B',
        accent: {
          purple: '#8B5CF6',
          blue: '#38BDF8',
          glow: 'rgba(139, 92, 246, 0.15)',
        },
        text: {
          primary: '#F8FAFC',
          secondary: '#94A3B8',
          muted: '#64748B',
        },
        border: {
          subtle: '#1E293B',
          glow: 'rgba(139, 92, 246, 0.3)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 8px 30px rgba(0, 0, 0, 0.35)',
        'card-hover': '0 12px 35px rgba(139, 92, 246, 0.2)',
        'glow': '0 0 25px rgba(139, 92, 246, 0.25)',
      }
    },
  },
  plugins: [],
}
