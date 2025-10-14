export default function ErrorPage({ statusCode }) {
  return (
    <html>
      <body style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
        <h1>Application Error</h1>
        <p>Status code: {statusCode ?? 'unknown'}</p>
      </body>
    </html>
  )
}
