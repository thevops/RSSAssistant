import sys
import feedparser


def print_feed_fields(feed):
    items = feedparser.parse(feed)
    for k, v in items.entries[0].items():
        print(f"\nKey: {k:15}")
        print(f"Type of Value: {type(v)}")
        print(f"Value: {v}\n")
        print("=" * 30)

def print_feed_len(feed):
    items = feedparser.parse(feed)
    print("Feed length (number of items):", len(items.entries))


if __name__ == "__main__":
    if sys.argv[1]:
        url = sys.argv[1]
    else:
        url = input("Enter feed url: ")
    print("-" * 60)
    print_feed_len(url)
    print("-" * 60)
    print_feed_fields(url)
