import Dashboard from "@/components/dashboard";
import { getLabs } from "@/lib/api";

export default async function Home() {
  try {
    const labs = await getLabs();

    return <Dashboard initialLabs={labs} />;
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "The application could not start.";

    return (
      <main className="grid min-h-screen place-items-center px-6">
        <div className="max-w-lg rounded-2xl border border-rose-400/30 bg-panel p-8">
          <p className="font-mono text-xs uppercase tracking-[0.25em] text-rose-300">
            Backend unavailable
          </p>

          <h1 className="mt-4 text-3xl font-semibold">
            The dashboard needs its services.
          </h1>

          <p className="mt-4 leading-7 text-slate-400">{message}</p>

          <p className="mt-5 text-sm text-slate-500">
            Start catalog on 8001, progress on 8002, and the gateway on 8000,
            then refresh this page.
          </p>
        </div>
      </main>
    );
  }
}
