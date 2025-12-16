import type { SearchParams, SearchResult } from "../types/search";

const API_URL: string = import.meta.env.VITE_API_URL;

export async function parseSearchInput(query: string) {
  const res = await fetch(`${API_URL}/api/providers/search/parse`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    const errorData = await res.json()
    console.log(errorData)
    throw new Error(errorData.detail || `Request failed with status ${res.status}`)
  }

  const data: SearchParams = await res.json();
  console.log(data);
  return data;
}


export async function fetchSearchResults(req: SearchParams, page: number=1, page_size: number=10) {
  const res = await fetch(`${API_URL}/api/providers/search/query?page=${page}&page_size=${page_size}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    const errorData = await res.json()
    console.log(errorData)
    throw new Error(errorData.detail || `Request failed with status ${res.status}`)
  }

  const data: SearchResult = await res.json();
  console.log(data);
  return data;
}
