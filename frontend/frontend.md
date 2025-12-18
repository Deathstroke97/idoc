# Frontend (Next.js App Router)

Modern UI for the medical directory (clinics, doctors, appointment booking).

## Stack
- Next.js 14 (App Router, TypeScript)
- React 18
- CSS (globals in `app/globals.css`), Google Font (Manrope)

## Project layout
- `app/layout.tsx` — root layout, font + global styles
- `app/page.tsx` — landing page (hero + featured clinics & doctors)
- `app/clinics/page.tsx` — clinics list page
- `app/clinics/[id]/page.tsx` — clinic detail with doctors + appointment modal
- `components/` — UI components (Navbar, cards, AppointmentModal)
- `lib/api.ts` — API client for backend endpoints
- `globals.css` — tokens and layout styles

## Backend contract (consumed)
- `GET /clinics` — returns clinics with embedded doctors
- `GET /doctors` — returns doctors (optionally by `clinic_id`)
- `POST /make-appointmet` — create appointment
- Base URL configurable via `NEXT_PUBLIC_API_BASE_URL` (defaults to `http://localhost:8000`)

## Running the frontend
From `frontend/`:
```bash
npm install
npm run dev -- --hostname 0.0.0.0 --port 3000
```
Open http://localhost:3000

## Notes
- No gradients per design requirement; uses soft surfaces, cards, and chips.
- Appointment modal swaps to a success state after submission, showing appointment details.
- If no doctors exist in a clinic, booking is disabled and an empty-state message is shown.
- Typed route config is enabled (`next.config.mjs`).
