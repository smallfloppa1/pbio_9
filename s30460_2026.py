import random
import sys

NUCLEOTIDES = ["A", "C", "G", "T"]


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


def main():
    length = get_valid_length()
    sid = get_valid_id()
    desc = input("Description (optional): ")
    username = input("Your name: ")

    dna = make_dna(length)
    st = stats(dna)
    show_stats(st, length)

    dna_with_name = embed_name(dna, username)
    fasta_out = to_fasta(sid, desc, dna_with_name)

    out_file = f"{sid}.fasta"
    save_fasta(out_file, fasta_out)
    print(f"\nSaved to {out_file}")


if __name__ == "__main__":
    main()