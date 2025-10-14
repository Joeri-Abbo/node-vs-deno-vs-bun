import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Node.js Next.js App',
  description: 'Next.js app running on Node.js',
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