import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI English Tutor",
  description: "Student voice chat for AI English Avatar Tutor",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
