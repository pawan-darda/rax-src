Feature: Create an Offering via POST

    As a maintainer of Inventory for project Newton devices
    I want to create a new offering
    So that I can validate newly created devices ensuring their listed offering id matches an existing entry

    Background:

        Given I am authenticated with NIS API
        And I send a POST request to NIS API's Offerings resource

    @positive
    Scenario: Including all three required parameters in the proper type and format
    kmi               nn
        When the following parameters are passed in as the method JSON body
            | offering   | 123456              |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        Then the response code should be 200
        And the Content-Type Header should be "application/json"
        And the response body matches the following
            | offering   | 123456              |
            | name       | 'Performance One'   |
            | type       | 'Server'            |

    @positive
    Scenario: Well formated request but offering name already exists
    
        When the following parameters are passed in as the method JSON body
            | offering   | 456789              |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        And an offering with a matching name already exists
        Then the response code should be 200
        And the Content-Type Header should be "application/json"
        And the response body matches the following
            | offering   | 456789              |
            | name       | 'Performance One'   |
            | type       | 'Server'            |

    @negative
    Scenario: Request body is not a JSON object
    
        When the response body is not of type JSON object
        Then the response code should be 400
        And the 'error' should be 'Request body should be a JSON object'

    @negative
    Scenario: Including any extraneous fields of any type
    
        When the following parameters are passed in as the method JSON body
            | extraneous | 'test'              |
            | offering   | 123456              |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        Then the response code should be 400
        And the 'error' should be 'Extraneous fields included'

    @negative
    Scenario: Well formated request but offering already exists
    
        When the following parameters are passed in as the method JSON body
            | offering   | 123456              |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        And an offering with that id already exists
        Then the response code should be 400
        And the 'error' should be 'Offering with that id already exists'

    @negative
    Scenario: Request missing offering id
    
        When the following parameters are passed in as the method JSON body
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        Then the response code should be 400
        And the 'error' should be 'Must supply a positive integer offering id'

    @negative
    Scenario: Request with offering id null
    
        When the following parameters are passed in as the method JSON body
            | offering   | null                |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        Then the response code should be 400
        And the 'error' should be 'Must supply a positive integer offering id'

    @negative
    Scenario: Request with non-int offering id
    
        When the following parameters are passed in as the method JSON body
            | offering   | '123456'            |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        Then the response code should be 400
        And the 'error' should be 'Must supply a positive integer offering id'

    @negative
    Scenario: Request with offering id less than zero
    
        When the following parameters are passed in as the method JSON body
            | offering   | -123                |
            | name       | 'Performance One'   |
            | type       | 'Server'            |
        Then the response code should be 400
        And the 'error' should be 'Must supply a positive integer offering id'

    @negative
    Scenario: Request missing offering name
    
        When the following parameters are passed in as the method JSON body
            | offering   | 123456              |
            | type       | 'Server'            |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering name as a non-empty string'

    @negative
    Scenario: Request with offering name null
    
        When the following parameters are passed in as the method JSON body
            | offering   | 123456     |
            | name       | null       |
            | type       | 'Server'   |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering name as a non-empty string'

    @negative
    Scenario: Request with non-string offering name
    
        When the following parameters are passed in as the method JSON body
            | offering   | '123456'   |
            | name       | 1          |
            | type       | 'Server'   |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering name as a non-empty string'

    @negative
    Scenario: Request with empty string offering name
    
        When the following parameters are passed in as the method JSON body
            | offering   | '123456'   |
            | name       | ''         |
            | type       | 'Server'   |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering name as a non-empty string'

    @negative
    Scenario: Request missing offering type
    
        When the following parameters are passed in as the method JSON body
            | offering   | 123456              |
            | name       | 'Performance One'   |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering type as a non-empty string'

    @negative
    Scenario: Request with offering type null
    
        When the following parameters are passed in as the method JSON body
            | offering   | 123456              |
            | name       | 'Performance One'   |
            | type       | null                |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering type as a non-empty string'

    @negative
    Scenario: Request with non-string offering type
    
        When the following parameters are passed in as the method JSON body
            | offering   | '123456'            |
            | name       | 'Performance One'   |
            | type       | 1                   |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering type as a non-empty string'

    @negative
    Scenario: Request with empty string offering type
    
        When the following parameters are passed in as the method JSON body
            | offering   | '123456'            |
            | name       | 'Performance One'   |
            | type       | ''                  |
        Then the response code should be 400
        And the 'error' should be 'Must supply an offering type as a non-empty string'