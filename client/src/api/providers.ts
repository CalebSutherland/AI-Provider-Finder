import type { ProviderSearch } from "../types/provider";

const API_URL: string = import.meta.env.VITE_API_URL;

export async function fetchSearchResults(query: string){
  const res = await fetch(`${API_URL}/api/search_providers`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query })
  })

  if (!res.ok) {
    throw new Error("Request failed");
  }

  const data: ProviderSearch = await res.json();
  console.log(data);
  return data
}