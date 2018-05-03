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
            <NavItem href="toolgate_maps/punkter_pa_karta">Toolgate Maps</NavItem>       
            <NavItem>Skapa konto</NavItem>
          </Nav>
          <Nav pullRight>
            <NavItem href="/loggain">Logga In</NavItem>
          </Nav>
          </Navbar>
    )
  }
}
