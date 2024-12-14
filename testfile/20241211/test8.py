import shlex

while True:
    # List to store all dragged files
    all_file_paths = []

    print("Drag and drop files into the terminal. Press Enter with no input to finish.")

    # Continuously capture input until the user presses Enter with no input
    while True:
        # Capture input (files dragged into the terminal)
        file_paths = input("Drag and drop files here: ")
        
        # If input is empty (user pressed Enter with no files), exit the loop
        if not file_paths:
            break
        
        # Use shlex.split to safely handle spaces, quotes, and no spaces
        new_files = shlex.split(file_paths)
        
        # Add the newly captured files to the list of all files
        all_file_paths.extend(new_files)

    # Print out all collected files
    print("\nThe files you selected are:")
    for file in all_file_paths:
        print(file)
