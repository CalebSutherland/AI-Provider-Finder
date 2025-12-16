export interface Provider {
  id: number;
  last_name: string;
  first_name: string | null;
  credentials: string | null;
  street_1: string;
  street_2: string | null;
  city: string;
  state: string;
  zipcode: string;
  specialty: string;
  accepts_medicare: string;
  total_benes: number;
  avg_age: number;
}

export interface SearchParams {
  specialty: string;
  zipcode: string | null;
  state: string | null;
  city: string | null;
  hcpcs_prefix: string | null;
  hcpcs_description: string | null;
  confidence: string;
}

export interface SearchResult {
  result: Provider[]
  count: number
}