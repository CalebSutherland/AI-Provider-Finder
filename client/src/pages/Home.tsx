import styles from "./Home.module.css";
import TextField from "@mui/material/TextField";

export default function Home() {
  return (
    <div className={styles.home}>
      <header className={styles.header}>
        <span>Logo</span>
        <span>AI Provider Finder</span>
      </header>

      <section className={styles.hero}>
        <div className={styles.heroContainer}>
          <h1>
            Find your <span>Perfect Doctor</span>
          </h1>
          <p>
            Describe what you need in your own words. Our AI-powered search
            helps you find the best healthcare providers nearby.
          </p>
          <div>
            <TextField fullWidth />
            <p>Describe what you're looking for in plain language</p>
          </div>
        </div>
      </section>

      <main>
        <div>
          <p>Doctor List goes here</p>
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
