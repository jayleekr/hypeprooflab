import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HypeProof AI",
  description: "AI solves problems. Humans define them.",
  icons: {
    icon: "/favicon.ico",
  },
  openGraph: {
    title: "HypeProof AI",
    description: "AI solves problems. Humans define them.",
    url: "https://hypeproof-ai.xyz",
    siteName: "HypeProof AI",
    images: [
      {
        url: "https://hypeproof-ai.xyz/og-image.png",
        width: 1200,
        height: 630,
        alt: "HypeProof AI - We don't chase Hype. We prove it.",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "HypeProof AI",
    description: "AI solves problems. Humans define them.",
    images: ["https://hypeproof-ai.xyz/og-image.png"],
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
