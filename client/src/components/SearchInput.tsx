import { useState } from "react";

import Paper from "@mui/material/Paper";
import InputBase from "@mui/material/InputBase";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";

import styles from "./SearchInput.module.css";

interface SearchInputProps {
  placeholder: string;
  handleSubmit: (input: string) => void;
}
export default function SearchInput({
  placeholder,
  handleSubmit,
}: SearchInputProps) {
  const [searchInput, setSearchInput] = useState("");

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSubmit(searchInput);
  };

  return (
    <div className={styles.search}>
      <Paper
        component="form"
        onSubmit={onSubmit}
        sx={{ p: "2px 4px", display: "flex", alignItems: "center" }}
      >
        <SearchIcon color="action" sx={{ fontSize: 30, ml: 1 }} />
        <InputBase
          fullWidth
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder={placeholder}
          sx={{ height: "3.5rem", ml: 1, flex: 1 }}
        />
        <Button
          variant="contained"
          type="submit"
          disabled={searchInput == ""}
          sx={{ mr: 1 }}
        >
          Search
        </Button>
      </Paper>
    </div>
  );
}
