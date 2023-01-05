import React from "react";
import { CameraStream } from "./CameraStream";
// class to hold a variable list of streams
export class StreamHolder extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            streams: []
        };
    }
    // add a stream to the list
    addStream(stream) {
        this.setState({
            streams: [...this.state.streams, stream]
        });
    }
    // remove a stream from the list
    removeStream(stream) {
        this.setState({
            streams: this.state.streams.filter(s => s !== stream)
        });
    }
    // render the list of streams
    render() {
        return (
            <div>
                {this.state.streams.map(stream => (
                    <div key={stream.id}>
                        <button onClick={() => this.removeStream(stream)}>
                            Remove
                        </button>
                        <CameraStream stream={stream} />
                    </div>
                ))}
                <button onClick={() => this.addStream(new Stream())}>
                    Add Stream
                </button>
            </div>
        );
    }
}