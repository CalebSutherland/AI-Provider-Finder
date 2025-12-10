import AddTaskIcon from "@mui/icons-material/AddTask";
import styles from "./SearchTips.module.css";

export default function SearchTips() {
  const tips = [
    "Include the city and state, or a zipcode.",
    "Mention the provider type and the service you're looking for.",
    "Be specific to narrow results down",
  ];

  return (
    <div className={styles.tips_container}>
      <p className={styles.header}>Tips for the best results</p>
      {tips.map((tip) => (
        <span key={tip} className={styles.row}>
          <AddTaskIcon fontSize="large" color="primary" />
          <p>{tip}</p>
        </span>
      ))}
    </div>
  );
}
