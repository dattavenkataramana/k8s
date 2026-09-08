"use client";

import { useMemo, useState } from "react";

import { ArrowIcon, CheckIcon, ClockIcon, LayersIcon } from "./icons";
import { Lab, setLabProgress } from "@/lib/api";

const difficultyStyle = {
  Beginner: "border-emerald-400/30 bg-emerald-400/10 text-emerald-300",
  Intermediate: "border-amber-400/30 bg-amber-400/10 text-amber-300",
  Advanced: "border-rose-400/30 bg-rose-400/10 text-rose-300",
};

export default function Dashboard({ initialLabs }: { initialLabs: Lab[] }) {
  const [labs, setLabs] = useState(initialLabs);
  const [activeCategory, setActiveCategory] = useState("All");
  const [pendingId, setPendingId] = useState<number | null>(null);
  const [error, setError] = useState("");

  const categories = ["All", ...Array.from(new Set(labs.map((lab) => lab.category)))];
  const visibleLabs =
    activeCategory === "All"
      ? labs
      : labs.filter((lab) => lab.category === activeCategory);
  const completed = labs.filter((lab) => lab.completed).length;
  const percent = labs.length ? Math.round((completed / labs.length) * 100) : 0;
  const minutesRemaining = labs
    .filter((lab) => !lab.completed)
    .reduce((total, lab) => total + lab.duration_minutes, 0);
  const nextLab = useMemo(() => labs.find((lab) => !lab.completed), [labs]);

  async function toggleLab(lab: Lab) {
    setPendingId(lab.id);
    setError("");
    try {
      await setLabProgress(lab.id, !lab.completed);
      setLabs((items) =>
        items.map((item) =>
          item.id === lab.id ? { ...item, completed: !item.completed } : item,
        ),
      );
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Something went wrong.");
    } finally {
      setPendingId(null);
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-5 pb-16 pt-7 sm:px-8 lg:px-12">
      <nav className="flex items-center justify-between border-b border-white/10 pb-6">
        <div className="flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded-xl border border-cyan/30 bg-cyan/10 text-cyan">
            <LayersIcon />
          </span>
          <div>
            <p className="font-display text-lg font-semibold tracking-tight">DevOps Hub</p>
            <p className="text-xs text-slate-500">BUILD · SHIP · OBSERVE</p>
          </div>
        </div>
        <div className="hidden items-center gap-2 text-sm text-slate-400 sm:flex">
          <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_#34d399]" />
          Learning environment
        </div>
      </nav>

      <section className="grid gap-8 py-12 lg:grid-cols-[1fr_340px] lg:items-end">
        <div>
          <p className="mb-4 font-mono text-xs uppercase tracking-[0.3em] text-cyan">
            Your deployment journey
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold leading-[1.05] tracking-[-0.04em] sm:text-6xl">
            Turn application code into a{" "}
            <span className="text-cyan">production platform.</span>
          </h1>
          <p className="mt-6 max-w-2xl text-base leading-7 text-slate-400 sm:text-lg">
            Use these labs as your workload. You build the containers, pipeline,
            cluster, security, and observability around it.
          </p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-panel/80 p-6 shadow-glow backdrop-blur">
          <div className="flex items-end justify-between">
            <div>
              <p className="text-sm text-slate-400">Overall progress</p>
              <p className="mt-1 font-display text-4xl font-semibold">{percent}%</p>
            </div>
            <p className="text-sm text-slate-500">{completed}/{labs.length} labs</p>
          </div>
          <div className="mt-5 h-2 overflow-hidden rounded-full bg-white/5">
            <div
              className="h-full rounded-full bg-gradient-to-r from-cyan to-emerald-400 transition-all duration-500"
              style={{ width: `${percent}%` }}
            />
          </div>
          <div className="mt-5 flex justify-between border-t border-white/10 pt-4 text-sm">
            <span className="text-slate-500">Time remaining</span>
            <span className="text-slate-300">{Math.round(minutesRemaining / 60)} hours</span>
          </div>
        </div>
      </section>

      {nextLab && (
        <section className="mb-12 flex flex-col justify-between gap-5 rounded-2xl border border-amber/20 bg-amber/[0.06] p-6 sm:flex-row sm:items-center">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber">Up next</p>
            <h2 className="mt-2 text-xl font-semibold">{nextLab.title}</h2>
            <p className="mt-1 text-sm text-slate-400">{nextLab.description}</p>
          </div>
          <button
            onClick={() => toggleLab(nextLab)}
            disabled={pendingId === nextLab.id}
            className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-amber px-5 py-3 text-sm font-semibold text-ink transition hover:bg-amber/90 disabled:opacity-50"
          >
            Mark complete <ArrowIcon />
          </button>
        </section>
      )}

      <section>
        <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm text-slate-500">Hands-on curriculum</p>
            <h2 className="mt-1 text-3xl font-semibold tracking-tight">Practice labs</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setActiveCategory(category)}
                className={`rounded-lg border px-3 py-2 text-xs transition ${
                  activeCategory === category
                    ? "border-cyan/40 bg-cyan/10 text-cyan"
                    : "border-white/10 text-slate-400 hover:border-white/20 hover:text-white"
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <p className="mt-6 rounded-xl border border-rose-400/30 bg-rose-400/10 p-4 text-sm text-rose-300">
            {error}
          </p>
        )}

        <div className="mt-7 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {visibleLabs.map((lab, index) => (
            <article
              key={lab.id}
              className={`group flex min-h-72 flex-col rounded-2xl border p-6 transition ${
                lab.completed
                  ? "border-cyan/25 bg-cyan/[0.04]"
                  : "border-white/10 bg-panel/60 hover:-translate-y-1 hover:border-white/20"
              }`}
            >
              <div className="flex items-start justify-between">
                <span className="font-mono text-xs text-slate-600">
                  LAB {String(index + 1).padStart(2, "0")}
                </span>
                <span className={`rounded-full border px-2.5 py-1 text-[11px] ${difficultyStyle[lab.difficulty]}`}>
                  {lab.difficulty}
                </span>
              </div>
              <h3 className="mt-6 text-xl font-semibold leading-snug">{lab.title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-400">{lab.description}</p>
              <div className="mt-5 flex flex-wrap gap-2">
                {lab.tools.map((tool) => (
                  <span key={tool} className="rounded-md bg-white/5 px-2 py-1 text-[11px] text-slate-400">
                    {tool}
                  </span>
                ))}
              </div>
              <div className="mt-auto flex items-center justify-between border-t border-white/10 pt-5">
                <span className="flex items-center gap-2 text-xs text-slate-500">
                  <ClockIcon /> {lab.duration_minutes} min
                </span>
                <button
                  onClick={() => toggleLab(lab)}
                  disabled={pendingId === lab.id}
                  className={`flex items-center gap-2 text-xs font-semibold transition disabled:opacity-50 ${
                    lab.completed ? "text-cyan" : "text-slate-300 hover:text-white"
                  }`}
                >
                  {lab.completed ? <><CheckIcon /> Completed</> : "Mark complete"}
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

