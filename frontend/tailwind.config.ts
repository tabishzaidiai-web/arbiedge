import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef7ff',
          100: '#d9ecff',
          200: '#bcdfff',
          300: '#8eccff',
          400: '#59afff',
          500: '#338cff',
          600: '#1a6df5',
          700: '#1357e1',
          800: '#1647b6',
          900: '#183f8f',
          950: '#142857',
        },
      },
    },
  },
  plugins: [],
};

export default config;
