import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { ClinicCard } from "@/components/ClinicCard";
import { fetchClinics } from "@/lib/api";

export const revalidate = 0;

export default async function ClinicsPage() {
  const clinics = await fetchClinics();

  return (
    <div>
      <Navbar />
      <main className="page-shell">
        <header className="section-header">
          <div className="section-title">
            <h2>Clinics</h2>
            <span>Explore trusted locations and specialties</span>
          </div>
          <div className="badge-row">
            <span className="tag">Total · {clinics.length}</span>
            <Link href="/" className="ghost-btn">
              Back to home
            </Link>
          </div>
        </header>

        {clinics.length === 0 ? (
          <div className="empty-state">No clinics yet. Please seed the backend.</div>
        ) : (
          <div className="grid">
            {clinics.map((clinic) => (
              <ClinicCard key={clinic.id} clinic={clinic} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
