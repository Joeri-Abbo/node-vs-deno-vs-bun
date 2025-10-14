export default function HomePage() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Bun Next.js Application</h1>
      <p>This is a Next.js application running on Bun runtime.</p>
      <div>
        <h2>System Info</h2>
        <p>Runtime: Bun</p>
        <p>Framework: Next.js</p>
        <p>Port: 3003</p>
      </div>
      <div>
        <h2>Performance Test</h2>
        <p>This app is used for comparing memory and CPU usage across different JavaScript runtimes.</p>
      </div>
    </div>
  )
}