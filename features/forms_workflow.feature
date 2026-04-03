Feature: Forms workflow
  As a user
  I want dynamic widgets to behave consistently
  So that complex form interactions stay reliable

  @bdd @regression
  Scenario: Core forms interactions work end to end
    Given the user opens the "forms" page
    When the user toggles the conditional field on the forms page
    And the user completes the forms workflow using shared test data
    Then the forms page shows the conditional field
    And the forms page keeps advanced widgets ready

