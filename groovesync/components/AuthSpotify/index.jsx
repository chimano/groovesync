import React from "react";
import Spotify from "rn-spotify-sdk";
import { Button } from '@ant-design/react-native';

export default class AuthSpotify extends React.Component {
    handleSpotify = () => {
        Spotify.initialize({ clientID: this.props.clientID })
    }
    
    render() {
        return <Button onPress={handleSpotify}>Authenticate Spotify</Button>
    }
}