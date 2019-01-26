require("dotenv").config();
import React from "react";
import { StyleSheet, Text, View } from "react-native";
import AuthSpotify from "./components/AuthSpotify";

export default class App extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <Text>Hello World!</Text>
        <AuthSpotify />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  }
});
