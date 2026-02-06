import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HypeProof AI",
  description: "AI가 문제를 푼다. 인간은 문제를 정의한다.",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
