
def write_invalid_links_to_file(links, reason):
    with open('bin/invalid_links.txt', 'a') as file:
        for link in links:
            file.write(f"{reason}:\t{link}\n")
