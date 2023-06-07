# presidio-project

This is the README document for the `presidio-project` program. It provides instructions for setting up and running the program on AWS using the Serverless Framework.

## Prerequisites

Before running the `presidio-project` program, make sure you have the following prerequisites:

- An AWS account with appropriate permissions.
- Node.js and npm installed on your machine.
- Serverless Framework installed globally. You can install it by running the following command:

  ```bash
  npm install -g serverless
  ```

## Setup

To set up the `presidio-project` program, follow these steps:

1. Create an IAM User with programmatic access, administrator access, and access key ID and secret access key.
2. Configure the Serverless Framework with your AWS credentials. Run the following command and replace `{access key ID}` and `{secret access key}` with the credentials of your IAM User:

   ```bash
   serverless config credentials --provider aws --key {access key ID} --secret {secret access key} --profile serverlessUser
   ```

## Deployment

To deploy the `presidio-project` program on AWS, perform the following steps:

1. Clone the repository and navigate to the project directory.
2. Install the project dependencies by running the following command:

   ```bash
   npm install
   ```

3. Modify the `serverless.yml` file to configure the necessary AWS resources. Update the values for `custom.inputBucketName`, `custom.tableName`, and `custom.outputBucketName` to specify the desired names for the S3 buckets and DynamoDB table.

4. Deploy the program using the Serverless Framework. Run the following command:

   ```bash
   serverless deploy --aws-profile serverlessUser
   ```

   This command will deploy the program to the specified AWS region (us-west-1 by default).

5. After the deployment is successful, note the output values for `custom.inputBucketName`, `custom.tableName`, and `custom.outputBucketName`. You will need these values for the next steps.

## Running the Program

The `presidio-project` program consists of two functions:

1. **presidio_lambda**: This function is triggered by an S3 event when a file is created in the input S3 bucket. It performs the following steps:
   - Retrieves the file information from the S3 event.
   - Reads the file content from S3.
   - Stores the file content as a document in DynamoDB.
   - Converts the DynamoDB document to a CSV file.
   - Uploads the CSV file to a different location in the output S3 bucket.

2. **get_result**: This function is triggered by an HTTP GET request with a `fileName` parameter in the path. It performs the following steps:
   - Retrieves the CSV file content from the output S3 bucket based on the provided `fileName`.
   - Returns the response with the file URL and content.

To run the program, follow these steps:

1. Trigger the `presidio_lambda` function by creating a file in the input S3 bucket. The bucket name is `custom.inputBucketName`. You can upload a file manually using the AWS S3 console or programmatically using the AWS SDK.

2. To retrieve the result, send an HTTP GET request to the `get-result` function endpoint with the `fileName` parameter in the path. The endpoint URL should be in the following format:

   ```
   https://your-api-gateway-url/get-result/{fileName}
   ```

   Replace `{fileName}` with the name of the file for which you want to retrieve the result.

   The response will include the URL of the file in the output S3 bucket

 (`https://s3.amazonaws.com/{output_bucket_name}/{file_name}`) and the file content.

## Cleanup

To remove the deployed resources and clean up the AWS environment, you can run the following command:

```bash
serverless remove --aws-profile serverlessUser
```

This command will remove all the AWS resources created for the `presidio-project` program.

Note: The removal process may take a few minutes to complete.

## Conclusion

You have successfully set up and deployed the `presidio-project` program on AWS using the Serverless Framework. You can now trigger the `presidio_lambda` function by uploading a file to the input S3 bucket and retrieve the result using the `get-result` function.

If you have any questions or encounter any issues, please don't hesitate to reach out for assistance.
