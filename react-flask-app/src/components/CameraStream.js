import React from "react";

export class CameraStream extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        stream: null
        };
    }
    
    componentDidMount() {
        this.setState({
        stream: new MediaSource()
        });
    }
    
    render() {
        // get streams from video_feed
        let feed = document.getElementById("video_feed");
        console.log(feed)

        return (
        <div>
            <img src="\video_feed"></img>
        </div>
        );
    }
}