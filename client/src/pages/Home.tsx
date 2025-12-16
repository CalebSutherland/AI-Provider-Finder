import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import SearchInput from "../components/SearchInput";
import SearchTips from "../components/SearchTips";
import ProviderTable from "../components/ProviderTable";
import styles from "./Home.module.css";
import PersonSearchIcon from "@mui/icons-material/PersonSearch";

import { fetchSearchResults, parseSearchInput } from "../api/search";
import type { SearchParams } from "../types/search";

export default function Home() {
  const [isNewSearch, setIsNewSearch] = useState(false);
  const [searchParams, setSearchParams] = useState<SearchParams | null>(null);
  const [paginationModel, setPaginationModel] = useState({
    pageSize: 10,
    page: 0,
  });

  const searchMutation = useMutation({
    mutationFn: parseSearchInput,
    onSuccess: (data) => {
      setSearchParams(data);
      setPaginationModel({ pageSize: 10, page: 0 });
      setIsNewSearch(true);
    },
    onError: (error: Error) => {
      console.error("Search parsing failed:", error);
    },
  });

  const searchQuery = useQuery({
    queryKey: [
      "searchResults",
      searchParams,
      paginationModel.page,
      paginationModel.pageSize,
    ],
    queryFn: () =>
      fetchSearchResults(
        searchParams!,
        paginationModel.page + 1,
        paginationModel.pageSize
      ),
    enabled: !!searchParams,
    placeholderData: (previousData) => previousData,
  });

  if (isNewSearch && searchQuery.data && !searchQuery.isFetching) {
    setIsNewSearch(false);
  }

  const handleSearch = (input: string) => {
    setSearchParams(null);
    searchMutation.mutate(input);
  };

  let location: string = "";
  let tableMessage: React.ReactNode = null;

  if (searchParams?.zipcode) {
    location = `${searchParams.city}, ${searchParams.state}, ${searchParams.zipcode}`;
  } else if (searchParams?.city) {
    location = `${searchParams.city}, ${searchParams.state}`;
  } else if (searchParams?.state) {
    location = searchParams.state;
  }

  if (searchMutation.isPending) {
    tableMessage = <p>Parsing user input...</p>;
  } else if (isNewSearch || (searchQuery.isFetching && !searchQuery.data)) {
    tableMessage = <p>Loading providers...</p>;
  } else if (searchParams && searchQuery.data) {
    tableMessage = (
      <p>
        Found{" "}
        <b>
          {searchQuery.data?.count} {searchParams?.specialty}
        </b>{" "}
        providers in <b>{location} </b>
        {searchParams?.hcpcs_description && (
          <>
            with services related to <b>{searchParams.hcpcs_description}</b>
          </>
        )}
      </p>
    );
  }

  return (
    <div className={styles.home}>
      <header className={styles.header}>
        <div>
          <PersonSearchIcon color="primary" sx={{ fontSize: 40 }} />
          <span>Provider Finder AI</span>
        </div>
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
              placeholder="Ex: I need a cardiologist who can do an ultrasound near downtown Chicago"
              handleSubmit={handleSearch}
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
          {searchMutation.error && (
            <p>
              Error parsing input: <b>{searchMutation.error.message}</b>
            </p>
          )}
          {searchQuery.error && (
            <p>
              Error searching for providers: <b>{searchQuery.error.message}</b>
            </p>
          )}

          {searchParams && !searchParams.hcpcs_prefix && (
            <p>Warning: No provider service detected</p>
          )}

          {!searchMutation.isIdle && (
            <div>
              {tableMessage}
              <ProviderTable
                data={searchQuery.data}
                isLoading={
                  searchMutation.isPending ||
                  (searchQuery.isFetching && !searchQuery.isFetched)
                }
                paginationModel={paginationModel}
                setPaginationModel={setPaginationModel}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
