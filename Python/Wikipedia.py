import wikipedia

def Search(SearchTerm:str) -> str:
    wikipedia.search(SearchTerm)[0]

def Generate(Input:str) -> str:
    pass

if __name__ == "__main__":
    print()