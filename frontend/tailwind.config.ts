import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#08111f",
        panel: "#101c2e",
        cyan: "#31d6c4",
        amber: "#ffb84d",
      },
      boxShadow: {
        glow: "0 0 40px rgba(49, 214, 196, 0.12)",
      },
    },
  },
  plugins: [],
};

export default config;

