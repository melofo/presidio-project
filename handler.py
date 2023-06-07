import boto3
import csv
import os


table_name = os.environ.get("tableName")
output_bucket_name = os.environ.get("outputBucketName")


def presidio_lambda(event, context):
    """
    This API endpoint is triggered by an S3 event when a file is created in the input S3 bucket. It performs the following steps:
        1. Retrieve the file information from the S3 event.
        2. Read the file content from S3.
        3. Store the file content as a document in DynamoDB.
        4. Convert the DynamoDB document to a CSV file.
        5. Upload the CSV file to a different location in the output S3 bucket.

    Request
        This API endpoint is triggered automatically by the S3 event. No specific request is required.

    Response
        If the processing is successful, the endpoint returns an HTTP 200 response.
    """
    try:
        # Step 1: Retrieve the file information from the S3 event.
        input_bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]

        # Step 2: Read the file from S3.
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=input_bucket_name, Key=file_key)
        file_content = response["Body"].read().decode("utf-8")

        # Step 3: Store the file content as a document in DynamoDB.
        dynamodb = boto3.client("dynamodb")
        dynamodb.put_item(
            TableName=table_name,
            Item={"file-key": {"S": file_key}, "file-content": {"S": file_content}},
        )

        # Step 4: Convert the DynamoDB document to a CSV file.
        # Split the text into lines
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
        # Write the data to a csv file
        temp_file = "/tmp/temp.csv"
        with open(temp_file, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)  # Write the header row
            writer.writerows(data)  # Write the data rows

        # Step 5: Upload the CSV file to a different location in S3
        base, ext = os.path.splitext(file_key)
        csv_file_key = f"{base}.csv"
        s3 = boto3.resource("s3")
        output_bucket = s3.Bucket(output_bucket_name)
        output_bucket.upload_file(temp_file, csv_file_key)
    except Exception as err:
        print(err)


def get_result(event, context):
    """
    This API endpoint is triggered by an HTTP GET request with a fileName parameter in the path. It performs the following steps:
        1. Retrieve the CSV file content from the output S3 bucket based on the provided fileName.
        2. Return the response with the file URL and content.

    Request
        Method: GET
        Path: /get-result/{fileName}

    Parameters
        {fileName} (required): The name of the file to retrieve the result.

    Response
        HTTP 200: If the file is found in the output S3 bucket, the response body contains the following:
            The URL of the file in the S3 bucket: https://s3.amazonaws.com/{output_bucket_name}/{file_name}
            The file content.
        HTTP 400: If the fileName parameter is missing or the file cannot be found, the response body contains an error message.
    """
    s3 = boto3.client("s3")
    if "pathParameters" not in event or "fileName" not in event["pathParameters"]:
        return {"statusCode": 400, "body": "Missing the fileName from the path"}
    file_name = f"{os.path.splitext(event['pathParameters']['fileName'])[0]}.csv"
    try:
        # Step 1: Retrieve the CSV file content from the output S3 bucket.
        response = s3.get_object(Bucket=output_bucket_name, Key=file_name)
        file_content = response["Body"].read().decode("utf-8")
        # Step 2: Return the response with the file URL and content.
        return {
            "statusCode": 200,
            "body": f"https://s3.amazonaws.com/{output_bucket_name}/{file_name}\n\n\n"
            + file_content,
        }
    except Exception as e:
        print("Error:", e)
        return {"statusCode": 400, "body": "Failed to read data by filename"}
