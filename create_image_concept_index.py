import pandas as pd
import os

# Read image paths
image_paths_df = pd.read_csv(
    '/Users/kariyamaso/EEG_Image_decode/data/THINGS/Metadata/image-paths.csv',
    header=None
)

# Read concepts metadata to get concept names and their order
concepts_df = pd.read_csv(
    '/Users/kariyamaso/EEG_Image_decode/data/THINGS/Metadata/'
    '_concepts-metadata_things.tsv',
    sep='\t'
)

# Create a more comprehensive mapping from folder name to concept ID
folder_to_concept_id = {}

# For each concept in the metadata
for idx, row in concepts_df.iterrows():
    concept_id = idx + 1  # 1-based index
    word = row['Word'].replace(' ', '_')  # Base concept name
    unique_id = row['uniqueID']  # Unique identifier for homonyms

    # Map the uniqueID (which matches folder names for homonyms)
    folder_to_concept_id[unique_id] = concept_id

    # Also map the base word if it's not already mapped
    if word not in folder_to_concept_id:
        folder_to_concept_id[word] = concept_id

# Handle special case for flip_flop -> flip-flop
if 'flip-flop' in folder_to_concept_id:
    folder_to_concept_id['flip_flop'] = folder_to_concept_id['flip-flop']

# Create the image concept index
image_concept_indices = []
unmapped_concepts = set()

for idx, row in image_paths_df.iterrows():
    image_path = row[0]
    # Extract concept name from path
    # (e.g., "images/aardvark/aardvark_01b.jpg" -> "aardvark")
    path_parts = image_path.split('/')

    if len(path_parts) >= 3:
        folder_name = path_parts[1]

        # Try to find the concept ID
        if folder_name in folder_to_concept_id:
            concept_id = folder_to_concept_id[folder_name]
        else:
            concept_id = 0
            unmapped_concepts.add(folder_name)

        image_concept_indices.append(concept_id)
    else:
        print(f"Warning: Unexpected path format: {image_path}")
        image_concept_indices.append(0)

# Print summary of unmapped concepts
if unmapped_concepts:
    print(f"\nUnmapped concepts: {sorted(unmapped_concepts)}")
    print(f"Total unmapped concepts: {len(unmapped_concepts)}")

# Create output dataframe
output_df = pd.DataFrame(image_concept_indices)

# Save to CSV
output_path = (
    '/Users/kariyamaso/EEG_Image_decode/data/THINGS/Metadata/'
    'Concept-specific/image_concept_index.csv'
)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
output_df.to_csv(output_path, header=False, index=False)

print(f"\nCreated image_concept_index.csv with "
      f"{len(image_concept_indices)} entries")
num_unique = len(set(image_concept_indices))
if 0 in image_concept_indices:
    num_unique -= 1
print(f"Number of unique concepts: {num_unique}")
if any(c > 0 for c in image_concept_indices):
    min_id = min(c for c in image_concept_indices if c > 0)
    max_id = max(image_concept_indices)
    print(f"Concept ID range: {min_id} - {max_id}")
print(f"Number of unmapped images: {image_concept_indices.count(0)}")

# Verify the mapping by checking a few examples
print("\nSample mappings:")
sample_indices = [0, 100, 1000, 5000, 10000, 20000]
for i in sample_indices:
    if i < len(image_paths_df):
        path = image_paths_df.iloc[i, 0]
        concept_id = image_concept_indices[i]
        print(f"  {path} -> Concept ID: {concept_id}")