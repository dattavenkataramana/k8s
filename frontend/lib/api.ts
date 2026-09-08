export type Difficulty = "Beginner" | "Intermediate" | "Advanced";

export interface Lab {
  id: number;
  title: string;
  description: string;
  category: string;
  difficulty: Difficulty;
  duration_minutes: number;
  tools: string[];
  completed: boolean;
}

// Server-side URL (used by Next.js Server Components)
const SERVER_API_URL =
  process.env.INTERNAL_API_URL ?? "http://api-gateway:8000";

// Browser URL (used by Client Components)
const CLIENT_API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getLabs(): Promise<Lab[]> {
  const response = await fetch(`${SERVER_API_URL}/api/v1/labs`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(
      "Could not load labs. Check that all backend services are running.",
    );
  }

  return response.json();
}

export async function setLabProgress(
  labId: number,
  completed: boolean,
): Promise<void> {
  const response = await fetch(
    `${CLIENT_API_URL}/api/v1/labs/${labId}/progress`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ completed }),
    },
  );

  if (!response.ok) {
    throw new Error("Could not update progress.");
  }
}
