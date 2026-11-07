"""Reproduce baseline and alternative outputs with one command."""

import argparse
import csv
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .model import NotificationModel


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def process_trace(raw_path, condition, output_dir):
    # Derive every processed result from the saved raw file, not parallel logic.
    with raw_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    arrivals = [int(r["arrival_minute"]) for r in rows]
    presentations = [int(r["presentation_minute"]) for r in rows]
    delays = [int(r["presentation_delay_minutes"]) for r in rows]
    summary = {
        "condition": condition,
        "notification_count": len(rows),
        "alert_episodes": len(set(presentations)),
        "mean_presentation_delay_minutes": mean(delays),
        "max_presentation_delay_minutes": max(delays),
    }
    write_csv(output_dir / f"{condition}_processed_00_summary.csv", [summary])
    fig, ax = plt.subplots(figsize=(10, 5.8), layout="constrained")
    y = list(range(len(rows)))
    ax.hlines(y, arrivals, presentations, color="#527fa7", linewidth=3)
    ax.scatter(arrivals, y, color="#596271", marker="o", s=40, label="Arrival", zorder=3)
    ax.scatter(presentations, y, color="#007b82", marker="|", s=260,
               linewidths=2.5, label="Presentation", zorder=4)
    ax.set_yticks(y, [r["notification_id"] for r in rows])
    ax.invert_yaxis()
    ax.set_xticks(range(0, 61, 10))
    ax.set_xlim(0, 61)
    ax.set_xlabel("Minute in the synthetic 60-minute session")
    ax.set_ylabel("Notification agent")
    mode = "Immediate delivery" if condition == "baseline" else "Fixed 10-minute batching"
    ax.set_title(f"{condition.capitalize()}: {mode}\n"
                 f"{summary['alert_episodes']} alert episodes | "
                 f"Mean delay {mean(delays):.2f} min | Maximum delay {max(delays)} min",
                 loc="left", pad=15, fontsize=13)
    ax.grid(axis="x", alpha=.22)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper right", frameon=True)
    fig.savefig(output_dir / f"{condition}_processed_01_presentation_timeline.png", dpi=160)
    plt.close(fig)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for condition, mode in (("baseline", "immediate"), ("alternative", "batch")):
        model = NotificationModel(delivery_mode=mode).run()
        raw_path = args.output_dir / f"{condition}_raw_00_notification_trace.csv"
        write_csv(raw_path, model.notification_trace())
        model.datacollector.get_model_vars_dataframe().to_csv(
            args.output_dir / f"{condition}_raw_01_state_by_minute.csv", index=False)
        print(process_trace(raw_path, condition, args.output_dir))


if __name__ == "__main__":
    main()
