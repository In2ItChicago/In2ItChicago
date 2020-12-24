<template>
  <div>
    <div v-if="authenticatedUser">
      <p>You are logged in as {{ authenticatedUser.email }}.</p>
      <p>Logout?</p>
      <button @click.prevent="logout">Logout</button>
    </div>
    <div v-else>
      <input type="radio" id="hasAccountInput" :value="false" v-model="needsAccount" />
      <label for="hasAccountInput">I have an account</label>
      <br />
      <input type="radio" id="needsAccountInput" :value="true" v-model="needsAccount" />
      <label for="needsAccountInput">I need an account</label>
      <form @submit.prevent="loginOrRegister">
        <input type="email" v-model="email" placeholder="Your email address" />
        <input type="password" v-model="password" placeholder="Your password" />
        <input
          v-if="needsAccount"
          type="password"
          v-model="registrationPassword"
          placeholder="Re-enter Password"
        />
        <button v-text="needsAccount ? 'Register' : 'Login'" />
      </form>
    </div>
  </div>
</template>
<script>
import firebase from 'firebase'

export default {
  name: 'Login',
  asyncData() {
    return {
      authenticatedUser: null,
      email: '',
      password: '',
      registrationPassword: '',
      needsAccount: true
    }
  },
  methods: {
    register() {
      if (this.password === this.registrationPassword) {
        firebase
          .auth()
          .createUserWithEmailAndPassword(this.email, this.password);
        
      } else {
        // display error message
      }
    },
    async login() {
      await firebase.auth().signInWithEmailAndPassword(this.email, this.password);
    },
    loginOrRegister() {
      if (this.needsAccount) {
        this.register()
      } else {
        this.login()
      }
    },
    logout() {
      firebase.auth().signOut();
    }
  },
  created() {
    firebase.auth().onAuthStateChanged(user => {
      this.authenticatedUser = user;
    });
    
  }
}
</script>