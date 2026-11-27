#!/usr/bin/env python3
"""Turn a work-breakdown CSV into a client-quote CSV with two tracks:
MVP (Must-have only, lean scope) and Production (all features, hardened).
All hours are AI-assisted - there is no no-AI baseline.

Usage: python3 estimate.py work.csv out.csv

work.csv columns:
  [id,]module,feature,moscow,complexity,dev_o,dev_m,dev_p,test_o,test_m,test_p,mvp_scope,notes
  - dev_*/test_* = AI-assisted hours for the PRODUCTION-quality feature (optimistic/likely/pessimistic)
  - moscow = Must|Should|Could|Wont   (MVP includes Must only)
  - mvp_scope = optional free text: what the MVP version of this feature cuts
  - module "_Cross-cutting" rows = project-level items (CI/CD, security...);
    set moscow=Prod to include them in Production only.
"""
import csv, math, sys

# Scope multipliers on PERT hours (input is already AI-assisted, production-quality).
# Tune after comparing estimates vs actuals.
MVP  = dict(dev=0.70, test=0.50, buffer=1.15)  # lean scope, fewer edge cases, happy-path testing
PROD = dict(dev=1.00, test=1.00, buffer=1.30)  # full scope; buffer for revisions/unknowns
# ponytail: flat multipliers; per-complexity multipliers if actuals show a pattern


def pert(o, m, p):
    return (float(o) + 4 * float(m) + float(p)) / 6


def hrs(x):
    return math.ceil(x * 2) / 2  # round up to nearest 0.5h


def row_out(r):
    dev, test = pert(r["dev_o"], r["dev_m"], r["dev_p"]), pert(r["test_o"], r["test_m"], r["test_p"])
    moscow = r["moscow"].strip().capitalize()
    in_mvp = moscow == "Must"
    in_prod = moscow != "Wont"
    mvp_dev = hrs(dev * MVP["dev"] * MVP["buffer"]) if in_mvp else 0
    mvp_test = hrs(test * MVP["test"] * MVP["buffer"]) if in_mvp else 0
    prod_dev = hrs(dev * PROD["dev"] * PROD["buffer"]) if in_prod else 0
    prod_test = hrs(test * PROD["test"] * PROD["buffer"]) if in_prod else 0
    return {
        "ID": r.get("id", ""), "Module": r["module"], "Feature": r["feature"], "Priority": moscow,
        "Complexity": r["complexity"],
        "MVP Dev Hrs": mvp_dev, "MVP Test Hrs": mvp_test, "MVP Total Hrs": mvp_dev + mvp_test,
        "Prod Dev Hrs": prod_dev, "Prod Test Hrs": prod_test, "Prod Total Hrs": prod_dev + prod_test,
        "MVP Scope": r.get("mvp_scope", "") if in_mvp else "Deferred to Production",
        "Notes": r.get("notes", ""),
    }


def main(src, dst):
    with open(src, newline="", encoding="utf-8-sig") as f:
        rows = [row_out(r) for r in csv.DictReader(f) if r.get("feature", "").strip()]
    num = [k for k in rows[0] if k.endswith("Hrs")]
    total = {k: "" for k in rows[0]} | {"Module": "TOTAL"} | {k: sum(r[k] for r in rows) for k in num}
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows); w.writerow(total)
    print(f"{len(rows)} rows -> {dst}")
    print(f"MVP:  {total['MVP Dev Hrs']} dev + {total['MVP Test Hrs']} test = {total['MVP Total Hrs']} h")
    print(f"Prod: {total['Prod Dev Hrs']} dev + {total['Prod Test Hrs']} test = {total['Prod Total Hrs']} h")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
