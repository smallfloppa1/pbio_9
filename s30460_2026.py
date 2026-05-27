# Album number: s30460
# Date: 2026-04-30
# Description: Random DNA sequence generator in FASTA format

import random
import sys

NUCLEOTIDES = ["A", "C", "G", "T"]
BASE_PAIRS = {"A": "T", "T": "A", "C": "G", "G": "C"}


def get_valid_length():
    """Asks user for sequence length, repeats until valid integer in [1, 100000]."""
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
    """Asks user for a sequence ID, rejects empty strings and whitespace."""
    while True:
        sid = input("Sequence ID: ")
        if sid == "":
            print("ID must not be empty.")
        elif " " in sid or "\t" in sid or "\n" in sid:
            print("ID must not contain spaces or tabs.")
        else:
            return sid


def make_dna(n):
    """Generates a random DNA string of length n from A, C, G, T."""
    return "".join(random.choice(NUCLEOTIDES) for _ in range(n))


def stats(seq):
    """Returns a dict with percentage of each nucleotide and GC-content."""
    total = len(seq)
    result = {}
    for base in NUCLEOTIDES:
        result[base] = round(seq.count(base) / total * 100, 2)
    result["GC"] = round(result["G"] + result["C"], 2)
    return result


def show_stats(st, n):
    """Prints nucleotide percentages and GC-content to the console."""
    print(f"\nStatistics (length={n}):")
    for base in NUCLEOTIDES:
        print(f"  {base}: {st[base]:.2f}%")
    print(f"  GC-content: {st['GC']:.2f}%")


def embed_name(seq, name):
    """Inserts the user's name in lowercase at a random position in the sequence."""
    idx = random.randint(0, len(seq))
    return seq[:idx] + name.lower() + seq[idx:]


def to_fasta(sid, desc, seq, width=80):
    """Formats a sequence as a FASTA record with lines of given width."""
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
    """Writes FASTA content to a file with a trailing newline."""
    with open(filename, "w") as fh:
        fh.write(content)
        fh.write("\n")


def find_motif(seq, motif):
    """Finds all positions of a motif in the sequence """
    hits = []
    motif = motif.upper()
    i = 0
    while i <= len(seq) - len(motif):
        if seq[i:i + len(motif)].upper() == motif:
            hits.append(i + 1)
        i += 1
    return hits


def ask_and_find_motif(seq):
    """Prompts the user for a motif and displays all found positions."""
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
    """Returns the complementary DNA strand using base pairing rules."""
    return "".join(BASE_PAIRS[ch] for ch in seq.upper())


def get_reverse_complement(seq):
    """Returns the reverse complement of the DNA sequence."""
    return get_complement(seq)[::-1]


def build_complement_fasta(sid, desc, seq, width=80):
    """Builds FASTA records for both complement and reverse complement."""
    comp = get_complement(seq)
    rcomp = get_reverse_complement(seq)
    part1 = to_fasta(f"{sid}_complement", f"complement | {desc}", comp, width)
    part2 = to_fasta(f"{sid}_rev_complement", f"reverse complement | {desc}", rcomp, width)
    return part1 + "\n" + part2


def dna_to_rna(seq):
    """Transcribes DNA to mRNA by replacing T with U."""
    rna = ""
    for ch in seq.upper():
        if ch == "T":
            rna += "U"
        else:
            rna += ch
    return rna


def build_mrna_fasta(sid, desc, seq, width=80):
    """Builds a FASTA record for the transcribed mRNA sequence."""
    rna = dna_to_rna(seq)
    return to_fasta(f"{sid}_mRNA", f"transcription | {desc}", rna, width)


def run_batch(count, length, desc, username):
    """Generates multiple sequences with auto-numbered IDs as multi-FASTA."""
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
    """Main function — handles batch or single mode and runs all features."""
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