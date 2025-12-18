import Link from "next/link";
import { Navbar } from "@/components/Navbar";
import { ClinicCard } from "@/components/ClinicCard";
import { DoctorCard } from "@/components/DoctorCard";
import { fetchClinics, fetchDoctors } from "@/lib/api";

export default async function Page() {
  const [clinics, doctors] = await Promise.all([fetchClinics(), fetchDoctors()]);
  const featuredClinics = clinics.slice(0, 6);
  const featuredDoctors = doctors.slice(0, 8);

  return (
    <div>
      <Navbar />
      <main className="page-shell">
        <section className="hero">
          <div>
            <div className="pill-row">
              <div className="surface-block">Directory · Clinics · Doctors</div>
              <div className="surface-block">Book instantly</div>
            </div>
            <h1>Find the right medical care in one calm place.</h1>
            <p>
              Explore trusted clinics, browse specialists, and confirm an appointment in
              moments. Designed to keep every step clear, modern, and reassuring—no clutter, no
              gradients, just clarity.
            </p>
            <div className="hero-actions">
              <Link href="/clinics" className="primary-btn">
                Browse clinics
              </Link>
              <Link href="/clinics" className="ghost-btn">
                Make an appointment
              </Link>
            </div>
          </div>
          <div className="stack">
            <div className="card">
              <h3>Today&apos;s highlights</h3>
              <p className="muted">Handpicked picks to get you started.</p>
              <div className="divider" />
              <div className="stack">
                <div className="surface-block">Clinics available: {clinics.length}</div>
                <div className="surface-block">Doctors listed: {doctors.length}</div>
              </div>
            </div>
            <div className="card">
              <h3>Popular specialties</h3>
              <div className="badge-row">
                {["Cardiology", "Dermatology", "Family Medicine", "Neurology", "Pediatrics"].map(
                  (s) => (
                    <span key={s} className="tag">
                      {s}
                    </span>
                  )
                )}
              </div>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <div className="section-title">
              <h2>Featured clinics</h2>
              <span>Carefully curated selection</span>
            </div>
            <Link href="/clinics" className="ghost-btn">
              View all clinics
            </Link>
          </div>
          <div className="grid">
            {featuredClinics.map((clinic) => (
              <ClinicCard key={clinic.id} clinic={clinic} />
            ))}
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <div className="section-title">
              <h2>Doctors you can trust</h2>
              <span>Across specialties and clinics</span>
            </div>
            <Link href="/clinics" className="ghost-btn">
              Book a visit
            </Link>
          </div>
          <div className="grid">
            {featuredDoctors.map((doctor) => {
              const clinic = clinics.find((c) => c.id === doctor.clinic_id);
              return <DoctorCard key={doctor.id} doctor={doctor} clinicName={clinic?.name} />;
            })}
          </div>
        </section>
      </main>
    </div>
  );
}
