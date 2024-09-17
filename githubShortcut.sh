#!/bin/bash

# Define variables
github_url="https://github.com/aebes5/UCD-CS-Courses.git"
ending_path="$1"
file_path="$2"
repo_name="UCD-CS-Courses"
branch_name="main"  # Assuming the main branch is used, replace with "master" if necessary

# Clone the repository
git clone "$github_url" "$repo_name"

# Move the file to the repository directory
mv "$file_path" "$repo_name/$ending_path"

# Navigate to the repository directory
cd "$repo_name"

# Add the file, commit changes, and push to origin
git add .
git commit -m "Added $ending_path"
git branch -m "$branch_name"  # Rename the branch if necessary
git push -u origin "$branch_name"

rm -r *
cd ..
rm -rf "$repo_name"