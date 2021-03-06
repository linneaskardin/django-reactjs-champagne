// This is a main menu component.
import React from "react"
import { Link } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import { Nav, Navbar, NavItem } from "react-bootstrap";

export default class Mainmenu extends React.Component {
 render() {
   return (
     <Nav className="navbar navbar-inverse bg-light">
   <div className="container-fluid">
   {/* If you want to add the loogo for toolgate this is the place!! */}
   <ul className="nav navbar-nav">
     <li><a href="/"> Hem </a></li>
     <li><a href= "/about"> Om Toolgate Maps </a></li>
     <li><a href= "/toolgate_maps/punkter_pa_karta"> Toolgate Maps </a></li>
     
   </ul>
   <ul className="nav navbar-nav navbar-right">
    <li><a href="/accounts/signup"><span className="glyphicon glyphicon-user"></span> Skapa konto </a></li>
    <li><a href="/accounts/login"><span className="glyphicon glyphicon-log-in"></span> Logga in </a></li>
   </ul>
 </div>
</Nav>
   )
 }
}

{/* <div className="navbar-header">
<a className="navbar-brand"></a> 
</div> */}


