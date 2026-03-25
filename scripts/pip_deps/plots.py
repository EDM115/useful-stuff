import json
import os
import matplotlib.pyplot as plt


def load_dependencies(path="output/dependencies.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def plot_requires_distribution(dep_map):
    counts = [len(info.get("requires", [])) for info in dep_map.values()]
    plt.figure()
    plt.hist(counts, bins=range(max(counts) + 2), edgecolor="black")
    plt.title("Distribution of Number of Requires per Package")
    plt.xlabel("Number of Requires")
    plt.ylabel("Number of Packages")
    os.makedirs("output", exist_ok=True)
    plt.savefig("output/requires_distribution.png")
    plt.close()


def plot_required_by_distribution(dep_map):
    counts = [len(info.get("required_by", [])) for info in dep_map.values()]
    plt.figure()
    plt.hist(counts, bins=range(max(counts) + 2), edgecolor="black")
    plt.title("Distribution of Number of Dependents per Package")
    plt.xlabel("Number of Dependents")
    plt.ylabel("Number of Packages")
    plt.savefig("output/required_by_distribution.png")
    plt.close()


def plot_top_dependents(dep_map, top_n=10):
    items = sorted(
        dep_map.items(), key=lambda kv: len(kv[1].get("required_by", [])), reverse=True
    )
    top = items[:top_n]
    names = [pkg for pkg, info in top]
    counts = [len(info.get("required_by", [])) for pkg, info in top]
    plt.figure(figsize=(10, 6))
    plt.barh(names[::-1], counts[::-1], edgecolor="black")
    plt.title(f"Top {top_n} Packages by Number of Dependents")
    plt.xlabel("Number of Dependents")
    plt.tight_layout()
    plt.savefig("output/top_dependents.png")
    plt.close()


def plot_scatter_requires_vs_required_by(dep_map):
    requires = [len(info.get("requires", [])) for info in dep_map.values()]
    required_by = [len(info.get("required_by", [])) for info in dep_map.values()]
    plt.figure()
    plt.scatter(requires, required_by)
    plt.title("Requires vs Required-by for Packages")
    plt.xlabel("Number of Requires")
    plt.ylabel("Number of Dependents")
    plt.grid(True)
    plt.savefig("output/requires_vs_required_by_scatter.png")
    plt.close()


# Additional plots


def plot_pie_top_requires(dep_map, top_n=5):
    items = sorted(
        dep_map.items(), key=lambda kv: len(kv[1].get("requires", [])), reverse=True
    )
    top = items[:top_n]
    labels = [pkg for pkg, _ in top] + ["Others"]
    sizes = [len(info.get("requires", [])) for pkg, info in top] + [
        sum(len(info.get("requires", [])) for pkg, info in items[top_n:])
    ]
    plt.figure()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Top {top_n} Packages by Requires (Pie)")
    plt.axis("equal")
    plt.savefig("output/pie_top_requires.png")
    plt.close()


def plot_pie_top_required_by(dep_map, top_n=5):
    items = sorted(
        dep_map.items(), key=lambda kv: len(kv[1].get("required_by", [])), reverse=True
    )
    top = items[:top_n]
    labels = [pkg for pkg, _ in top] + ["Others"]
    sizes = [len(info.get("required_by", [])) for pkg, info in top] + [
        sum(len(info.get("required_by", [])) for pkg, info in items[top_n:])
    ]
    plt.figure()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Top {top_n} Packages by Dependents (Pie)")
    plt.axis("equal")
    plt.savefig("output/pie_top_required_by.png")
    plt.close()


def plot_pie_zero_requires(dep_map):
    zero = sum(1 for info in dep_map.values() if not info.get("requires"))
    nonzero = len(dep_map) - zero
    plt.figure()
    plt.pie(
        [zero, nonzero],
        labels=["No Requires", "Has Requires"],
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Packages with Zero vs Non-zero Requires")
    plt.axis("equal")
    plt.savefig("output/pie_zero_requires.png")
    plt.close()


def plot_bar_avg_requires_by_bucket(dep_map):
    # average number of requires per bucket of dependents
    buckets = {}
    for info in dep_map.values():
        key = len(info.get("required_by", []))
        buckets.setdefault(key, []).append(len(info.get("requires", [])))
    keys = sorted(buckets.keys())
    avgs = [sum(vals) / len(vals) for vals in (buckets[k] for k in keys)]
    plt.figure(figsize=(10, 6))
    plt.bar(keys, avgs, edgecolor="black")
    plt.title("Average Requires by Number of Dependents")
    plt.xlabel("Number of Dependents")
    plt.ylabel("Average Number of Requires")
    plt.tight_layout()
    plt.savefig("output/bar_avg_requires.png")
    plt.close()


def plot_cumulative_distribution(dep_map):
    counts = sorted(len(info.get("required_by", [])) for info in dep_map.values())
    cumulative = [sum(1 for c in counts if c <= x) for x in counts]
    plt.figure()
    plt.plot(counts, cumulative)
    plt.title("Cumulative Distribution of Dependents")
    plt.xlabel("Number of Dependents")
    plt.ylabel("Cumulative Number of Packages")
    plt.grid(True)
    plt.savefig("output/cumulative_dependents.png")
    plt.close()


def main():
    print("Loading dependency data from output/dependencies.json...")
    dep_map = load_dependencies()
    print(f"Loaded {len(dep_map)} packages\n")

    plot_steps = [
        ("requires_distribution.png", plot_requires_distribution),
        ("required_by_distribution.png", plot_required_by_distribution),
        ("top_dependents.png", plot_top_dependents),
        (
            "requires_vs_required_by_scatter.png",
            plot_scatter_requires_vs_required_by,
        ),
        ("pie_top_requires.png", plot_pie_top_requires),
        ("pie_top_required_by.png", plot_pie_top_required_by),
        ("pie_zero_requires.png", plot_pie_zero_requires),
        ("bar_avg_requires.png", plot_bar_avg_requires_by_bucket),
        ("cumulative_dependents.png", plot_cumulative_distribution),
    ]

    total = len(plot_steps)
    for idx, (filename, plot_fn) in enumerate(plot_steps, start=1):
        print(f"Generating [{idx:02}/{total:02}] {filename}...")
        plot_fn(dep_map)

    print("\nDone. All plots generated in output/")


if __name__ == "__main__":
    main()
