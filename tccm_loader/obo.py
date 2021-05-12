from tccm_api.loader.obo_loader import OboLoader
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python -m tccm_loader.obo [name]")
        sys.exit(1)
    name = sys.argv[1]
    loader = OboLoader(f"http://purl.obolibrary.org/obo/{name}.obo", f"http://purl.obolibrary.org/obo/{name}.owl")
    loader.to_termci()
    with open(f'{name}.ttl', 'w', encoding='utf-8') as file:
        file.write(loader.graph.serialize(format='turtle').decode('utf-8'))