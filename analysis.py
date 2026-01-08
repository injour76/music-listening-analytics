# analysis.py
# Music Listening Analytics

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path


# CONFIG

PROJECT_DIR = Path(__file__).parent
CSV_PATH = PROJECT_DIR / "music.csv"
DB_PATH = PROJECT_DIR / "music_log.db"
OUTPUTS_DIR = PROJECT_DIR / "outputs"

EXCEL_OUT = OUTPUTS_DIR / "workout_summary.xlsx"
PIE_OUT = OUTPUTS_DIR / "minutes_by_genre_pie.png"

SHOW_CHARTS = True


# ---------------------------
# FUNCTIONS
# ---------------------------
def load_data(csv_path):
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find {csv_path}")

    df = pd.read_csv(csv_path)

    # normalize columns
    df.columns = df.columns.str.strip().str.lower()

    # clean text fields
    for col in ["artist", "track", "genre", "activity", "date"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "activity" in df.columns:
        df["activity"] = df["activity"].str.lower()

    return df


def summarize(df):
    print("Data shape:", df.shape)
    print("\nMissing values:\n", df.isna().sum())
    print("\nSample rows:\n", df.head())

    minutes_by_activity = (
        df.groupby("activity")["minutes"]
        .sum()
        .sort_values(ascending=False)
    )

    return minutes_by_activity


def export_outputs(df, minutes_by_activity):
    OUTPUTS_DIR.mkdir(exist_ok=True)

    # workout summary
    workout_df = df[df["activity"] == "workout"]
    workout_sorted = workout_df.sort_values("minutes", ascending=False)
    workout_sorted.to_excel(EXCEL_OUT, index=False)

    # bar chart
    plt.figure()
    minutes_by_activity.plot(kind="bar")
    plt.title("Total Minutes by Activity")
    plt.xlabel("Activity")
    plt.ylabel("Minutes")
    plt.tight_layout()

    if SHOW_CHARTS:
        plt.show()
    else:
        plt.close()

    # pie chart by genre
    genre_minutes = (
        df.groupby("genre")["minutes"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(6, 6))
    genre_minutes.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Minutes by Genre")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(PIE_OUT)

    if SHOW_CHARTS:
        plt.show()
    else:
        plt.close()


def save_to_sqlite(df, db_path):
    conn = sqlite3.connect(db_path)
    df.to_sql("music", conn, if_exists="replace", index=False)

    query = """
    SELECT activity, SUM(minutes) AS total_minutes
    FROM music
    GROUP BY activity
    ORDER BY total_minutes DESC;
    """

    result = pd.read_sql(query, conn)
    print("\nSQL Results:\n", result)

    conn.close()


def main():
    df = load_data(CSV_PATH)
    minutes_by_activity = summarize(df)
    export_outputs(df, minutes_by_activity)
    save_to_sqlite(df, DB_PATH)
    print("\nAnalysis complete. Outputs saved to /outputs")



# ENTRY POINT
if __name__ == "__main__":
    main()
