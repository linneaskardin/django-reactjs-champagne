//The MenuApp contains the container with the component inside. And this Component will can be
//placed in the index.html file for the diffrent Django-apps. 
import React from "react"
import { render } from "react-dom"
import MenuContainer from "./containers/MenuContainer"

class MenuApp extends React.Component {
  render() {
    return (
      <MenuContainer />
    )
  }
}

render(<MenuApp />, document.getElementById('MenuApp'))
