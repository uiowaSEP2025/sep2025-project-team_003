Feature: New User Onboardin
  As a handyman
  I want to log in to my account
  So that I can go through the onboarding process

  Scenario: Onboarding prefill
    Given I am on the login page
    When I type "testuser" into the username field
    And I type "SepTeam003!" into the password field    
    And I click the submit button specifically
    Then I should see a snackbar with "Login Successful"

    Given I am on the onboarding page
    Then I expect the button "Yes" show up
    Then I wait for 0.5 seconds
    When I click the "Yes" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Service Name" show up 
    Then I wait for 0.5 seconds
    When I click the "Next 1" button
    Then I expect the input field "Customer First Name" show up
    Then I wait for 0.5 seconds
    When I click the "Next 2" button
    Then I expect the input field "Material Name" show up
    Then I wait for 0.5 seconds
    When I click the "Next 3" button
    Then I expect the input field "Contractor First Name" show up
    Then I wait for 0.5 seconds
    When I click the "Next 4" button
    Then I expect the input field "Start Date" show up
    Then I wait for 0.5 seconds
    When I click the "Next 5" button
    Then I expect the button "Add Service" show up
    Then I wait for 0.5 seconds
    When I click the "Create" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 0.5 seconds
    Then the current URL should be "/home"

  Scenario: Onboarding real input data
    Given I am on the login page
    When I type "testuser" into the username field
    And I type "SepTeam003!" into the password field    
    And I click the submit button specifically
    Then I should see a snackbar with "Login Successful"

    Given I am on the onboarding page
    Then I expect the button "No" show up
    Then I wait for 0.5 seconds
    When I click the "No" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Service Name" show up 
    Then I wait for 0.5 seconds
    When I type on the "Service Name" with "Test Service"
    When I type on the "Service Description" with "Test Service Description"
    When I click the "Next 1" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Customer First Name" show up
    When I type on the "Customer First Name" with "First"
    When I type on the "Customer Last Name" with "Last"
    When I type on the "Customer Email" with "first.last@example.com"
    When I type on the "Customer Phone Number" with "123-123-1234"
    When I type on the "Add Notes" with "Test Customer Notes"
    When I click the "Next 2" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Material Name" show up
    When I type on the "Material Name" with "Test Material"
    When I click the "Next 3" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Contractor First Name" show up
    When I type on the "Contractor First Name" with "FirstCon"
    When I type on the "Contractor Last Name" with "LastCon"
    When I type on the "Contractor Email" with "firstcon.lastcon@example.com"
    When I type on the "Contractor Phone Number" with "123-123-1234"
    When I click the "Next 4" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Start Date" show up
    When I click the "Select Customer" button
    Then I wait for 0.5 seconds
    Then I expect the button "Checkbox 1" show up
    Then I wait for 0.5 seconds
    When I click the "Checkbox 1" button
    Then I wait for 0.5 seconds
    When I click the "Change" button
    Then I wait for 0.5 seconds
    Then I expect the element "Customer*" has text "First Last"
    When I type on the "Start Date*" with "01/01/2000"
    When I type on the "End Date*" with "01/02/2000"
    When I type on the "Description*" with "Test Job Description"
    When I type on the "Address*" with "9999 Test Job Address"
    When I type on the "City*" with "Test City"
    When I click the "State" button
    Then I wait for 0.5 seconds
    When I select any option
    When I type on the "Zip code*" with "99999"
    When I click the "Next 5" button
    Then I expect the button "Add Service" show up
    When I click the "Add Service" button
    Then I wait for 0.5 seconds
    Then I expect the button "Checkbox 1" show up
    Then I wait for 0.5 seconds
    When I click the "Checkbox 1" button
    Then I wait for 0.5 seconds
    When I click the "Add" button
    Then I wait for 0.5 seconds
    Then I expect the element "Service Table" show up
    Then I expect the button "Add Material" show up
    When I click the "Add Material" button
    Then I wait for 0.5 seconds
    Then I expect the button "Checkbox 1" show up
    Then I wait for 0.5 seconds
    When I click the "Checkbox 1" button
    Then I wait for 0.5 seconds
    When I click the "Add" button
    Then I wait for 0.5 seconds
    Then I expect the element "Material Table" show up
    Then I expect the button "Add Contractor" show up
    When I click the "Add Contractor" button
    Then I wait for 0.5 seconds
    Then I expect the button "Checkbox 1" show up
    Then I wait for 0.5 seconds
    When I click the "Checkbox 1" button
    Then I wait for 0.5 seconds
    When I click the "Add" button
    Then I wait for 0.5 seconds
    Then I expect the element "Contractor Table" show up
    When I click the "Create" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 0.5 seconds
    Then the current URL should be "/home"
