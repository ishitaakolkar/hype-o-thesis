// tailwind.config.js
module.exports = {
    purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
    darkMode: false, // or 'media' or 'class'
    theme: {
      extend: {
        colors: {
          'teal-custom': '#14b8a6',
        },
      },
    },
    variants: {
      extend: {},
    },
    plugins: [],
  };