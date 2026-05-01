import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Flappy Bird Platform",
  description: "Flappy Bird web game with leaderboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-sky-100 min-h-screen font-sans">{children}</body>
    </html>
  );
}
