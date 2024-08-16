from bplustree import BPlusTree

# Define the fanout
fanout = 4

# Create a B+ Tree
b_plus_tree = BPlusTree(fanout)

# Insertion Order
insertion_order = ["René", "Arianna", "Biascica", "Lopez", "Alessandro",
                   "Gloria", "Karin", "Itala", "Duccio", "Stanis"]

# Insert keys
print("B+ Tree Insertion Steps:\n")
for key in insertion_order:
    print(f"Inserting: {key}")
    b_plus_tree.insert(key)
    print("Current B+ Tree State:")
    print(b_plus_tree.print_tree_state())
    print("-" * 50)

# Deletion Order
print("\n\n\n")
deletion_order = ["René", "Biascica", "Gloria", "Alessandro", "Stanis"]

print("\nB+ Tree Deletion Steps:\n")
for key in deletion_order:
    print(f"Deleting: {key}")
    b_plus_tree.delete(key)
    print("Current B+ Tree State:")
    print(b_plus_tree.print_tree_state())
    print("-" * 50)
