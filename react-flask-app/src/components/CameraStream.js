import React from "react";

export class CameraStream extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        stream: null
        };
    }
    
    componentDidMount() {
        // this.setState({
        // stream: new MediaSource()
        // });
    }
    
    render() {
        return (
        <img src={"/video_feed/" + this.props.id}></img>
        );
    }
}