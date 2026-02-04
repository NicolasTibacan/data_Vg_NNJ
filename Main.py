from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from Extract.extract_data import extract_vgsales
from Load.load_data import load_to_sqlite
from config.database import get_engine
from transform.transform_data import clean_vgsales


def plot_genre_sales(df, output_dir: Path) -> Path:
	genre_sales = (
		df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
	)

	plt.figure(figsize=(10, 6))
	sns.barplot(x=genre_sales.values, y=genre_sales.index, palette="viridis")
	plt.title("Global Sales by Genre")
	plt.xlabel("Global Sales (Millions)")
	plt.ylabel("Genre")

	output_path = output_dir / "genre_sales_comparison.png"
	plt.tight_layout()
	plt.savefig(output_path, dpi=150)
	plt.close()

	return output_path


def plot_top_genre_trend(df, output_dir: Path) -> tuple[str, Path]:
	top_genre = df.groupby("Genre")["Global_Sales"].sum().idxmax()
	trend = (
		df[df["Genre"] == top_genre]
		.groupby("Year")["Global_Sales"]
		.sum()
		.reset_index()
		.sort_values("Year")
	)

	plt.figure(figsize=(10, 5))
	sns.lineplot(data=trend, x="Year", y="Global_Sales", marker="o")
	plt.title(f"Global Sales Trend for Top Genre: {top_genre}")
	plt.xlabel("Year")
	plt.ylabel("Global Sales (Millions)")

	output_path = output_dir / "top_genre_trend.png"
	plt.tight_layout()
	plt.savefig(output_path, dpi=150)
	plt.close()

	return top_genre, output_path


def plot_all_genres_trend(df, output_dir: Path) -> Path:
	trend = (
		df.groupby(["Year", "Genre"])["Global_Sales"]
		.sum()
		.reset_index()
		.sort_values("Year")
	)

	plt.figure(figsize=(12, 6))
	sns.lineplot(data=trend, x="Year", y="Global_Sales", hue="Genre")
	plt.title("Global Sales by Genre Over Time")
	plt.xlabel("Year")
	plt.ylabel("Global Sales (Millions)")
	plt.legend(title="Genre", bbox_to_anchor=(1.02, 1), loc="upper left")

	output_path = output_dir / "genre_trends_over_time.png"
	plt.tight_layout()
	plt.savefig(output_path, dpi=150)
	plt.close()

	return output_path


def main() -> None:
	df = extract_vgsales()
	cleaned = clean_vgsales(df)

	engine = get_engine()
	load_to_sqlite(cleaned, engine)

	output_dir = Path("reports")
	output_dir.mkdir(parents=True, exist_ok=True)

	genre_plot = plot_genre_sales(cleaned, output_dir)
	top_genre, trend_plot = plot_top_genre_trend(cleaned, output_dir)
	all_genres_plot = plot_all_genres_trend(cleaned, output_dir)

	print(f"Loaded {len(cleaned)} rows into SQLite.")
	print(f"Genre comparison plot: {genre_plot}")
	print(f"Top genre: {top_genre}")
	print(f"Top genre trend plot: {trend_plot}")
	print(f"All genres trend plot: {all_genres_plot}")


if __name__ == "__main__":
	main()
