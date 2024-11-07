/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

const primary = colors.blue

module.exports = {
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors: {
        primary
      },
    },
  },
  plugins: [],
}
