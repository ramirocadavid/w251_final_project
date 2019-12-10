import React, { Component } from 'react';
import ReactPlayer from 'react-player'
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

    constructor(props) {
        super(props);

        this.handleUpload = this.handleUpload.bind(this);

        this.state = {
            modelType: 'starrynight_final',
            modelInput: null,
            modelOutput: null,
            fileLoading: false,
            fileType: null
        }
        this.fileInput = React.createRef();
    }

    handleUpload() {
        var file = this.fileInput.current.files[0]
        var data = new FormData()
        data.append('file', file)
        console.log(file)
        if (file.type) {
            this.setState({
                fileLoading: true,
                modelInput: file,
                modelOutput: null,
                fileType: file.type
            })
            // Process video
            if (file.type === 'video/mp4') {
                fetch('http://localhost:5000/video', {
                    method: 'POST',
                    headers: { 'Type': this.state.modelType },
                    body: data
                })
                .then(function(response) {
                    console.log("Response:")
                    console.log(response)
                    return response.blob()
                })
                .then(output => {
                    const objectURL = URL.createObjectURL(output);
                    this.setState({
                        modelOutput: objectURL,
                        fileLoading: false,
                    }) 
                })
            // Process image
            } else if (file.type === 'image/jpeg') {
                console.log("ENTERED IMAGE")
                getBase64(file)
                .then(fileData => {
                    fetch('http://localhost:5000/image', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Type': this.state.modelType },
                        body: JSON.stringify({ file: fileData, 'Type': this.state.modelType })
                    })
                    .then(function(response) {
                        return response.json()
                    })
                    .then(data => {
                        console.log(data)
                        this.setState({
                            modelInput: file,
                            modelOutput: data,
                            fileLoading: false
                        })
                    })
                });
            }
        }   
    }

    screenshot() {
        // access the webcam trough this.refs
        var screenshot = this.refs.webcam.getScreenshot();
        this.setState({
            fileInput: screenshot,
            modelInput: screenshot,
            modelOutput: false,
            fileLoading: true,
        });
        fetch('http://localhost:5000/image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Type': this.state.modelType },
            body: JSON.stringify({ file: screenshot })
        })
        .then(function(response) {
            console.log(response)
            return response.json()
        })
        .then(data => {
            this.setState({
                modelOutput: data,
                fileLoading: false,
                fileType: "image/jpeg",
                screenshot: true
            })
        })
    }

    read_file(x) {
        var reader = new FileReader()
        reader.onload = function() {
            var dataURL = reader.result;
            var input = document.getElementById('input');
            input.src = dataURL;
        }
        return reader.readAsDataURL(x)
    }

    render() {

        var bodyContent;
        var bodyInput;
        if (this.state.modelOutput) {
            if (this.state.fileType === "video/mp4") {
                bodyContent = (
                    <ReactPlayer url={this.state.modelOutput} controls={true} class='outputElement'/>
                )
                console.log(this.state.modelInput)
                bodyInput = (
                    <ReactPlayer url={URL.createObjectURL(this.state.modelInput)} controls={true} cass='outputElement'/>
                )
            } else {
                bodyContent = (
                    <img src={this.state.modelOutput} class='outputElement' alt='xxxx'></img>
                )
                if (this.state.screenshot) {
                    bodyInput = (
                            <img src={this.state.modelInput} class='outputElement' id='input' alt='xxxx'></img>
                    )
                } else {
                    bodyInput = (
                        <img src={this.read_file(this.state.modelInput)} class='outputElement' id='input' alt='xxxx'></img>
                    )
                }
            }
        } else if (this.state.fileLoading) {
            bodyContent = <h1>Loading...</h1>
        } else {
            bodyContent = <h1>Select a file or take a screenshot...</h1> } return (
                   <div id="Block" className="App">
                <div id="Title">
                    <header>&nbsp;&nbsp;Neural Style Transfer</header>
                </div>
                <div id="Controls" className="div">
                    <br></br>
                    <div className="dropdown">
                        <button class="dropbtn">Select style</button>
                        <div class="dropdown-content">
                            <a onClick={() => this.setState({ modelType: 'starrynight_final' })}>Starry night</a>
                            <a onClick={() => this.setState({ modelType: 'candy_final' })}>Candy</a>
                            <a onClick={() => this.setState({ modelType: 'lookon_final' })}>Lookon</a>
                        </div>
                    </div>
                    <br></br>
                    <br></br>
                    <input
                        accept="video/mp4, image/jpeg"
                        id="fileInput"
                        multiple
                        type="file"
                        onChange={(this.handleUpload)}
                        ref={this.fileInput}
                        style={{display: 'none'}}
                    />
                    <input 
                        type="button"
                        value="Select file" 
                        onClick={() => document.getElementById('fileInput').click()}
                    />
                    <br></br>
                    <br></br>
                    <button type="button" onClick={this.screenshot.bind(this)}>Take screenshot!</button>
                    <br></br>
                    <br></br>
                </div>
                <div id="Output" className="div">
                    <br></br>
                    <br></br>
                    <div>{bodyInput}</div>
                    <br></br>
                    <div>{bodyContent}</div>
                </div>
                <div id="Camera" style={{"visibility": "hidden"}}>
                    <Webcam audio={false} height={400} width={600} ref='webcam' />
                </div>
            </div>
        );
    }
}

export default App;
