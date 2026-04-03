Feature: Tables workflow
  As an operator
  I want to edit and filter the data grid
  So that tabular workflows remain stable under automation

  @bdd @regression
  Scenario: Grid editing and filtering remain consistent
    Given the user opens the "tables" page
    When the user updates table row 1
    And the user filters the table to active rows
    Then the table shows six visible rows
    And table row 3 remains active

