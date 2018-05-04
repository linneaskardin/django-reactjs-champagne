// This is a main menu component. 
import React from "react"
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import { Nav, Navbar, NavItem } from "react-bootstrap";

export default class Mainmenu extends React.Component {
  render() {
    return (
      <Nav className="navbar navbar-inverse">
    <div className="container-fluid">
    <div className="navbar-header">
      <a className="navbar-brand">Toolgate Maps</a>
    </div>
    <ul className="nav navbar-nav">
      <li className="active"><a href="/"> Hem </a></li>
      <li><a href="toolgate_maps/punkter_pa_karta"> Toolgate Maps </a></li>
      <li><a href="accounts/signup"><span className="glyphicon glyphicon-user"></span> Skapa Konto </a></li>
    </ul>
    <ul className="nav navbar-nav navbar-right">   
      <li><a href="accounts/login"><span className="glyphicon glyphicon-log-in"></span> Logga In </a></li>
      {/* <button className="btn btn-danger navbar-btn">Button</button> */}
    </ul>

  </div>
</Nav>
    )
  }
}


// /* <Navbar fluid collapseOnSelect>
// <Nav>
//   <NavItem href="/">Hem</NavItem>
//   {/* This link only wokrs if you are on the homepage or on toolgate_maps */}
// //   <NavItem href="toolgate_maps/punkter_pa_karta">Toolgate Maps</NavItem>       
// //   <NavItem href=>Skapa konto</NavItem>
// // </Nav>
// // <Nav pullRight>
// //   <NavItem href=>Logga In</NavItem>
// // </Nav>
// // </Navbar> */}