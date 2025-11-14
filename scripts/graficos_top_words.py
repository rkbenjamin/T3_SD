import os
import matplotlib.pyplot as plt
import pandas as pd

YAHOO_PATH = "results/yahoo_wordcount/part-r-00000"
LLM_PATH = "results/llm_wordcount/part-r-00000"
FIGS_DIR = "figs"

os.makedirs(FIGS_DIR, exist_ok=True)


def load_wordcount(path):
    words = []
    freqs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            word = parts[0]
            try:
                freq = int(parts[1])
            except ValueError:
                continue
            words.append(word)
            freqs.append(freq)

    df = pd.DataFrame({"word": words, "freq": freqs})
    df = df.sort_values("freq", ascending=False).reset_index(drop=True)
    return df


def plot_top10(df, title, out_path):

    top10 = df.head(10)

    plt.figure()
    plt.bar(top10["word"], top10["freq"])
    plt.title(title)
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Gráfico guardado en: {out_path}")


def print_markdown_top50(df, titulo):
    top50 = df.head(50)
    print(f"\n## {titulo}")
    print("| Rank | Word | Frequency |")
    print("|------|------|-----------|")
    for i, row in top50.iterrows():
        print(f"| {i+1} | {row['word']} | {row['freq']} |")


def main():
    yahoo_df = load_wordcount(YAHOO_PATH)
    llm_df = load_wordcount(LLM_PATH)

    plot_top10(yahoo_df, "Top 10 words - Yahoo", os.path.join(FIGS_DIR, "yahoo_top10.png"))
    plot_top10(llm_df, "Top 10 words - LLM", os.path.join(FIGS_DIR, "llm_top10.png"))

    print_markdown_top50(yahoo_df, "Top 50 words - Yahoo")
    print_markdown_top50(llm_df, "Top 50 words - LLM")


if __name__ == "__main__":
    main()