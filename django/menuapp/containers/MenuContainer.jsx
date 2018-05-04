// Inside the maincontainer the MainMenu-component is placed. 
import React from "react"
import Mainmenu from "../components/Mainmenu"

export default class MainContainer extends React.Component {
  render() {
    return (
        <div>
      <Mainmenu></Mainmenu>
      </div>
    )
  }
}