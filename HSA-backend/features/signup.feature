Feature: User Login
  As a handyman
  I want to create a new user account and new organization
  So that I can start the HSA usage

  Scenario: Signup process
    Given I am on the login page
    When I click the "Signup" button
    Then the current URL should be "/signup"
    Then I expect the input field "User First Name" show up
    When I type on the "User First Name" with "First"
    When I type on the "User Last Name" with "Last"
    When I type on the "User Email" with "first.last@example.com"
    When I type on the "Username" with "firstlast"
    When I type on the "Password" with "SepTeam003!"
    When I type on the "Confirm Password" with "SepTeam003!"
    When I click the "Next 1" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Organization Name" show up
    When I type on the "Organization Name" with "Test LLC"
    Then I expect the input field "Organization Email" has value "first.last@example.com"
    When I type on the "Primary Phone" with "123-123-1234"
    Then I expect the input field "Owner Name" has value "First Last"
    When I click the "Next 2" button
    Then I wait for 0.5 seconds
    Then I expect the input field "Address" show up
    When I type on the "Address" with "9999 Test Address"
    When I type on the "City" with "Test City"
    When I click the "State" button
    When I select any option
    When I type on the "Zip code" with "99999"
    When I click the "Create" button
    Then I wait for 0.5 seconds
    When I click the "Confirm" button
    Then I wait for 2 seconds
    Then the current URL should be "/login"