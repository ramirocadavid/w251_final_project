import React, { Component } from 'react';
import logo from './logo.svg';
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

        this.handleImageUpload = this.handleImageUpload.bind(this);

        this.state = {
            modelOutput: null,
            fileLoading: false
        }
        this.fileInput = React.createRef();
    }

    handleImageUpload() {
        var file = this.fileInput.current.files[0]

        if (file) {
            this.setState({
                fileLoading: true
            })

            getBase64(this.fileInput.current.files[0])
            .then(fileData => {
                fetch('http://localhost:5000/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ file: fileData })
                })
                .then(response => response.json())
                .then(data => {
                    this.setState({
                        modelOutput: data,
                        fileLoading: false
                    })
                })
            });
        }   
    }

    render() {
        var bodyContent;
        if (this.state.modelOutput) {
            bodyContent = <img src={this.state.modelOutput}></img>
        } else if (this.state.fileLoading) {
            bodyContent = <h1>Loading...</h1>
        } else {
            bodyContent = <h1>Please select a file...</h1>
        }

        return (
            <div className="App">
                <header className="App-header">
                    <input
                        accept="image/*"
                        id="fileInput"
                        multiple
                        type="file"
                        onChange={(this.handleImageUpload)}
                        ref={this.fileInput}
                    />
                    
                </header>
                
                <div className='App-body'>
                    {bodyContent}
                </div>
            </div>
        );
    }
}

export default App;
