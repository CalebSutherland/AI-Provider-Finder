import { useState } from "react";

import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import SearchInput from "./SearchInput";

interface ScoreDialogProps {
  userQuery: string;
  setUserQuery: React.Dispatch<React.SetStateAction<string>>;
  handleSubmit: (e: React.FormEvent) => void;
}
export default function ScoreDialog({
  userQuery,
  setUserQuery,
  handleSubmit,
}: ScoreDialogProps) {
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleDialogSubmit = (e: React.FormEvent) => {
    handleSubmit(e);
    handleClose();
  };

  return (
    <>
      <Button
        variant="contained"
        size="large"
        sx={{ fontSize: "1.2rem" }}
        onClick={handleClickOpen}
      >
        Rank Providers
      </Button>
      <Dialog fullWidth maxWidth="md" open={open} onClose={handleClose}>
        <DialogTitle>Find the match for you</DialogTitle>
        <DialogContent>
          <DialogContentText mb={"1rem"}>
            To find a provider that best fits you, enter at least one of the
            following: age, race, or sex.
          </DialogContentText>
          <SearchInput
            userQuery={userQuery}
            placeholder="Ex: 23 year old white male; I am a black women aged 64;"
            setUserQuery={setUserQuery}
            handleSubmit={handleDialogSubmit}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
