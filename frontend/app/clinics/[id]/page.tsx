import { notFound } from "next/navigation";
import { Navbar } from "@/components/Navbar";
import { DoctorCard } from "@/components/DoctorCard";
import { fetchClinics } from "@/lib/api";
import { AppointmentModal } from "@/components/AppointmentModal";

type Props = { params: { id: string } };

export default async function ClinicDetailPage({ params }: Props) {
  const clinics = await fetchClinics();
  const clinic = clinics.find((c) => String(c.id) === params.id);

  if (!clinic) {
    return notFound();
  }

  return (
    <div>
      <Navbar />
      <main className="page-shell">
        <div className="clinic-hero">
          <div className="tag">Clinic ID · {clinic.id}</div>
          <h1>{clinic.name}</h1>
          <p className="muted">
            Specialists across key disciplines. Transparent availability, zero clutter.
          </p>
          <div className="cta-bar">
            <AppointmentModal clinic={clinic} />
            <a className="ghost-btn" href="/clinics">
              Back to clinics
            </a>
          </div>
        </div>

        <section className="section">
          <div className="section-header">
            <div className="section-title">
              <h2>Doctors in this clinic</h2>
              <span>{clinic.doctors.length} specialists</span>
            </div>
          </div>

          {clinic.doctors.length === 0 ? (
            <div className="empty-state">No doctors listed yet.</div>
          ) : (
            <div className="doctor-list">
              {clinic.doctors.map((doctor) => (
                <DoctorCard key={doctor.id} doctor={doctor} clinicName={clinic.name} />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
