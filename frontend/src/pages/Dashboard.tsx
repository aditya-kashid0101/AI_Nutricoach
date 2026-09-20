import { useEffect, useMemo, useState } from "react";
import { apiClient } from "../api/client";
import { useAuth } from "../context/AuthContext";
import type { Food, Intake, Nutrition, Profile, Recommendation } from "../types";

const emptyProfile: Profile = {
  age: 21,
  gender: "male",
  height_cm: 175,
  weight_kg: 70,
  fitness_goal: "maintenance",
  activity_level: "moderate",
};

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState<Profile>(emptyProfile);
  const [nutrition, setNutrition] = useState<Nutrition | null>(null);
  const [foods, setFoods] = useState<Food[]>([]);
  const [intake, setIntake] = useState<Intake[]>([]);
  const [selectedFood, setSelectedFood] = useState("");
  const [servings, setServings] = useState("1");
  const [meal, setMeal] = useState("lunch");
  const [aiText, setAiText] = useState("");
  const [aiSource, setAiSource] = useState("");
  const [aiBusy, setAiBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function load() {
    const [profileRes, foodsRes, intakeRes] = await Promise.all([
      apiClient.get<Profile | null>("/profile"),
      apiClient.get<Food[]>("/foods"),
      apiClient.get<Intake[]>("/foods/intake"),
    ]);
    setFoods(foodsRes.data);
    setIntake(intakeRes.data);
    if (profileRes.data) {
      setProfile(profileRes.data);
      const nutritionRes = await apiClient.get<Nutrition>("/nutrition/summary");
      setNutrition(nutritionRes.data);
    }
  }

  useEffect(() => {
    load().catch(() => setMessage("Could not load your dashboard."));
  }, []);

  const totals = useMemo(
    () =>
      intake.reduce(
        (acc, item) => ({
          calories: acc.calories + item.calories,
          protein: acc.protein + item.protein,
          carbs: acc.carbs + item.carbs,
          fat: acc.fat + item.fat,
        }),
        { calories: 0, protein: 0, carbs: 0, fat: 0 },
      ),
    [intake],
  );

  async function saveProfile() {
    setSaving(true);
    setMessage("");
    try {
      const res = await apiClient.put<Profile>("/profile", profile);
      setProfile(res.data);
      const nutritionRes = await apiClient.get<Nutrition>("/nutrition/summary");
      setNutrition(nutritionRes.data);
      setMessage("Profile and nutrition targets updated.");
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } }).response?.data?.detail;
      setMessage(detail ?? "Could not save the profile.");
    } finally {
      setSaving(false);
    }
  }

  async function logFood() {
    if (!selectedFood) return;
    await apiClient.post("/foods/intake", {
      food_id: Number(selectedFood),
      servings: Number(servings),
      meal_type: meal,
    });
    const res = await apiClient.get<Intake[]>("/foods/intake");
    setIntake(res.data);
    setMessage("Food logged.");
  }

  async function getRecommendation() {
    setAiBusy(true);
    setAiText("");
    try {
      const res = await apiClient.post<Recommendation>("/recommendations", {
        meal,
        preferences: "",
      });
      setAiText(res.data.recommendation);
      setAiSource(res.data.source);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } }).response?.data?.detail;
      setAiText(detail ?? "Could not generate a recommendation.");
    } finally {
      setAiBusy(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#0b0b0b] text-white">
      <header className="border-b border-white/10 bg-black/30">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <div className="font-semibold text-amber-400">NutriCoach</div>
            <div className="text-sm text-slate-500">Adaptive nutrition workspace</div>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm text-slate-400 sm:block">{user?.email}</span>
            <button onClick={logout} className="rounded-xl border border-white/10 px-4 py-2 text-sm hover:bg-white/5">Logout</button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold">Good to see you, {user?.name}</h1>
          <p className="mt-2 text-slate-400">Set your profile, track meals, and ask the AI coach what to eat next.</p>
        </div>

        {message && <div className="mb-6 rounded-xl border border-amber-400/20 bg-amber-400/10 p-3 text-sm text-amber-100">{message}</div>}

        <section className="grid gap-6 lg:grid-cols-3">
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 lg:col-span-1">
            <h2 className="text-xl font-semibold">Nutrition profile</h2>
            <p className="mt-1 text-sm text-slate-500">These inputs drive deterministic targets.</p>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <label className="text-sm text-slate-300">Age<input value={profile.age} onChange={(e) => setProfile({...profile, age: Number(e.target.value)})} type="number" className="mt-1 w-full rounded-xl border border-white/10 bg-black/20 p-3" /></label>
              <label className="text-sm text-slate-300">Gender<select value={profile.gender} onChange={(e) => setProfile({...profile, gender: e.target.value})} className="mt-1 w-full rounded-xl border border-white/10 bg-black/20 p-3"><option value="male">Male</option><option value="female">Female</option></select></label>
              <label className="text-sm text-slate-300">Height cm<input value={profile.height_cm} onChange={(e) => setProfile({...profile, height_cm: Number(e.target.value)})} type="number" className="mt-1 w-full rounded-xl border border-white/10 bg-black/20 p-3" /></label>
              <label className="text-sm text-slate-300">Weight kg<input value={profile.weight_kg} onChange={(e) => setProfile({...profile, weight_kg: Number(e.target.value)})} type="number" className="mt-1 w-full rounded-xl border border-white/10 bg-black/20 p-3" /></label>
            </div>

            <label className="mt-4 block text-sm text-slate-300">Goal<select value={profile.fitness_goal} onChange={(e) => setProfile({...profile, fitness_goal: e.target.value})} className="mt-1 w-full rounded-xl border border-white/10 bg-black/20 p-3"><option value="weight_loss">Weight loss</option><option value="muscle_gain">Muscle gain</option><option value="maintenance">Maintenance</option></select></label>

            <label className="mt-4 block text-sm text-slate-300">Activity<select value={profile.activity_level} onChange={(e) => setProfile({...profile, activity_level: e.target.value})} className="mt-1 w-full rounded-xl border border-white/10 bg-black/20 p-3"><option value="sedentary">Sedentary</option><option value="light">Light</option><option value="moderate">Moderate</option><option value="active">Active</option><option value="very_active">Very active</option></select></label>

            <button onClick={saveProfile} disabled={saving} className="mt-5 w-full rounded-xl bg-amber-400 px-4 py-3 font-bold text-black disabled:opacity-60">{saving ? "Saving..." : "Save profile"}</button>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 lg:col-span-2">
            <h2 className="text-xl font-semibold">Daily targets</h2>
            {!nutrition ? (
              <div className="mt-8 rounded-2xl bg-black/20 p-6 text-slate-400">Save your profile to calculate your targets.</div>
            ) : (
              <>
                <div className="mt-5 grid grid-cols-2 gap-4 md:grid-cols-4">
                  {[
                    ["Calories", `${nutrition.calorie_target} kcal`],
                    ["Protein", `${nutrition.protein_g} g`],
                    ["Carbs", `${nutrition.carbs_g} g`],
                    ["Fat", `${nutrition.fat_g} g`],
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-2xl bg-black/25 p-5">
                      <div className="text-sm text-slate-500">{label}</div>
                      <div className="mt-2 text-2xl font-bold">{value}</div>
                    </div>
                  ))}
                </div>
                <div className="mt-5 grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 p-5"><span className="text-slate-500">BMR</span><div className="mt-1 text-2xl font-bold">{nutrition.bmr} kcal</div></div>
                  <div className="rounded-2xl border border-white/10 p-5"><span className="text-slate-500">TDEE</span><div className="mt-1 text-2xl font-bold">{nutrition.tdee} kcal</div></div>
                </div>
                <p className="mt-5 text-sm leading-6 text-slate-500">{nutrition.explanation}</p>
              </>
            )}
          </div>
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-6">
            <h2 className="text-xl font-semibold">Log food</h2>
            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              <select value={selectedFood} onChange={(e) => setSelectedFood(e.target.value)} className="rounded-xl border border-white/10 bg-black/20 p-3 sm:col-span-2">
                <option value="">Select a food</option>
                {foods.map((food) => <option key={food.id} value={food.id}>{food.name} · {food.calories} kcal/100g</option>)}
              </select>
              <input value={servings} onChange={(e) => setServings(e.target.value)} type="number" min="0.25" step="0.25" className="rounded-xl border border-white/10 bg-black/20 p-3" />
            </div>
            <div className="mt-3 flex gap-3">
              <select value={meal} onChange={(e) => setMeal(e.target.value)} className="flex-1 rounded-xl border border-white/10 bg-black/20 p-3">
                <option>breakfast</option><option>lunch</option><option>snack</option><option>dinner</option>
              </select>
              <button onClick={logFood} className="rounded-xl bg-white px-5 font-semibold text-black">Log</button>
            </div>
            <div className="mt-5 grid grid-cols-4 gap-2 text-center">
              <div className="rounded-xl bg-black/20 p-3"><div className="text-xs text-slate-500">Calories</div><div className="font-semibold">{Math.round(totals.calories)}</div></div>
              <div className="rounded-xl bg-black/20 p-3"><div className="text-xs text-slate-500">Protein</div><div className="font-semibold">{Math.round(totals.protein)}g</div></div>
              <div className="rounded-xl bg-black/20 p-3"><div className="text-xs text-slate-500">Carbs</div><div className="font-semibold">{Math.round(totals.carbs)}g</div></div>
              <div className="rounded-xl bg-black/20 p-3"><div className="text-xs text-slate-500">Fat</div><div className="font-semibold">{Math.round(totals.fat)}g</div></div>
            </div>
            <div className="mt-5 space-y-2">
              {intake.slice(0, 6).map((item) => <div key={item.id} className="flex justify-between rounded-xl border border-white/5 px-3 py-2 text-sm"><span>{item.food_name} × {item.servings}</span><span className="text-slate-400">{Math.round(item.calories)} kcal</span></div>)}
              {!intake.length && <div className="text-sm text-slate-500">No food logged yet.</div>}
            </div>
          </div>

          <div className="rounded-3xl border border-amber-400/20 bg-amber-400/[0.06] p-6">
            <h2 className="text-xl font-semibold">AI Coach</h2>
            <p className="mt-1 text-sm text-slate-400">Ask for a practical next-meal recommendation based on your profile and logged intake.</p>
            <button onClick={getRecommendation} disabled={aiBusy || !nutrition} className="mt-5 rounded-xl bg-amber-400 px-5 py-3 font-bold text-black disabled:opacity-50">{aiBusy ? "Thinking..." : `Recommend ${meal}`}</button>
            {aiText && <div className="mt-5 rounded-2xl bg-black/25 p-5"><div className="mb-2 text-xs uppercase tracking-wider text-amber-300">{aiSource === "ai" ? "AI generated" : "Fallback recommendation"}</div><p className="whitespace-pre-wrap leading-7 text-slate-200">{aiText}</p></div>}
          </div>
        </section>
      </div>
    </main>
  );
}
