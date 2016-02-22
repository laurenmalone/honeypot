Feature: Telnet Communication
  In order to get attacker details
  As a honeypot liar
  I want to request details over
  a telnet connection.

  Scenario:
    Given a closed telnet connection
     When starting the plugin
     Then an exception is thrown

  Scenario: Gained Location
    Given the attacker is willing to answer location details
     When retrieving the attacker's location
     Then the connection is closed
      And the status is stored
