import Link from "next/link";
import type { Clinic } from "@/lib/api";

type Props = {
  clinic: Clinic;
};

export function ClinicCard({ clinic }: Props) {
  return (
    <Link href={`/clinics/${clinic.id}`} className="card" aria-label={`Open ${clinic.name}`}>
      <h3>{clinic.name}</h3>
      <p className="muted">{clinic.doctors.length} doctors · Multi-specialty</p>
      <div className="badge-row" aria-hidden="true">
        {clinic.doctors.slice(0, 3).map((d) => (
          <span key={d.id} className="tag">
            {d.specialty}
          </span>
        ))}
        {clinic.doctors.length > 3 && <span className="tag">+{clinic.doctors.length - 3} more</span>}
      </div>
    </Link>
  );
}
