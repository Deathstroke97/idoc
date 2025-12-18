"use client";

import { useMemo, useState } from "react";
import type { Clinic, Doctor } from "@/lib/api";
import { createAppointment } from "@/lib/api";

type Props = {
  clinic: Clinic;
};

type FormState = {
  doctorId: number | "";
  date: string;
  time: string;
  userName: string;
  userPhone: string;
};

export function AppointmentModal({ clinic }: Props) {
  const hasDoctors = clinic.doctors.length > 0;
  const [open, setOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<{
    doctor?: Doctor;
    details?: { date: string; time: string; userName: string; userPhone: string };
  } | null>(null);

  const initialDoctorId = clinic.doctors[0]?.id ?? "";

  const [form, setForm] = useState<FormState>({
    doctorId: initialDoctorId,
    date: "",
    time: "",
    userName: "",
    userPhone: "",
  });

  const selectedDoctor = useMemo(
    () => clinic.doctors.find((d) => d.id === form.doctorId),
    [clinic.doctors, form.doctorId]
  );

  const close = () => {
    setOpen(false);
    setError(null);
    setSubmitting(false);
    setSuccess(null);
    setForm({
      doctorId: initialDoctorId,
      date: "",
      time: "",
      userName: "",
      userPhone: "",
    });
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.doctorId || !form.date || !form.time || !form.userName || !form.userPhone) {
      setError("Please fill all fields.");
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await createAppointment({
        clinic_id: clinic.id,
        doctor_id: Number(form.doctorId),
        date: form.date,
        time: form.time,
        user_name: form.userName,
        user_phone: form.userPhone,
      });
      setSuccess({
        doctor: selectedDoctor,
        details: {
          date: form.date,
          time: form.time,
          userName: form.userName,
          userPhone: form.userPhone,
        },
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <button
        className="primary-btn"
        onClick={() => setOpen(true)}
        disabled={!hasDoctors}
        title={!hasDoctors ? "No doctors available to book right now." : undefined}
      >
        Make appointment
      </button>

      {open && (
        <div className="modal-backdrop" role="dialog" aria-modal="true">
          <div className="modal">
            <button className="modal-close" onClick={close} aria-label="Close modal">
              ×
            </button>
            <h2 style={{ marginTop: 0 }}>Book at {clinic.name}</h2>
            <p className="muted" style={{ marginTop: 4 }}>
              Choose a doctor and time. You will get a confirmation instantly.
            </p>

            {error && <div className="error" role="alert">{error}</div>}

            {!hasDoctors ? (
              <div className="empty-state">No doctors available to book.</div>
            ) : success ? (
              <div className="success-box">
                <div>Appointment is done ✅</div>
                <div>Clinic: {clinic.name}</div>
                {success.doctor && <div>Doctor: {success.doctor.name}</div>}
                {success.details && (
                  <>
                    <div>Date: {success.details.date}</div>
                    <div>Time: {success.details.time}</div>
                    <div>Patient: {success.details.userName}</div>
                    <div>Phone: {success.details.userPhone}</div>
                  </>
                )}
                <button className="ghost-btn" onClick={close} style={{ marginTop: 8 }}>
                  Close
                </button>
              </div>
            ) : (
              <form className="form" onSubmit={onSubmit}>
                <div className="field">
                  <label htmlFor="doctor">Doctor</label>
                  <select
                    id="doctor"
                    value={form.doctorId}
                    onChange={(e) => setForm((f) => ({ ...f, doctorId: Number(e.target.value) }))}
                    required
                  >
                    {clinic.doctors.map((doctor) => (
                      <option key={doctor.id} value={doctor.id}>
                        {doctor.name} · {doctor.specialty}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="field">
                  <label htmlFor="date">Date</label>
                  <input
                    id="date"
                    type="date"
                    value={form.date}
                    onChange={(e) => setForm((f) => ({ ...f, date: e.target.value }))}
                    required
                  />
                </div>

                <div className="field">
                  <label htmlFor="time">Time</label>
                  <input
                    id="time"
                    type="time"
                    value={form.time}
                    onChange={(e) => setForm((f) => ({ ...f, time: e.target.value }))}
                    required
                  />
                </div>

                <div className="field">
                  <label htmlFor="name">Your name</label>
                  <input
                    id="name"
                    type="text"
                    placeholder="Full name"
                    value={form.userName}
                    onChange={(e) => setForm((f) => ({ ...f, userName: e.target.value }))}
                    required
                  />
                </div>

                <div className="field">
                  <label htmlFor="phone">Phone</label>
                  <input
                    id="phone"
                    type="tel"
                    placeholder="+1 555 123 4567"
                    value={form.userPhone}
                    onChange={(e) => setForm((f) => ({ ...f, userPhone: e.target.value }))}
                    required
                  />
                </div>

                <div className="cta-bar">
                  <button className="primary-btn" type="submit" disabled={submitting}>
                    {submitting ? "Booking..." : "Confirm appointment"}
                  </button>
                  <button type="button" className="ghost-btn" onClick={close}>
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  );
}
