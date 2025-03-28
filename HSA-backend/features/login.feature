Feature: User Login
  As a user
  I want to log in to my account
  So that I can access my dashboard

  Scenario: Successful login
    Given I am on the login page
    When I type "devuser" into the username field
    And I type "SepTeam003!" into the password field    
    And I click the submit button
    Then I should see a snackbar with "Login Successful"

  Scenario: Unsuccessfull login
    Given I am on the login page
    When I type "baduser" into the username field
    And I type "badpass!" into the password field    
    And I click the submit button
    Then I should see a snackbar with "Username or password is invalid, please try again!"
