import Paper from "@mui/material/Paper";
import InputBase from "@mui/material/InputBase";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";

import styles from "./SearchInput.module.css";

interface SearchInputProps {
  userQuery: string;
  placeholder: string;
  setUserQuery: React.Dispatch<React.SetStateAction<string>>;
  handleSubmit: (e: React.FormEvent) => void;
}
export default function SearchInput({
  userQuery,
  placeholder,
  setUserQuery,
  handleSubmit,
}: SearchInputProps) {
  return (
    <div className={styles.search}>
      <Paper
        component="form"
        onSubmit={handleSubmit}
        sx={{ p: "2px 4px", display: "flex", alignItems: "center" }}
      >
        <SearchIcon color="action" sx={{ fontSize: 30, ml: 1 }} />
        <InputBase
          fullWidth
          value={userQuery}
          onChange={(e) => setUserQuery(e.target.value)}
          placeholder={placeholder}
          sx={{ height: "3.5rem", ml: 1, flex: 1 }}
        />
        <Button
          variant="contained"
          type="submit"
          disabled={userQuery == ""}
          sx={{ mr: 1 }}
        >
          Search
        </Button>
      </Paper>
    </div>
  );
}
