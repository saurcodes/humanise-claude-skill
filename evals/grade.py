#!/usr/bin/env python3
"""Grade humanizer eval outputs against assertions."""
import json
import re
import os

WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iteration-1")
EVALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evals.json")

def extract_final_version(text):
    """Extract only the final rewrite section for grading."""
    # Try "Final Version" section (with-skill format)
    match = re.search(r'##\s+Final Version\s*\n(.*?)(?:\n##|\Z)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Try "Final rewrite"
    match = re.search(r'##\s+Final [Rr]ewrite\s*\n(.*?)(?:\n##|\Z)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Try "Rewritten Text" section (baseline format)
    match = re.search(r'##\s+Rewritten Text\s*\n(.*?)(?:\n##|\Z)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: use full text
    return text

def count_words(text):
    return len(text.split())

def avg_sentence_length(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    return sum(len(s.split()) for s in sentences) / len(sentences)

def check_assertion(assertion, output_text):
    final_text = extract_final_version(output_text)
    atype = assertion["type"]
    value = assertion["value"]

    if atype == "not_contains":
        passed = value.lower() not in final_text.lower()
        evidence = f"Text {'does not contain' if passed else 'CONTAINS'} '{value}'"
        if not passed:
            # Find context
            idx = final_text.lower().find(value.lower())
            start = max(0, idx - 30)
            end = min(len(final_text), idx + len(value) + 30)
            evidence += f". Context: '...{final_text[start:end]}...'"
    elif atype == "word_count_lte":
        wc = count_words(final_text)
        passed = wc <= value
        evidence = f"Final version word count: {wc} (limit: {value})"
    elif atype == "avg_sentence_length_lte":
        avg = avg_sentence_length(final_text)
        passed = avg <= value
        evidence = f"Average sentence length: {avg:.1f} words (limit: {value})"
    else:
        passed = False
        evidence = f"Unknown assertion type: {atype}"

    return {
        "text": assertion["description"],
        "passed": passed,
        "evidence": evidence
    }

def grade_run(eval_id, eval_name, assertions, run_dir):
    output_path = os.path.join(run_dir, "outputs", "output.md")
    if not os.path.exists(output_path):
        print(f"  MISSING: {output_path}")
        return

    with open(output_path) as f:
        output_text = f.read()

    results = [check_assertion(a, output_text) for a in assertions]
    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    grading = {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "pass_rate": passed / total if total > 0 else 0,
        "passed": passed,
        "total": total,
        "expectations": results
    }

    grading_path = os.path.join(run_dir, "grading.json")
    with open(grading_path, "w") as f:
        json.dump(grading, f, indent=2)

    print(f"  {os.path.basename(run_dir)}: {passed}/{total} passed ({100*passed//total if total else 0}%)")
    for r in results:
        status = "✓" if r["passed"] else "✗"
        print(f"    {status} {r['text']}")
        if not r["passed"]:
            print(f"      → {r['evidence']}")

def main():
    with open(EVALS_PATH) as f:
        evals = json.load(f)

    eval_dirs = [
        ("eval-0-corporate-memo", 0),
        ("eval-1-tech-blog", 1),
        ("eval-2-voice-matching", 2),
    ]

    for dir_name, eval_id in eval_dirs:
        eval_data = evals["evals"][eval_id]
        assertions = eval_data["assertions"]
        eval_name = dir_name

        print(f"\n=== {dir_name} ===")

        for run_type in ["with_skill", "without_skill"]:
            run_dir = os.path.join(WORKSPACE, dir_name, run_type)
            print(f"\n  [{run_type}]")
            grade_run(eval_id, eval_name, assertions, run_dir)

if __name__ == "__main__":
    main()
