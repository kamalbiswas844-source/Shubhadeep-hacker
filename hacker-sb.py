#!/usr/bin/env python3
# wordlist_tool.py — Menu-based wordlist generator (educational purpose)
# Usage: python3 wordlist_tool.py

import itertools
import gzip
import sys
import random

def get_opener(filename):
    return gzip.open if filename.endswith(".gz") else open

# ---------- Option 1: Auto-generate ----------
def auto_generate():
    print("\n--- Auto Generate (Hackers) ---")

    # 1) File name (FIRST)
    out_file = input("Set your file name: ").strip() or "generated.txt"

    # Charset
    print("\nwordlist create menu:")
    print("  [1] Lowercase (a-z)")
    print("  [2] Uppercase (A-Z)")
    print("  [3] Digits (0-9)")
    print("  [4] Lowercase + digits")
    print("  [5] All in one mix")
    print("  [6] All (a-z, A-Z, 0-9, symbols)")
    print("  [7] Custom charset")
    choice = input("Choose charset [1-7]: ").strip()

    presets = {
        "1": "abcdefghijklmnopqrstuvwxyz",
        "2": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "3": "0123456789",
        "4": "abcdefghijklmnopqrstuvwxyz0123456789",
        "5": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "6": ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
              "0123456789!@#$%^&*()-_=+"),
    }
    charset = presets.get(choice)
    if charset is None:
        if choice == "7":
            charset = input("Enter custom charset: ")
        else:
            print("Invalid choice."); return

    # 2) Word length (SECOND)
    word_len = int(input("Word length (e.g. 6): ").strip() or 6)
    if word_len < 1:
        print("Length must be >= 1"); return

    # 3) How many million lines (THIRD)
    millions = float(input("How many million lines? (e.g. 5 = 5,000,000): ").strip() or 1)
    target = int(millions * 1_000_000)

    total_space = len(charset) ** word_len
    print(f"\nPossible combinations of length {word_len}: {total_space:,}")
    if target > total_space:
        print(f"NOTE: Target ({target:,}) > total space ({total_space:,}) — duplicates will be avoided by shuffling unique words only.")

    # If target fits within the space -> generate unique random words
    # If target > space -> generate all unique, then pad with duplicates if needed
    count = 0
    with get_opener(out_file)(out_file, "wt", errors="ignore") as out:
        if target <= total_space and total_space <= 50_000_000:
            # Small enough: build all, shuffle, take target
            print("Generating unique words...")
            words = ["".join(c) for c in itertools.product(charset, repeat=word_len)]
            random.shuffle(words)
            for w in words[:target]:
                out.write(w + "\n")
                count += 1
                if count % 1_000_000 == 0:
                    print(f"\rGenerated: {count:,}", end="", flush=True)
        else:
            # Large space: random sampling on the fly
            print("Generating random words (streaming)...")
            seen = set()
            while count < target:
                w = "".join(random.choice(charset) for _ in range(word_len))
                if w in seen:
                    continue
                seen.add(w)
                out.write(w + "\n")
                count += 1
                if count % 1_000_000 == 0:
                    print(f"\rGenerated: {count:,} (unique)", end="", flush=True)
                    # If space is huge, don't blow memory tracking seen forever
                    if len(seen) > 20_000_000:
                        seen.clear()
    print(f"\nDone: {count:,} words written to {out_file}")

# ---------- Option 2: Mutate user's own wordlist ----------
SUFFIXES = ["", "1", "12", "123", "1234", "!", "!!", "!!!", "@", "#", "2024", "2025", "2026"]
PREFIXES = ["", "1", "!", "@", "#"]
LEET     = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}
CASES    = [str.lower, str.upper, str.capitalize]

def leet(word):
    return "".join(LEET.get(c, c) for c in word)

def mutate_own_wordlist():
    print("\n--- Set your wordlist ---")
    base_file = input("Set your wordlist  file name: ").strip()
    try:
        base_handle = open(base_file, "r", errors="ignore")
    except FileNotFoundError:
        print("File not found!"); return

    out_file = input("Set your wordlist file name: ").strip() or "mutated.txt"
    limit = input("Max words limit [press Enter for unlimited]: ").strip()
    limit = int(limit) if limit else None

    count = 0
    with base_handle as base, get_opener(out_file)(out_file, "wt", errors="ignore") as out:
        for line in base:
            word = line.strip()
            if not word:
                continue
            seen = set()
            for case_fn in CASES:
                w = case_fn(word)
                for pre, suf in itertools.product(PREFIXES, SUFFIXES):
                    m = pre + w + suf
                    if m not in seen:
                        seen.add(m)
                        out.write(m + "\n")
                        count += 1
                l = leet(w)
                if l not in seen:
                    seen.add(l)
                    out.write(l + "\n")
                    count += 1
                if limit and count >= limit:
                    print(f"Limit reached: {count:,} words written.")
                    return
            if count % 1_000_000 < 20:
                print(f"\rGenerated: {count:,}", end="", flush=True)
    print(f"\nDone: {count:,} words written to {out_file}")

# ---------- Main menu ----------
def main():
    while True:
        print("\n===== (SHUBHADEEP)<=>(HACKER) =====")
        print("1) Auto generate wordlist (hackers)")
        print("2) Generate costom wordlist (hackers)")
        print("3) Exit")
        choice = input("Select option plz [1-3]:  ").strip()

        if choice == "1":
            auto_generate()
        elif choice == "2":
            mutate_own_wordlist()
        elif choice == "3":
            print("by (hackers)")
            sys.exit(0)
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()