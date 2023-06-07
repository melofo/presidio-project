def test_split_file_content():
    file = open("./upload-data/Final_MOCK_DATA.txt", "r")
    file_content = file.read()
    file.close()

    lines = file_content.split("\n")
    # Split the header line by tab and remove leading/trailing spaces
    header = [column.strip() for column in lines[0].split("\t")]
    # Initialize an empty list to store the data rows
    data = []
    # Iterate over the remaining lines
    for line in lines[1:]:
        # Split each line by tab and remove leading/trailing spaces
        row = [column.strip() for column in line.split("\t")]
        # Append the row to the data list
        data.append(row)
    print(data)


if __name__ == "__main__":
    test_split_file_content()
