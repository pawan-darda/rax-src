Feature: Deploy Devices via POST

    As a maintainer of Inventory for project Newton devices
    I want to get device ids for one or more devices available on an aggr
    And mark those devices as allocated
    So that I can automate the allocation of these devices for customers
    And update inventory counts

    Background:

        Given I am authenticated with NIS API
        And I send a POST request to NIS API's Deploy resource

    @positive
    Scenario: Requesting a one device from a single aggr with a well formatted request
    
        When request body is a JSON object described as
            | sku          | 123456            |
            | datacenter   | 'IAD1'            |
            | aggr         | 'aggr501E.ord1'   |
            | quantity     | 1                 |
        And at least 1 firewall device exists with a matching datacenter and aggr
        And at least 1 server device exists with a matching datacenter and aggr
        Then the response code should be 200
        And the Content-Type Header should be "application/json"
        And the response body is a JSON object with key 'data' and an array value
        And each element in the array is a JSON object with a 'sku' key and a 'devices' key
        And the 'sku' key is in integer
        And the 'devices' key is an array of integers matching device ids
        And the array contains 1 firewall device with a matching datacenter and aggr
        And the array contains 1 server device with a matching datacenter and aggr
        And an invetory GET shows that the returned firewall and server have is_allocated equals 'true'

    @positive
    Scenario: Requesting a more than one device from a single aggr with a well formatted request
    
        When request body is a JSON object described as
            | sku          | 123456            |
            | datacenter   | 'IAD1'            |
            | aggr         | 'aggr501E.ord1'   |
            | quantity     | 3                 |
        And at least 1 firewall device exists with a matching datacenter and aggr
        And at least <quantity> server devices exists with a matching datacenter and aggr
        Then the response code should be 200
        And the Content-Type Header should be "application/json"
        And the response body is a JSON object with key 'data' and an array value
        And each element in the array is a JSON object with a 'sku' key and a 'devices' key
        And the 'sku' key is in integer
        And the 'devices' key is an array of integers matching device ids
        And the array contains 1 firewall device with a matching datacenter and aggr
        And the array contains <quantity> server devices with a matching datacenter and aggr
        And an invetory GET shows that the returned firewall and server have is_allocated equals 'true'

    @positive
    Scenario: Requesting one or more devices from a multiple aggrs with a well formatted request
    
        When request body is an array with 
        And each element in the array is a JSON object with formatting similar to
            | sku          | 123456            |
            | datacenter   | 'IAD1'            |
            | aggr         | 'aggr501E.ord1'   |
            | quantity     | 1                 |
        And at least 1 firewall device exists for each requested datacenter and aggr
        And at least <quantity> server devices exists for each requested datacenter and aggr
        Then the response code should be 200
        And the Content-Type Header should be "application/json"
        And the response body is a JSON object with key 'data' and an array value
        And each element in the array is a JSON object with a 'sku' key and a 'devices' key
        And the 'sku' key is in integer
        And the 'devices' key is an array of integers matching device ids
        And the array contains 1 firewall device for each requested aggr
        And the array contains <quantity> server devices for each requested aggr
        And an invetory GET shows that the returned firewalls and servers have is_allocated equals 'true'

    @negative
    Scenario: Incorrect request body data type
    
        When request body is not a JSON object
        And request body is not an array
        Or request body is an array with one or more non-JSON object elements
        Then the response code should be 400
        And 'error' should be 'Request body should be JSON object or array of JSON objects'

    @negative
    Scenario: Request body element has required key missing or null or empty string
    
        When request body is a JSON object
        Or request body is an array containing JSON object
        And one or more JSON objects do not include 'sku' key or key is null or empty string
        Or one or more JSON objects do not include 'quantity' key or key is null or empty string
        Or one or more JSON objects do not include 'aggr_zone' key or key is null or empty string
        Or one or more JSON objects do not include 'dc' key or key is null or empty string
        Then the response code should be 400
        And 'error' should be 'Request body elements must include <key>' where key matches missing required key

    @negative
    Scenario: Request body element has wrong data type
    
        When request body is a JSON object
        Or request body is an array containing JSON objects
        And request body includes all required keys
        And one or more values is the wrong data type for respective key
        Then the response code should be 400
        And 'error' should be 'Request body elements key <key> must be of type <type>' where type matches expected type for that key

    @negative
    Scenario: Quantity is less than 1
    
        When request body is a JSON object
        Or request body is an array containing 
        And one or more JSON objects in request body has a quantity less than 1
        Then the response code should be 400
        And 'error' should be 'Specified quantities must be greated than zero'

    @negative
    Scenario: Datacenter doesn't exist
    
        When request body is a JSON object
        Or request body is an array containing 
        And one or more JSON objects in request body includes a datacenter not listed in service config
        Then the response code should be 400
        And 'error' should be '<datacenter> is not an allowed datacenter'
