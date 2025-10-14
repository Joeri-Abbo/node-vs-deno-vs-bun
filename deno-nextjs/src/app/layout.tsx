import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Deno Next.js App',
  description: 'Next.js app running on Deno',
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