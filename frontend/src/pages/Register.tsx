import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../api/client";

export default function Register() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await apiClient.post("/auth/register", { name, email, password });
      navigate("/login");
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } }).response?.data?.detail;
      setError(detail ?? "Unable to create the account.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#0b0b0b] px-4 py-16 text-white">
      <div className="mx-auto max-w-md">
        <div className="mb-8">
          <div className="text-amber-400 text-lg font-semibold">NutriCoach</div>
          <h1 className="mt-3 text-5xl font-bold tracking-tight">Create account</h1>
          <p className="mt-3 text-lg text-slate-400">Start building your personalized nutrition plan.</p>
        </div>
        <form onSubmit={submit} className="rounded-3xl border border-white/10 bg-white/[0.04] p-8 shadow-2xl">
          {error && <div className="mb-5 rounded-xl border border-red-400/30 bg-red-400/10 p-3 text-sm text-red-200">{error}</div>}
          <label className="block text-sm text-slate-300">Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required className="mt-2 w-full rounded-2xl border border-white/10 bg-white/[0.05] px-4 py-4 text-white outline-none focus:border-amber-400" />
          <label className="mt-5 block text-sm text-slate-300">Email</label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required className="mt-2 w-full rounded-2xl border border-white/10 bg-white/[0.05] px-4 py-4 text-white outline-none focus:border-amber-400" />
          <label className="mt-5 block text-sm text-slate-300">Password</label>
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" minLength={8} required className="mt-2 w-full rounded-2xl border border-white/10 bg-white/[0.05] px-4 py-4 text-white outline-none focus:border-amber-400" />
          <button disabled={busy} className="mt-6 w-full rounded-2xl bg-amber-400 px-4 py-4 font-bold text-black disabled:opacity-60">{busy ? "Creating..." : "Create account"}</button>
          <p className="mt-6 text-center text-slate-400">Already have an account? <Link className="text-amber-400 font-semibold" to="/login">Sign in</Link></p>
        </form>
      </div>
    </main>
  );
}
