<template>
  <div>
    <v-row>
      <v-col md="4" offset-md="4" sm="12" offset-sm="0">
        <v-card class="p-4">
          <h1>Login</h1>
          <v-form @submit.prevent="login">
            <v-text-field
              v-model="email"
              label="E-mail"
              required
              :rules="emailRules"
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Password"
              type="password"
              required
              :rules="passwordRules"
            ></v-text-field>
            <v-alert
              class="mt-1"
              type="error"
              dense
              outlined
              v-if="errorMessage"
              >
              {{ errorMessage }}
            </v-alert>
            <v-btn color="#173450" dark large type="submit">Login</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import firebase from 'firebase/app'
import 'firebase/auth'

export default {
  name: 'Login',
  asyncData() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      await firebase.auth().signInWithEmailAndPassword(this.email, this.password)
        .then((user) => {
          this.$router.push('/submit-event');
        })
        .catch((error) => {
          this.errorMessage = error.message;
        });
    }
  },
  created() {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        this.$router.push('/submit-event');
      }
    });
  },
  data() {
    return {
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      passwordRules: [
        v => !!v || 'Password is required',
      ]
    };
  }
}
</script>