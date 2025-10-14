import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Bun Next.js App',
  description: 'Next.js app running on Bun',
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