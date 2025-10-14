export default function HomePage() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Deno Next.js Application</h1>
      <p>This is a Next.js application running on Deno runtime.</p>
      <div>
        <h2>System Info</h2>
        <p>Runtime: Deno</p>
        <p>Framework: Next.js</p>
        <p>Port: 3002</p>
      </div>
      <div>
        <h2>Performance Test</h2>
        <p>This app is used for comparing memory and CPU usage across different JavaScript runtimes.</p>
      </div>
    </div>
  )
}