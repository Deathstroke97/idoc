import type { Doctor } from "@/lib/api";

type Props = {
  doctor: Doctor;
  clinicName?: string;
};

export function DoctorCard({ doctor, clinicName }: Props) {
  return (
    <div className="card">
      <div className="doctor-name">{doctor.name}</div>
      <p className="muted">{doctor.specialty}</p>
      {clinicName && <span className="tag">Clinic · {clinicName}</span>}
    </div>
  );
}
