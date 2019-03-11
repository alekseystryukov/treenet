import React from 'react';
import 'expo';
import { View, Text, Button, StyleSheet, Image, StatusBar, Platform,
    ActivityIndicator, ListView, Linking, WebView, TouchableOpacity } from 'react-native';
import { StackNavigator, DrawerNavigator } from 'react-navigation'; // 1.0.0-beta.27
import {GoogleSignin} from 'react-native-google-signin';


class MyHomeScreen extends React.Component {
  static navigationOptions = {
    drawerLabel: 'Home',
    drawerIcon: ({ tintColor }) => (
      <Image
        source={require('./chats-icon.png')}
        style={[styles.icon, {tintColor: tintColor}]}
      />
    ),
  };

  render() {
    return (
        <View style={styles.view} >
            <Button
                onPress={() => this.props.navigation.navigate('Notifications')}
                title="Go to notifications"
            />
        </View>
    );
  }
}

class MyNotificationsScreen extends React.Component {
  static navigationOptions = {
    drawerLabel: 'Notifications',
    drawerIcon: ({ tintColor }) => (
      <Image
        source={require('./notif-icon.png')}
        style={[styles.icon, {tintColor: tintColor}]}
      />
    ),
  };

  render() {
    return (
     <View style={styles.view} >
          <Button
            onPress={() => this.props.navigation.goBack()}
            title="Go back home"
          />
      </View>
    );
  }
}

const styles = StyleSheet.create({
    icon: {
        width: 24,
        height: 24,
    },
    view: {
        paddingTop: StatusBar.currentHeight,
    },
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#F5FCFF',
    },
});

const MyApp = DrawerNavigator(
    {
        Home: {
        screen: MyHomeScreen,
        },
        Notifications: {
        screen: MyNotificationsScreen,
        },

    },
    // {
    //     contentOptions: {
    //       itemsContainerStyle: {
    //         paddingTop: StatusBar.currentHeight,
    //       },
    //     }
    // }
);

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          isLoading: true,
          accessToken: null,
          user: null
        }
    }

    async componentDidMount() {
        try {
            await GoogleSignin.hasPlayServices({ autoResolve: true });
            await GoogleSignin.configure({
                webClientId: '138430851207-deb2edrpcbrssfp9a62netfot4h53mfn.apps.googleusercontent.com',
                offlineAccess: false
            });

            const user = await GoogleSignin.currentUserAsync();
            console.log(user);
            this.setState({user});
        }
        catch(err) {
            console.log("Play services error", err.code, err.message);
        }


        // try{
        //     let response = await fetch('http://10.217.0.97:3000/auth');
        //     let data = await response.json()
        //     if (response.status == 403){
        //         // Linking.openURL(data["google"]).catch(
        //         //     err => console.error('An error occurred', err)
        //         // );
        //         console.log("hi");
        //     }else{
        //         this.setState({
        //             isLoading: false,
        //             userInfo: data,
        //         }, function() {
        //             console.log(this.state.userInfo);
        //         });
        //     }
        // } catch(error){
        //     console.error(error);
        // }
        //
        // return 0;

    }

    render() {
        if (!this.state.user) {
          return (
            <View style={styles.container}>
              <Button style={{width: 120, height: 44}} onPress={() => { this._signIn(); }}/>
            </View>
          );
        }

        if (this.state.user) {
          return (
            <View style={styles.container}>
              <Text style={{fontSize: 18, fontWeight: 'bold', marginBottom: 20}}>Welcome {this.state.user.name}</Text>
              <Text>Your email is: {this.state.user.email}</Text>

              <TouchableOpacity onPress={() => {this._signOut(); }}>
                <View style={{marginTop: 50}}>
                  <Text>Log out</Text>
                </View>
              </TouchableOpacity>
            </View>
          );
        }
    }

    _signIn() {
        GoogleSignin.signIn()
        .then((user) => {
          console.log(user);
          this.setState({user: user});
        })
        .catch((err) => {
          console.log('WRONG SIGNIN', err);
        })
        .done();
    }

    _signOut() {
        GoogleSignin.revokeAccess().then(() => GoogleSignin.signOut()).then(() => {
          this.setState({user: null});
        })
        .done();
    }
}
