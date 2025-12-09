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
  city: string;
  state: string;
  zipcode: string | null;
  specialty: string;
  hcpcs_prefix: string;
  confidence: string;
}

export interface ProviderSearch {
  success: boolean;
  parsed_params: SearchParams;
  results: Provider[]
  count: number
  error?: string
}