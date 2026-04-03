Feature: Authentication workflow
  As a returning user
  I want to complete login and MFA
  So that I can access the authenticated session controls

  @bdd @smoke
  Scenario: Demo user signs in successfully
    Given the user opens the "auth" page
    When the user signs in with the demo account
    Then the auth page shows a signed-in token
    And the auth page shows the session controls

  @bdd @ui
  Scenario: Demo user completes MFA refresh flow
    Given the user opens the "auth" page
    When the user signs in with the demo account without remember me
    And the user submits the demo MFA code
    Then the auth page shows a rotated refresh token

