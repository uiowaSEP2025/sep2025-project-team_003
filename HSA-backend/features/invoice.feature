Feature: Invoice CRUDS
    As a handyman
    I want to CRUD Invoices
    So that I can track them in the application

Scenario: View Invoice page
    Given I am logged in
    Given I have finished the onboarding process
    Given I am on the invoices page
    When I don't see the loading spinner
    Then I should see a table row with the following elements
        | paid                   |
        | 2025-03-27             |
        | 2025-03-20             |
        | Firstorg1, Lastorg1    |

Scenario: View detailed invoice
    Given I am logged in
    Given I have finished the onboarding process
    Given I am on the invoices page
    When I don't see the loading spinner
    And I click the first table row
    Then I wait for 0.5 seconds
    Then I should see the info table with the following data 
        | Label       | Data                |
        | Customer    | Firstorg1, Lastorg1 |       
        | Status      | paid                |
        | Issued Date | 2025-03-20          |
        | Due Date    | 2025-03-27          |
    Then I should see the cost table with the following data
        | Job Description   | Material Subtotal | Total Price |
        | description j1... | $100.00           | $200.00     | 
        | description j2...	| $100.00           | $200.00     |
        | Subtotal:	        | $200.00           | $400.00     | 
        | Discount:         |                   | 10.00%      | 
        | Tax:              |                   | 10%         |
        | Total:            |                   | $396.00     |

Scenario: Delete Invoice
    Given I am logged in
    Given I have finished the onboarding process
    And I am on the invoices page
    When I don't see the loading spinner
    When  I click the delete button specifically
    When I confirm the delete dialog
    Then I wait for 0.5 seconds 
    Then I should see "Nothing to show here" in the table

Scenario: Edit Invoice
    Given I am logged in
    Given I have finished the onboarding process
    And I am on the invoices page
    When I don't see the loading spinner
    Then I wait for 1 seconds
    When I click the edit button specifically
    And I select a status with "issued"
    And I fill in the dates with "02/01/2025" and "02/08/2025"
    And I click the first checkbox in the invoice quotes table
    And I fill in the tax rate with "5"
    And I click the submit button specifically
    And I confirm the edit
    When I don't see the loading spinner
    Then I wait for 0.5 seconds
    When I click the first table row
    Then I should see the info table with the following data 
        | Label       | Data                |
        | Customer    | Firstorg1, Lastorg1 |
        | Status      | issued              |
        | Issued Date | 2025-02-01          |
        | Due Date    | 2025-02-08          |
    Then I should see the cost table with the following data
        | Job Description   | Material Subtotal | Total Price |
        | description j1...	| $100.00	        | $200.00     |
        | Subtotal:         | $100.00	        | $200.00     |
        | Discount:         |                   | 20.00%      |
        | Tax:              |                   | 5%          |
        | Total:            |                   | $168.00     |

Scenario: Create Invocice
    Given I am logged in
    Given I have finished the onboarding process
    And I am on the invoices page
    When I don't see the loading spinner
    When  I click the delete button specifically
    When I confirm the delete dialog
    Then I wait for 0.5 seconds 
    Then I should see "Nothing to show here" in the table
    When I click the create invoice button
    And I select a status with "issued"
    When I fill in the dates with "02/01/2025" and "02/08/2025"
    And I click the first checkbox in the invoice customer table
    Then I wait for 0.5 seconds
    When I click the first checkbox in the invoice quotes table
    Then I wait for 0.5 seconds
    When I fill in the tax rate with "5"
    And I click the submit button specifically
    When I don't see the loading spinner
    Then I wait for 0.5 seconds
    When I click the first table row
    Then I should see the info table with the following data 
        | Label       | Data                |
        | Customer    | Firstorg1, Lastorg1 |
        | Status      | issued              |
        | Issued Date | 2025-02-01          |
        | Due Date    | 2025-02-08          |
    Then I should see the cost table with the following data
        | Job Description   | Material Subtotal | Total Price |
        | description j1...	| $100.00	        | $200.00     |
        | Subtotal:         | $100.00	        | $200.00     |
        | Discount:         |                   | 20.00%      |
        | Tax:              |                   | 5%          |
        | Total:            |                   | $168.00     |


