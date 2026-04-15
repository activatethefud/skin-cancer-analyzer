import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Skin Cancer Analyzer',
  description: 'AI-powered skin lesion analysis',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
