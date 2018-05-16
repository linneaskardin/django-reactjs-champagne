// This is a main menu component.
import React from "react"
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import { Nav, Navbar, NavItem } from "react-bootstrap";

export default class Mainmenuauth extends React.Component {
 render() {
   return (
     <Nav className="navbar navbar-inverse bg-light">
   <div className="container-fluid">
   {/* If you want to at the loggo of toolgate this is the place! */}
     {/* <a href="#" className="pull-left"><img src="http://www.nattpokalen.se/wp-content/uploads/2018/02/Toolgate-logo-svart-300x162.png"></img></a> */}
   <ul className="nav navbar-nav">
     <li><a href="/"> Hem </a></li>
     <li><a href= "/about"> Om Toolgate Maps </a></li>
     <li><a href= "/toolgate_maps/punkter_pa_karta"> Toolgate Maps </a></li>
     {/* <li><a href= "/my_page"> Min sida </a></li> */}
   </ul>
   <ul className="nav navbar-nav navbar-right">  
     <li><a href="/accounts/logout"><span className="glyphicon glyphicon-log-in"></span> Logga ut </a></li>
   </ul>
 </div>
</Nav>
   )
 }
}


