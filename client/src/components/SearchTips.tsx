import AddTaskIcon from "@mui/icons-material/AddTask";
import styles from "./SearchTips.module.css";

export default function SearchTips() {
  const tips = [
    "Use a zipcode to narrow down results in your location",
    "Include either doctor type or service needed in prompt",
    "Specify state if searching for a smaller city",
  ];

  return (
    <div className={styles.tips}>
      {tips.map((tip) => (
        <span key={tip} className={styles.row}>
          <AddTaskIcon fontSize="large" color="primary" />
          <p>{tip}</p>
        </span>
      ))}
    </div>
  );
}
