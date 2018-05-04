//The MenuApp contains the container with the component inside. And this Component will can be
//placed in the index.html file for the diffrent Django-apps. 
import React from "react"
import { render } from "react-dom"
import MenuContainerAuth from "./containers/MenuContainerAuth"

class MenuAppAuth extends React.Component {
  render() {
    return (
      <MenuContainerAuth />
    )
  }
}

render(<MenuAppAuth />, document.getElementById('MenuAppAuth'))
