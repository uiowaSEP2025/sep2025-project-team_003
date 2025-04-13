Feature: New User Onboardin
  As a handyman
  I want to log in to my account
  So that I can go through the onboarding process

  Scenario: onboarding prefill
    Given I am on the login page
    When I type "devuser" into the username field
    And I type "SepTeam003!" into the password field    
    And I click the submit button specifically
    Then I should see a snackbar with "Login Successful"

    Given I am on the onboarding page
    Then I expect the input field "Service Name" show up 
    When I click the "Prefill 1" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 0.5 seconds
    When I click the "Next 1" button
    Then I expect the input field "Customer First Name" show up
    Then I wait for 0.5 seconds
    When I click the "Prefill 2" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
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
    When I click the "Prefill 5" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 0.5 seconds
    When I click the "Next 5" button
    Then I expect the button "Add Service" show up
    Then I wait for 0.5 seconds
    When I click the "Create" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 0.5 seconds
    Then the current URL should be "/home"
