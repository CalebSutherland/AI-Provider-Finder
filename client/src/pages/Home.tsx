import { useState } from "react";
import { useMutation } from "@tanstack/react-query";

import ProviderTable from "../components/ProviderTable";
import SearchInput from "../components/SearchInput";
import SearchTips from "../components/SearchTips";
import ScoreDialog from "../components/ScoreDialog";
import styles from "./Home.module.css";

import { fetchSearchResults, scoreProviders } from "../api/providers";
import {
  type ProviderScoreRequest,
  type ProviderScoreResponse,
  type ProviderSearchResponse,
} from "../types/provider";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [scoreQuery, setScoreQuery] = useState("");
  const [tableData, setTableData] = useState<
    ProviderSearchResponse | ProviderScoreResponse | null
  >(null);

  const searchMutation = useMutation({
    mutationFn: (req: string) => fetchSearchResults(req),
    onSuccess: (data) => {
      setTableData(data);
    },
  });

  const scoreMutation = useMutation({
    mutationFn: (req: ProviderScoreRequest) => scoreProviders(req),
    onSuccess: (data) => {
      setTableData(data);
    },
  });

  const {
    mutate: searchMutate,
    isPending: isSearchPending,
    error: searchError,
    data: searchData,
  } = searchMutation;

  const {
    mutate: scoreMutate,
    isPending: isScorePending,
    error: scoreError,
  } = scoreMutation;

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    searchMutate(searchQuery);
  };

  const handleScoreSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const provider_ids = searchData ? searchData.results.map((p) => p.id) : [];
    scoreMutate({ query: scoreQuery, provider_ids: provider_ids });
  };

  return (
    <div className={styles.home}>
      <header className={styles.header}>
        <span>Logo</span>
        <span>AI Provider Finder</span>
      </header>

      <section className={styles.hero}>
        <div className={styles.hero_container}>
          <h1>
            Find your <span>Perfect Doctor</span>
          </h1>
          <p className={styles.hero_text}>
            Describe what you need in your own words. Our AI-powered search
            helps you find the best healthcare providers nearby.
          </p>
          <div>
            <SearchInput
              userQuery={searchQuery}
              placeholder="Ex: I need a cardiologist who can do an ultrasound near downtown Chicago"
              setUserQuery={setSearchQuery}
              handleSubmit={handleSearchSubmit}
            />
            <p className={styles.search_footer}>
              Describe what you're looking for in plain language
            </p>
          </div>
        </div>
      </section>

      <section className={styles.tips}>
        <SearchTips />
      </section>

      <main className={styles.main}>
        <div className={styles.main_container}>
          {searchError && <p>Error fetching providers</p>}
          {scoreError && <p>Error scoring providers</p>}

          {(tableData || isSearchPending || isScorePending) && (
            <div>
              <div className={styles.results}>
                {searchData && searchData.success ? (
                  <p>
                    Found <b>{searchData.results.length}</b>{" "}
                    <b>{searchData.parsed_params.specialty}</b> provider
                    {searchData.results.length != 1 ? "s" : ""} in{" "}
                    <b>
                      {searchData.parsed_params.city},{" "}
                      {searchData.parsed_params.state}
                      {searchData.parsed_params.zipcode
                        ? ", " + searchData.parsed_params.zipcode
                        : ""}
                    </b>{" "}
                    with services related to <b>{searchData.hcpcs_desc}</b>{" "}
                  </p>
                ) : (
                  isSearchPending && <p>Searching for providers</p>
                )}
              </div>

              <ProviderTable
                tableData={tableData}
                isLoading={isSearchPending || isScorePending}
              />

              {tableData?.success && (
                <div className={styles.dialog}>
                  <p>Find the best providers for you</p>
                  <ScoreDialog
                    userQuery={scoreQuery}
                    setUserQuery={setScoreQuery}
                    handleSubmit={handleScoreSubmit}
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
