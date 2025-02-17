import streamlit as st
import itertools
import random
import pandas as pd
import numpy as np

st.header("MaxDiff Generator")
st.write("This tool generates all possible combinations of test attributes and randomly select balanced subset of these combinations.")

# Step 1: Define attributes
attributes = st.sidebar.text_input("Enter the attributes separated by commas")

# Step 2: Define the number of attributes per set (e.g., groups of 4)
group_size = st.sidebar.number_input("Enter the number of attributes per group", min_value=1, step=1)

# Step 3: Define the number of groups to generate
num_groups = st.sidebar.number_input("Enter the number of groups to generate", min_value=1, step=1)

if attributes is not None:
    # Convert attributes input to a list and strip wite spaces
    attributes_list = [attr.strip() for attr in attributes.split(",") if attr.strip()]

    # Validate input
    if len(attributes_list) < group_size:
        st.error("The number of attributes must be greater than or equal to the group size.")
    else:
        # Generate all possible combinations
        all_combinations = list(itertools.combinations(attributes_list, group_size))

        # Ensure num_groups is not larger than possible combinations
        #num_groups = len(all_combinations)
        if num_groups > len(all_combinations):
            st.error(f"Number of groups has to be equal or less than {len(all_combinations)} so it doesn't exceed the total number of possible combinations.")
            
        else:
            # Select random groups
            selected_groups = random.sample(all_combinations, num_groups)

            # Display results
            st.success("MaxDiff Groups Generated:")
            df = pd.DataFrame(selected_groups, columns=[f"Attribute {i+1}" for i in range(group_size)])
            
            # Add the 'Groups' column with enumeration starting from 1
            df["Groups"] = range(1, len(df) + 1) 

        
            # Set 'Groups' as the index
            df.set_index("Groups", inplace=True)
            st.dataframe(df)
        
            # Define the string to search for
            search_string = attributes
        
            # Count occurrences across the entire DataFrame
            counts = {s: df.apply(lambda col: col.astype(str).str.contains(s, case=False, na=False)).sum().sum() for s in search_string.split(",")}
            st.write("Possible combinations (number of groups)", len(all_combinations))
            st.write("Attribute occurrences per subset:", counts)
            