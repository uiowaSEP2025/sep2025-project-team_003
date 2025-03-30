Feature: Customer CRUDS
    As a handyman
    I want to CRUD customers
    So that I can track them in the application

    Scenario: View Customers page
        Given I am logged in
        Given I am on the customers page
        When I don't see the loading spinner
        Then I should see a table row with the following elements
            | Firstorg1              |
            | Lastorg1               |
            | custorg1@example.com   |
            | 123-456-7890           |
        Then I should not see a table row with the following elements
            | Firstorg2              |
            | Lastorg2               |
            | custorg2@example.com   |
            | 098-765-4321           |

    
    Scenario: Delete customer
        Given I am logged in
        And I am on the customers page
        When I don't see the loading spinner
        When  I click the delete button
        When I confirm the delete dialog
        Then I wait for 0.5 seconds 
        Then I should see "Nothing to show here" in the table

    Scenario: Edit customer
        Given I am logged in
        And I am on the customers page
        When I don't see the loading spinner
        And I click the edit button
        And I fill in first name with "Alex"
        And I fill in last name with "Guo"
        And I fill in email with "aguo2@uiowa.edu"
        And I fill in phone with "321-654-0987"
        And I click the submit button
        When I don't see the loading spinner
        Then I should not see a table row with the following elements
            | Firstorg1              |
            | Lastorg1               |
            | custorg1@example.com   |
            | 123-456-7890           |
        Then I should see a table row with the following elements
            | Alex              |
            | Guo               |
            | aguo2@uiowa.edu   |
            | 321-654-0987      |

