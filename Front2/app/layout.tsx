import type { Metadata } from "next";
import "./globals.css";
import Body from "./Body";
import { useState } from "react";

export const metadata: Metadata = {
  title: "Spot On",
  description: "YBIGTA DS",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
      <link href='https://unpkg.com/boxicons@2.1.1/css/boxicons.min.css' rel='stylesheet' />
      </head>
      <Body>
      {children}
      </Body>
    </html>
  );
}
