export type Doctor = {
  id: number;
  name: string;
  specialty: string;
  clinic_id: number;
};

export type Clinic = {
  id: number;
  name: string;
  doctors: Doctor[];
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8000";

async function handleJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json() as Promise<T>;
}

export async function fetchClinics(): Promise<Clinic[]> {
  const res = await fetch(`${API_BASE}/clinics`, { cache: "no-store" });
  return handleJson<Clinic[]>(res);
}

export async function fetchDoctors(clinicId?: number): Promise<Doctor[]> {
  const query = clinicId ? `?clinic_id=${clinicId}` : "";
  const res = await fetch(`${API_BASE}/doctors${query}`, { cache: "no-store" });
  return handleJson<Doctor[]>(res);
}

export type AppointmentPayload = {
  clinic_id: number;
  doctor_id: number;
  date: string;
  time: string;
  user_name: string;
  user_phone: string;
};

export type AppointmentResponse = {
  id: number;
  clinic_id: number;
  doctor_id: number;
  date: string;
  time: string;
  user_name: string;
  user_phone: string;
};

export async function createAppointment(
  payload: AppointmentPayload
): Promise<AppointmentResponse> {
  const res = await fetch(`${API_BASE}/make-appointmet`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleJson<AppointmentResponse>(res);
}

export const apiBase = API_BASE;
