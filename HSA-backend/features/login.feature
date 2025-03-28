Feature: User Login
  As a user
  I want to log in to my account
  So that I can access my dashboard

  Scenario: Successful login
    Given I am on the login page
    When I type "devuser" into the username field
    And I type "devuser" into the username field
    And I type "SepTeam003!" into the password field    
    And I click the submit button
    Then I should see a snackbar with "Login Successful"
    

