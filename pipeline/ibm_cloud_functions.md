# Neural Style Transfer - Data Pipeline

## 1. Training

#### Pipeline overview
Image (Jetson/Web-server) -> IBM Cloudant (store image) -> IBM Functions (train) -> IBM Cloudant (store model) -> Jetson/Web-server

## 2. Inference

### Case 1: Image Style Transfer

#### Pipeline overview
Jetson (take picture) -> Cloudant (store image) -> Functions (inference) -> Cloudant (store output) -> web-server/Jetson (display output)


### Case 2: Video Stream Style Transfer

#### Pipeline overview
Jetson (stream video) -> Event Streams (receives video) + Cloudant (stored model) -> Functions (inference) -> Event Streams (streams output) -> web-server/Jetson (displays output)

## Generic pipeline test

#### Setup IBM Cloudant service

1. Identify IBM Cloud API endpoint.
    ```bash
    ibmcloud api https://cloud.ibm.com
    ```

2. Login to IBM Cloud account.
    ```bash
    ibmcloud login
    ```

3. Set  target resource group and region (see available regions with `ibmcloud regions` and groups with `ibmcloud resource groups`).
    ```bash
    ibmcloud target -r us-south -g Default
    ```

4. Create Cloudant service instance (start with lite plan, upgrade to standard if necessary, see [lite vs standard plan](https://cloud.ibm.com/docs/services/Cloudant?topic=cloudant-ibm-cloud-public#plans)).
    ```bash
    ibmcloud resource service-instance-create neural_transfer cloudantnosqldb lite us-south -p '{"legacyCredentials": true}'
    ```
    Check that the instance is active with `ibmcloud resource service-instance neural_transfer`. 

5. Create credentials for Cloudant service.
    ```bash
    ibmcloud resource service-key-create creds_for_neural_transfer Manager --instance-name neural_transfer
    ```
    These credentials can be retrieved later with  `ibmcloud resource service-key creds_for_neural_transfer`.


#### Store data in IBM Cloudant

1. Install cloudant Python package with `pip3 install cloudant`.

2. Connect to Cloudant service instance.

    ```python
    from cloudant.client import Cloudant
    from cloudant.error import CloudantException
    from cloudant.result import Result, ResultByKey
    
    serviceUsername = "<username>"
    servicePassword = "<password>"
    serviceURL = "url"
    
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()
    ```

3. Create a database within Cloudant instance.

    ```python
    # Create database
    databaseName = "neural_transfer_images"
    imagesDB = client.create_database(databaseName)

    # Check that database exists
    if ntImagesDatabase.exists():
        print("'{0}' Successfully created.\n".format(databaseName))
    ```

4. Store data in Cloudant database. Data in Cloudant has to be stored in JSON format. Images and video can be attached to JSON.

    ```python
    # Create test data
    sampleData = [
        [1, "one", "boiling", 100],
        [2, "two", "hot", 40],
        [3, "three", "warm", 20],
        [4, "four", "cold", 10],
        [5, "five", "freezing", 0]
    ]
    
    # Convert each entry to JSON and load to database.
    for document in sampleData:
        # Retrieve the fields in each row.
        number = document[0]
        name = document[1]
        description = document[2]
        temperature = document[3]

        # Create a JSON document that represents
        # all the data in the row.
        jsonDocument = {
            "numberField": number,
            "nameField": name,
            "descriptionField": description,
            "temperatureField": temperature
        }

        # Create a document using the Database API.
        newDocument = imagesDB.create_document(jsonDocument)

        # Check that the document exists in the database.
        if newDocument.exists():
            print("Document '{0}' successfully created.".format(number))
    ```

    Expected output:

    ```python
    Document '1' successfully created.
    Document '2' successfully created.
    Document '3' successfully created.
    Document '4' successfully created.
    Document '5' successfully created.
    ```

#### Setup IBM Cloud Functions

1. Install IBM Cloud Functions CLI

    ```bash
    # Install cloud functions
    ibmcloud plugin install cloud-functions
    # Set resource group and region
    ibmcloud target -r us-south -g Default
    ```

2. Setup namespace.

    ```bash
    # Create namespace
    ibmcloud fn namespace create neural-transfer
    # Set CLI context to new namespace
    ibmcloud fn property set --namespace neural-transfer
    ```

    Check that the namespace was setup correctly with `ibmcloud fn property get --namespace` and `ibmcloud fn namespace list | grep neural transfer` (the ids should match).


#### Cloudant to Functions to Cloudant

1. Bind Functions to Cloudant (bind to [Apache OpenWhisk package for Cloudant](https://github.com/apache/openwhisk-package-cloudant)).

    ```bash
    ibmcloud fn package bind /whisk.system/cloudant neural_transfer
    ibmcloud fn service bind cloudantnosqldb neural_transfer --instance neural_transfer
    ```

    Check that the binding was set correctly with `ibmcloud fn package get neural_transfer parameters`. 

2. Attach a trigger to Cloudant database

    ```bash
    ibmcloud fn trigger create data_inserted_trigger --feed neural_transfer/changes --param dbname "neural_transfer_images"
    ```

3. Create an action to process changes to the database. Store the following code as `process_change.py`.

    ```python
    def main(params):
        print(params)
        return params
    ```

    Deploy function from the Python file.

    ```bash
    ibmcloud fn action create process_change process_change.py --kind python:3.6
    ```

    Verify the creation of the action by invoking it explicitly (in a separate window, monitor functions logs with `ibmcloud fn activation poll`)

    ```bash
    ibmcloud fn action invoke --blocking --param name test_name process_change
    ```

    Expected output:
    ```bash
    Activation: 'process_change' (f2f55f3bd00c4f28b55f3bd00c0f2801)
    [
        "2019-11-16T21:12:09.311714Z    stdout: {'name': 'test_name'}"
    ]
    ```

5. Create an action sequence and map to the trigger with a rule. Here, we connect the package Cloudant  `read` action with the `process_change` action. The parameters from the cloudant `read` action will be passed automatically to the `proces_change` action.

    ```bash
    # Create action sequence
    ibmcloud fn action create process_change_cloudant_sequence --sequence neural_transfer/read,process_change
    
    # Create rule
    ibmcloud fn rule create log_change_rule data_inserted_trigger process_change_cloudant_sequence
    ```

6. Test by loading data to Cloudant from the Jetson unit (monitor with `ibmcloud fn activation poll`). Retrieve credentials with `ibmcloud resource service-key creds_for_neural_transfer`.

    ```python
    from cloudant.client import Cloudant
    from cloudant.error import CloudantException
    from cloudant.result import Result, ResultByKey
    
    # Connect to client
    serviceUsername = "<username>"
    servicePassword = "<password>"
    serviceURL = "url"
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()    
    imageDB = client['neural_transfer_images']
    if imageDB.exists():
        print("Database exists")

    # Load data to Cloudant
    jsonDocument = {"name": "test_name"}
    loadDocument = imageDB.create_document(jsonDocument)
    if loadDocument.exists():
        print("Document loaded successfully")
    ```

    Output expected:

    ```bash
    Activation: 'data_inserted_trigger' (42c535f8f3f74a3e8535f8f3f7ea3e95)
    [
        "{\"statusCode\":0,\"success\":true,\"activationId\":\"b2870ad8f6cb495f870ad8f6cb895fe6\",\"rule\":\"bdee6dba-3d83-46c7-bf5c-066bb6bb7a59/log_change_rule\",\"action\":\"bdee6dba-3d83-46c7-bf5c-066bb6bb7a59/process_change_cloudant_sequence\"}"
    ]

    Activation: 'process_change' (c6e880ba5f594528a880ba5f594528bd)
    [
        "2019-11-16T23:24:28.431974Z    stdout: {'_id': 'a74fda0637ffd6e85e783c22924c66d2', '_rev': '1-7088d371adfb8115d92db204026e643f', 'name': 'test_name_2'}"
    ]

    Activation: 'read' (b3b344eb6e174bfab344eb6e17abfa41)
    [
        "2019-11-16T23:24:28.379399Z    stdout: success { _id: 'a74fda0637ffd6e85e783c22924c66d2',",
        "2019-11-16T23:24:28.379439Z    stdout: _rev: '1-7088d371adfb8115d92db204026e643f',",
        "2019-11-16T23:24:28.379445Z    stdout: name: 'test_name_2' }"
    ]

    Activation: 'process_change_cloudant_sequence' (b2870ad8f6cb495f870ad8f6cb895fe6)
    [
        "b3b344eb6e174bfab344eb6e17abfa41",
        "c6e880ba5f594528a880ba5f594528bd"
    ]

    ```

#### Cloudant to User



## References

- [Cloudant Python Client](https://github.com/cloudant/python-cloudant)
- [Cloudant documentation](https://cloud.ibm.com/docs/services/Cloudant?topic=cloudant-getting-started)
- [Retrieving data from Cloudant](https://cloud.ibm.com/docs/services/Cloudant?topic=cloudant-creating-and-populating-a-simple-ibm-cloudant-database-on-ibm-cloud#retrieving-data)