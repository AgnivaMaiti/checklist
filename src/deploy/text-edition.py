import os
import datetime
from bs4 import BeautifulSoup

# Create a directory named "text_list" in the current working directory if it doesn't exist
output_directory = "text_list"
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# List all HTML files in the parent directory (../)
parent_directory = "../"
html_files = [file for file in os.listdir(parent_directory) if file.endswith(".html")]

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Count of HTML files
total_files = len(html_files)

# Print "Conversion started" once at the beginning
print("Conversion started:")

# Iterate through each HTML file
for index, html_file_name in enumerate(html_files, start=1):

    # Print the conversion progress
    print(f"({index}/{total_files}) {html_file_name} converted...")

    # Read HTML content from the HTML file
    with open(os.path.join(parent_directory, html_file_name), 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize text content
    text_content = ''

    # Find the major heading and description
    header = soup.find('header')
    major_heading = header.find('h1', class_='title').text.strip()
    description = header.find_all('p', class_='text_small')[-1].text.strip()

    # Add the major heading to the text content
    text_content += f"{major_heading}\n\n"
    text_content += f"{description}\n\n"

    # Find all the sections with class "checklist"
    sections = soup.find_all('section', class_='checklist')

    # Iterate through each section
    for section in sections:
        # Get the section title
        section_title = section.find('h2', class_='checklist__title').text.strip()

        # Underline the section title with '=' characters
        section_title_text = f"{section_title}\n{'=' * len(section_title)}\n"

        # Add an extra newline before each major section (except the first one)
        if section_title != 'Week 1: -':
            text_content += '\n'

        # Add the section title to the text content
        text_content += section_title_text

        # Find all checklist items within the section
        checklist_items = section.find_all('li', class_='checklist-item')

        # Initialize item counter for numbering
        item_counter = 1

        # Iterate through each checklist item
        for item in checklist_items:
            # Get the checklist item title (bold)
            item_title = item.find('span', class_='checklist-item__title').text.strip()

            # Get the checklist item description
            item_description = item.find('div', class_='info').text.strip()

            # Find links within the description
            item_links = item.find_all('a')
            links_text = f"Links ({len(item_links)}): {', '.join([link['href'] for link in item_links])}"

            # Combine the title, description, and links into a single text item
            item_text = f"{item_counter}. {item_title}\n  {item_description}\n  {links_text}\n"

            # Increment the item counter
            item_counter += 1

            # Append the item to the section's text content
            text_content += item_text

        # Add a separator line before the new last line
        text_content += "\n---\n"

    # Add a new line at the end with the generation information
    text_content += f"Generated by OpenGenus. Updated on {current_date}"

    # Write the text content to a file in the "text_list" directory with the same name as the HTML file
    text_file_name = os.path.splitext(html_file_name)[0] + ".txt"
    with open(os.path.join(output_directory, text_file_name), 'w', encoding='utf-8') as text_file:
        text_file.write(text_content)

# Print the final message when all conversions are complete
print(f"All {total_files} checklists converted to text.")