// This is a main menu component. 
import React from "react"
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import { Nav, Navbar, NavItem } from "react-bootstrap";

export default class Mainmenu extends React.Component {
  render() {
    return (
          <Navbar fluid collapseOnSelect>
          <Nav>
            <NavItem href="/">Hem</NavItem>
            {/* This link only wokrs if you are on the homepage or on toolgate_maps */}
            <NavItem href="toolgate_maps/punkter_pa_karta">Toolgate Maps</NavItem>       
            <NavItem href="accounts/signup">Skapa konto</NavItem>
          </Nav>
          <Nav pullRight>
            <NavItem href="accounts/login">Logga In</NavItem>
          </Nav>
          </Navbar>
    )
  }
}
