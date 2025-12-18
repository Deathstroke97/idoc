"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Navbar } from "@/components/Navbar";
import {
  cancelAppointment,
  fetchAppointments,
  fetchClinics,
  fetchDoctors,
  type AppointmentResponse,
  type Clinic,
  type Doctor,
} from "@/lib/api";

export default function AppointmentsPage() {
  const [userPhone, setUserPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [appointments, setAppointments] = useState<AppointmentResponse[]>([]);
  const [clinics, setClinics] = useState<Clinic[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);

  const clinicById = useMemo(() => {
    const map = new Map<number, Clinic>();
    clinics.forEach((c) => map.set(c.id, c));
    return map;
  }, [clinics]);

  const doctorById = useMemo(() => {
    const map = new Map<number, Doctor>();
    doctors.forEach((d) => map.set(d.id, d));
    return map;
  }, [doctors]);

  const load = useCallback(
    async (phone?: string) => {
      setLoading(true);
      setError(null);
      try {
        const [apps, allClinics, allDoctors] = await Promise.all([
          fetchAppointments(phone),
          fetchClinics(),
          fetchDoctors(),
        ]);
        setAppointments(apps);
        setClinics(allClinics);
        setDoctors(allDoctors);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Something went wrong.");
      } finally {
        setLoading(false);
      }
    },
    [setAppointments]
  );

  useEffect(() => {
    load(undefined);
  }, [load]);

  const onSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = userPhone.trim();
    await load(trimmed ? trimmed : undefined);
  };

  const onCancel = async (id: number) => {
    setError(null);
    try {
      await cancelAppointment(id);
      const trimmed = userPhone.trim();
      await load(trimmed ? trimmed : undefined);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    }
  };

  return (
    <div>
      <Navbar />
      <main className="page-shell">
        <section className="section" style={{ marginTop: 0 }}>
          <div className="section-header">
            <div className="section-title">
              <h2>My appointments</h2>
              <span>View and cancel bookings</span>
            </div>
          </div>

          <div className="card">
            <form className="form" onSubmit={onSearch}>
              <div className="field">
                <label htmlFor="phone">Filter by phone (optional)</label>
                <input
                  id="phone"
                  type="tel"
                  placeholder="+1 555 123 4567"
                  value={userPhone}
                  onChange={(e) => setUserPhone(e.target.value)}
                />
              </div>
              <div className="cta-bar">
                <button
                  className="primary-btn"
                  type="submit"
                  disabled={loading}
                >
                  {loading ? "Loading..." : "Search"}
                </button>
                <button
                  className="ghost-btn"
                  type="button"
                  onClick={() => {
                    setUserPhone("");
                    load(undefined);
                  }}
                  disabled={loading}
                >
                  Clear
                </button>
              </div>
            </form>
          </div>

          {error && (
            <div className="error" role="alert" style={{ marginTop: 16 }}>
              {error}
            </div>
          )}

          <div style={{ marginTop: 16 }}>
            {loading ? (
              <div className="empty-state">Loading appointments...</div>
            ) : appointments.length === 0 ? (
              <div className="empty-state">No appointments found.</div>
            ) : (
              <div className="grid">
                {appointments.map((a) => {
                  const clinicName = clinicById.get(a.clinic_id)?.name;
                  const doctor = doctorById.get(a.doctor_id);
                  return (
                    <div key={a.id} className="card">
                      <div className="tag">Appointment · #{a.id}</div>
                      <h3 style={{ marginTop: 10, marginBottom: 6 }}>
                        {doctor?.name || `Doctor #${a.doctor_id}`}
                      </h3>
                      <p className="muted" style={{ marginTop: 0 }}>
                        {doctor?.specialty ? `${doctor.specialty} · ` : ""}
                        {clinicName || `Clinic #${a.clinic_id}`}
                      </p>
                      <div className="divider" />
                      <div className="stack">
                        <div className="surface-block">Date: {a.date}</div>
                        <div className="surface-block">Time: {a.time}</div>
                        <div className="surface-block">
                          Patient: {a.user_name}
                        </div>
                        <div className="surface-block">
                          Phone: {a.user_phone}
                        </div>
                      </div>
                      <div className="cta-bar" style={{ marginTop: 14 }}>
                        <button
                          className="ghost-btn"
                          type="button"
                          onClick={() => onCancel(a.id)}
                        >
                          Cancel appointment
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
