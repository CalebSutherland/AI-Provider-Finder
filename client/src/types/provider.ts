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

export interface ProviderSearchResponse {
  success: boolean;
  parsed_params: SearchParams;
  results: Provider[]
  hcpcs_desc?: string;
  count?: number;
  error?: string;
}

export interface ScoredProvider extends Provider {
  score: number
  rank: number
}

export interface ProviderScoreRequest {
  query: string;
  provider_ids: number[]
}

export interface ProviderScoreResponse {
  success: boolean;
  parsed_params: SearchParams;
  results: ScoredProvider[]
  error?: string;
}
