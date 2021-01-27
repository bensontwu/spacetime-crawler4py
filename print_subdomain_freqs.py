from collections import defaultdict

def print_subdomain_freqs(subdomain_freqs):
    for subdomain in sorted(subdomain_freqs):
        print(f"{subdomain}:\t{subdomain_freqs[subdomain]}")

if __name__ == "__main__":
    file_name = "bin/sub_domains.txt"
    subdomain_freqs = defaultdict(int)

    with open(file_name, 'r') as f:
        for line in f:
            subdomain_freqs[line.strip()] += 1
    
    print_subdomain_freqs(subdomain_freqs)