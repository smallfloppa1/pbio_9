# Album number: s30460
# Date: 2026-04-30
# Description: Random DNA sequence generator in FASTA format

import random
import sys

NUCLEOTIDES = ["A", "C", "G", "T"]
BASE_PAIRS = {"A": "T", "T": "A", "C": "G", "G": "C"}


def get_valid_length():
    while True:
        raw = input("Sequence length: ")
        try:
            n = int(raw)
        except ValueError:
            print("Invalid input. Enter an integer between 1 and 100000.")
            continue
        if n < 1 or n > 100_000:
            print("Invalid input. Enter an integer between 1 and 100000.")
        else:
            return n


def get_valid_id():
    while True:
        sid = input("Sequence ID: ")
        if sid == "":
            print("ID must not be empty.")
        elif " " in sid or "\t" in sid or "\n" in sid:
            print("ID must not contain spaces or tabs.")
        else:
            return sid


def make_dna(n):
    return "".join(random.choice(NUCLEOTIDES) for _ in range(n))


def stats(seq):
    total = len(seq)
    result = {}
    for base in NUCLEOTIDES:
        result[base] = round(seq.count(base) / total * 100, 2)
    result["GC"] = round(result["G"] + result["C"], 2)
    return result


def show_stats(st, n):
    print(f"\nStatistics (length={n}):")
    for base in NUCLEOTIDES:
        print(f"  {base}: {st[base]:.2f}%")
    print(f"  GC-content: {st['GC']:.2f}%")


def embed_name(seq, name):
    idx = random.randint(0, len(seq))
    return seq[:idx] + name.lower() + seq[idx:]


def to_fasta(sid, desc, seq, width=80):
    if desc.strip() == "":
        header = f">{sid}"
    else:
        header = f">{sid} {desc}"
    chunks = []
    pos = 0
    while pos < len(seq):
        chunks.append(seq[pos:pos + width])
        pos += width
    return header + "\n" + "\n".join(chunks)


def save_fasta(filename, content):
    with open(filename, "w") as fh:
        fh.write(content)
        fh.write("\n")


def find_motif(seq, motif):
    hits = []
    motif = motif.upper()
    i = 0
    while i <= len(seq) - len(motif):
        if seq[i:i + len(motif)].upper() == motif:
            hits.append(i + 1)
        i += 1
    return hits


def ask_and_find_motif(seq):
    motif = input("\nSearch for motif (e.g. ATG): ").strip()
    if motif == "":
        return
    found = find_motif(seq, motif)
    if len(found) == 0:
        print(f"Motif '{motif.upper()}' was not found.")
    else:
        positions_str = ", ".join(str(p) for p in found)
        print(f"Motif '{motif.upper()}' found {len(found)} time(s) at: {positions_str}")


def get_complement(seq):
    return "".join(BASE_PAIRS[ch] for ch in seq.upper())


def get_reverse_complement(seq):
    return get_complement(seq)[::-1]


def build_complement_fasta(sid, desc, seq, width=80):
    comp = get_complement(seq)
    rcomp = get_reverse_complement(seq)
    part1 = to_fasta(f"{sid}_complement", f"complement | {desc}", comp, width)
    part2 = to_fasta(f"{sid}_rev_complement", f"reverse complement | {desc}", rcomp, width)
    return part1 + "\n" + part2


def dna_to_rna(seq):
    rna = ""
    for ch in seq.upper():
        if ch == "T":
            rna += "U"
        else:
            rna += ch
    return rna


def build_mrna_fasta(sid, desc, seq, width=80):
    rna = dna_to_rna(seq)
    return to_fasta(f"{sid}_mRNA", f"transcription | {desc}", rna, width)


def run_batch(count, length, desc, username):
    all_records = []
    for num in range(1, count + 1):
        sid = f"seq{num:04d}"
        dna = make_dna(length)
        st = stats(dna)
        show_stats(st, length)
        dna_display = embed_name(dna, username)
        record = to_fasta(sid, desc, dna_display)
        all_records.append(record)
    return "\n".join(all_records)


def main():
    mode = input("Batch mode? (y/n): ").strip().lower()

    if mode == "y":
        count = get_valid_length()
        length = get_valid_length()
        desc = input("Description (optional): ")
        username = input("Your name: ")
        output = run_batch(count, length, desc, username)
        out_file = "batch_output.fasta"
        save_fasta(out_file, output)
        print(f"\n{count} sequences saved to {out_file}")

    else:
        length = get_valid_length()
        sid = get_valid_id()
        desc = input("Description (optional): ")
        username = input("Your name: ")

        dna = make_dna(length)
        st = stats(dna)
        show_stats(st, length)

        dna_with_name = embed_name(dna, username)
        fasta_out = to_fasta(sid, desc, dna_with_name)

        ask_and_find_motif(dna)

        comp_fasta = build_complement_fasta(sid, desc, dna)
        fasta_out += "\n" + comp_fasta

        mrna_fasta = build_mrna_fasta(sid, desc, dna)
        fasta_out += "\n" + mrna_fasta

        out_file = f"{sid}.fasta"
        save_fasta(out_file, fasta_out)
        print(f"\nSaved to {out_file}")
        print("(Contains: original, complement, reverse complement, mRNA)")


if __name__ == "__main__":
    main()