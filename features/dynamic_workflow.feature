Feature: Dynamic workflow
  As a UI automation engineer
  I want async behavior to stay deterministic under test
  So that dynamic routes are debuggable in CI

  @bdd @regression
  Scenario: Dynamic async controls report expected states
    Given deterministic browser hooks are installed for the dynamic page
    And the user opens the "dynamic" page
    When the user exercises the dynamic async controls
    Then the dynamic page shows the expected async results

