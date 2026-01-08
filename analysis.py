# analysis.py
# Music Listening Project

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path


# CONFIG 
# ---------------------------
PROJECT_DIR = Path(__file__).parent
CSV_PATH = PROJECT_DIR / "music.csv"
DB_PATH = PROJECT_DIR / "music_log.db"
EXCEL_OUT = PROJECT_DIR / "workout_summary.xlsx"
PIE_OUT = PROJECT_DIR / "minutes_by_genre_pie.png"


EXPORT_EXCEL = True           
SHOW_CHARTS = True           
SAVE_PIE_IMAGE = True         
APPEND_NEW_SONG = False       


#  LOAD CSV
if not CSV_PATH.exists():
    raise FileNotFoundError(f"Could not find {CSV_PATH}. Make sure music.csv is in the same folder as analysis.py")

df = pd.read_csv(CSV_PATH)


df.columns = df.columns.str.strip().str.lower()


for col in ["artist", "track", "genre", "activity", "date"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()


if "activity" in df.columns:
    df["activity"] = df["activity"].str.lower()

print("=== FULL DATA ===")
print(df)

print("\n=== FIRST LOOK (head) ===")
print(df.head())

print("\n=== INFO ===")
print(df.info())

# INSIGHTS
# ---------------------------
print("\n=== TOTAL MINUTES ===")
total_minutes = df["minutes"].sum()
print(total_minutes)

print("\n=== MINUTES BY ACTIVITY (pandas) ===")
minutes_by_activity = df.groupby("activity")["minutes"].sum().sort_values(ascending=False)
print(minutes_by_activity)

# Workout filter + sort
print("\n=== WORKOUT ROWS ONLY ===")
workout_df = df[df["activity"] == "workout"]
print(workout_df)

print("\n=== WORKOUT SORTED (DESC) ===")
workout_sorted = workout_df.sort_values(by="minutes", ascending=False)
print(workout_sorted)


# EXPORT TO EXCEL 
if EXPORT_EXCEL:
    try:
        workout_sorted.to_excel(EXCEL_OUT, index=False)
        print(f"\ Exported workout summary to: {EXCEL_OUT}")
    except ModuleNotFoundError:
        print("\n Excel export failed: openpyxl not installed.")
        print("Run this in PowerShell/CMD:  pip install openpyxl")


# CHARTS
# Bar chart: minutes by activity
if SHOW_CHARTS:
    plt.figure()
    minutes_by_activity.plot(kind="bar")
    plt.title("Total Minutes by Activity")
    plt.xlabel("Activity")
    plt.ylabel("Minutes")
    plt.tight_layout()
    plt.show()

# Pie chart: minutes by genre 
genre_minutes = df.groupby("genre")["minutes"].sum().sort_values(ascending=False)

#  figure 
plt.figure(figsize=(6, 6))
genre_minutes.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Minutes by Genre")
plt.ylabel("")
plt.tight_layout()

if SAVE_PIE_IMAGE:
    plt.savefig(PIE_OUT)
    print(f"\n✅ Saved pie chart image to: {PIE_OUT}")

if SHOW_CHARTS:
    
    plt.show()
else:
    plt.close()


 # SQLITE (SQL) SAVE + QUERY

print("\n=== SQL: SAVING TO SQLITE ===")
conn = sqlite3.connect(DB_PATH)

df.to_sql("music", conn, if_exists="replace", index=False)

sql_query = """
SELECT activity, SUM(minutes) AS total_minutes
FROM music
GROUP BY activity
ORDER BY total_minutes DESC;
"""

result = pd.read_sql(sql_query, conn)
print("\n=== SQL RESULTS: TOTAL MINUTES BY ACTIVITY ===")
print(result)



if APPEND_NEW_SONG:
    new_song = {
        "date": "12/11/2024",
        "artist": "Frank Ocean",
        "track": "Nights",
        "genre": "R&B",
        "minutes": 4,
        "activity": "Relaxing",
    }

    
    df_updated = pd.concat([df, pd.DataFrame([new_song])], ignore_index=True)

  
    df_updated.to_csv(CSV_PATH, index=False)
    print("\nAdded new song and updated music.csv")
    print(df_updated.tail())

    
    pd.DataFrame([new_song]).to_sql("music", conn, if_exists="append", index=False)
    print(" Appended new song to SQLite table 'music'")

conn.close()
print(f"\n SQLite DB saved at: {DB_PATH}")
