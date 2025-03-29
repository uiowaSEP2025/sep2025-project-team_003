Feature: Customer CRUDS
    As a handyman
    I want to create customers
    So that I can track them in the application

    Scenario: View Customers page
        Given I am logged in
        Given I am on the customers page
        When I don't see the loading spinner
        Then I should see a table row with the following elements
            | Firstorg1              |
            | Lastorg1               |
            | custorg1@example.com   |
            | custorg1@example.com   |
            | 123-456-7890           |
        Then I should not see a table row with the following elements
            | Firstorg2              |
            | Lastorg2               |
            | custorg2@example.com   |
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
