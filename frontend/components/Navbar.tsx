import Link from "next/link";

export function Navbar() {
  return (
    <header className="nav">
      <div className="nav-inner">
        <Link href="/" className="brand" aria-label="iDoc home">
          <span role="img" aria-label="sparkle">
            ✨
          </span>
          iDoc
          <span className="chip">Medical directory</span>
        </Link>
        <nav className="nav-links">
          <Link href="/">Home</Link>
          <Link href="/clinics">Clinics</Link>
          <Link href="/clinics">Book</Link>
        </nav>
      </div>
    </header>
  );
}
