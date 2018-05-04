// Inside the maincontainer the MainMenu-component is placed. 
import React from "react"
import MainmenuAuth from "../components/MainmenuAuth"

export default class MainContainer extends React.Component {
  render() {
    return (
        <div>
      <MainmenuAuth></MainmenuAuth>
      </div>
    )
  }
}