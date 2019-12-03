import React, { Component } from 'react';
import Webcam from "react-webcam";
import './App.css';

function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

class App extends Component {

    constructor(props){
        super(props);
        this.state = { screenshot: null }
        // this can be moved directly to the onClick event
        // this.screenshot = this.screenshot.bind(this);
    }
    
    // this is the area I'm having issues with. Thanks!
    screenshot() {
        // access the webcam trough this.refs
        var screenshot = this.refs.webcam.getScreenshot();
        this.setState({screenshot: screenshot});
        fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file: screenshot })
        })
        .then(function(response) {
            console.log(response)
            return response.json()
        })
        .then(data => {
            this.setState({
                modelOutput: data,
                fileLoading: false
            })
        })
    }

    render(){

        return (
            <div>   
                <Webcam audio ={false} ref='webcam'/> 
                <button onClick={this.screenshot.bind(this)}>Capture</button>
                { this.state.screenshot ? <img src={this.state.screenshot} /> : null }
                { this.state.modelOutput ? <img src={this.state.modelOutput} /> : null }
            </div>
            )
    }
}

export default App;
