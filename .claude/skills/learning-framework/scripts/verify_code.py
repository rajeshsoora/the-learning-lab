"""
Plain-Python verifier for module code-walkthrough trace tables.

Scope (see references/code-fluency.md and SKILL.md Stage 7's code-fluency
check): this mirrors the *logic* of a module's PySpark code against a toy
dataset, in plain Python, so trace-table values shown in a Predict-then-reveal
step are independently checked rather than hand-computed. It does NOT execute
real PySpark (no JVM/Spark dependency) — it only verifies that the numbers
claimed in a walkthrough are arithmetically correct for the toy data used.

Run directly: python3 verify_code.py
"""

TOY_PAIRS = [
    # pair_id, composite, human_label
    ("P1", 0.95, "true_match"),
    ("P2", 0.88, "true_match"),
    ("P3", 0.82, "false_match"),
    ("P4", 0.70, "true_match"),
    ("P5", 0.58, "false_match"),
    ("P6", 0.45, "true_match"),
    ("P7", 0.30, "false_match"),
    ("P8", 0.15, "false_match"),
]

MATCH_THRESHOLD = 0.80
REVIEW_THRESHOLD = 0.50


def confusion_matrix(pairs, match_threshold):
    rows = []
    tp = fp = fn = tn = 0
    for pid, composite, label in pairs:
        is_match = label == "true_match"
        predicted = composite >= match_threshold
        if predicted and is_match:
            tp += 1
            cell = "TP"
        elif predicted and not is_match:
            fp += 1
            cell = "FP"
        elif not predicted and is_match:
            fn += 1
            cell = "FN"
        else:
            tn += 1
            cell = "TN"
        rows.append((pid, composite, label, is_match, predicted, cell))
    return rows, {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def pr_at(pairs, match_threshold):
    _, cm = confusion_matrix(pairs, match_threshold)
    tp, fp, fn = cm["tp"], cm["fp"], cm["fn"]
    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return {"threshold": match_threshold, "precision": precision, "recall": recall, **cm}


def calibration_table(pairs, bins=10):
    buckets = {}
    for pid, composite, label in pairs:
        bin_key = int(composite * bins) / bins
        total, matches = buckets.get(bin_key, (0, 0))
        buckets[bin_key] = (total + 1, matches + (1 if label == "true_match" else 0))
    rows = []
    for bin_key in sorted(buckets):
        total, matches = buckets[bin_key]
        rows.append((bin_key, total, matches, matches / total))
    return rows


def queue_size(pairs, match_t, review_t):
    auto_merge = review = auto_reject = 0
    for pid, composite, label in pairs:
        if composite >= match_t:
            auto_merge += 1
        elif composite >= review_t:
            review += 1
        else:
            auto_reject += 1
    return {"auto_merge": auto_merge, "review": review, "auto_reject": auto_reject}


if __name__ == "__main__":
    rows, cm = confusion_matrix(TOY_PAIRS, MATCH_THRESHOLD)
    print(f"confusion_matrix(match_threshold={MATCH_THRESHOLD}):")
    for pid, composite, label, is_match, predicted, cell in rows:
        print(f"  {pid}  composite={composite:.2f}  label={label:12s}  is_match={is_match!s:5}  predicted={predicted!s:5}  -> {cell}")
    print(f"  totals: {cm}")
    assert cm == {"tp": 2, "fp": 1, "fn": 2, "tn": 3}, "confusion_matrix mismatch"

    pr = pr_at(TOY_PAIRS, MATCH_THRESHOLD)
    print(f"\npr_at(match_threshold={MATCH_THRESHOLD}): {pr}")
    assert abs(pr["precision"] - 2 / 3) < 1e-9
    assert abs(pr["recall"] - 0.5) < 1e-9

    print("\ncalibration_table(bins=10):")
    for bin_key, total, matches, rate in calibration_table(TOY_PAIRS):
        print(f"  bin={bin_key:.1f}  total={total}  matches={matches}  match_rate={rate:.2f}")

    q = queue_size(TOY_PAIRS, MATCH_THRESHOLD, REVIEW_THRESHOLD)
    print(f"\nqueue_size(match_t={MATCH_THRESHOLD}, review_t={REVIEW_THRESHOLD}): {q}")
    assert q == {"auto_merge": 3, "review": 2, "auto_reject": 3}, "queue_size mismatch"

    print("\nAll trace values verified.")
