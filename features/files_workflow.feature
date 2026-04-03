Feature: Files workflow
  As a user
  I want upload and download controls to behave predictably
  So that file handling regressions are caught early

  @bdd @regression
  Scenario: Upload and download status flows succeed
    Given the user opens the "files" page
    When the user advances upload processing to completion
    And the user runs the file download status checks
    Then the file upload reports complete
    And the file download status includes the demo hash

