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


def embed_name(seq, name):
    pass


def to_fasta(sid, desc, seq, width=80):
    pass


def main():
    pass


if __name__ == "__main__":
    main()