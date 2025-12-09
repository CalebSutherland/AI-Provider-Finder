import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import ProviderTable from "../components/ProviderTable";
import styles from "./Home.module.css";

import { fetchSearchResults } from "../api/providers";
import SearchInput from "../components/SearchInput";

export default function Home() {
  const [userQuery, setUserQuery] = useState("");

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["providerSearch"],
    queryFn: () => fetchSearchResults(userQuery),
    enabled: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    refetch();
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
              userQuery={userQuery}
              setUserQuery={setUserQuery}
              handleSubmit={handleSubmit}
            />
          </div>
        </div>
      </section>

      <main className={styles.main}>
        <div className={styles.main_container}>
          {isLoading && <p>Loading providers...</p>}
          {error && <p>Error fetching providers</p>}
          {!isLoading && !error && data && (
            <ProviderTable providerSearch={data} />
          )}
        </div>
      </main>

      <footer>
        <div>
          <p>Helping you find the right healthcare, one search at a time.</p>
        </div>
      </footer>
    </div>
  );
}
