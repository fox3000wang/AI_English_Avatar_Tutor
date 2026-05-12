import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#17211d",
        mint: "#d9f7e8",
        coral: "#ff7a5c",
        paper: "#fbf7ef",
      },
    },
  },
  plugins: [],
};

export default config;
